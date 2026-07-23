# ADR 0012: Real Job Execution with Enforced Timeouts

## Status

Accepted

## Context

`WorkerExecutionLoop` previously renewed a worker's lease, called `worker.start()`, and released the lease again around a placeholder comment: `# Job execution would happen here.` No job ever actually ran anything. Separately, `ReleaseLeaseService.execute()` unconditionally called `worker.complete()`, meaning every job that reached this point was treated as successful; there was no path by which a job could be recorded as failed during normal execution.

Building real execution surfaced a further gap: `Job` had no concept of what to run at all. Every field on the entity (`resources`, `priority`, `constraints`, `status`, timestamps) describes scheduling and resource accounting, never a runnable unit of work. `CreateJobRequest`, the public API's job creation payload, only accepts resource numbers.

## Decision

- `Job` gains two new fields: `command: list[str] | None = None` (argv-style, never a shell string, so execution never needs `shell=True` and can never be exploited via shell injection) and `exit_code: int | None = None`, recording the outcome of the most recent execution attempt. `Job.complete()` and `Job.fail()` now accept and store an optional `exit_code`.
- A new `JobExecutionService` runs a job's command as a real subprocess via `Popen`, enforcing `execution_timeout` with a two-stage shutdown: `SIGTERM` first, then `SIGKILL` after a configurable grace period if the process does not exit, mirroring how systemd, Docker, and Kubernetes handle shutdown. It distinguishes three outcomes: clean success, clean failure (nonzero exit), and timeout (killed by us), returning a structured `JobExecutionResult` rather than a bare boolean. A job with no command (today's API default) is treated as an immediate no-op success, so every job, real or not, flows through the same code path.
- `WorkerExecutionLoop` calls `JobExecutionService`, then branches on the real result: `worker.complete(exit_code=...)` on success, `worker.fail(exit_code=...)` otherwise. `Worker.complete()`/`Worker.fail()` already transition their own `running_job` internally, so the loop calls exactly one of the two, never both, and never mutates the job's status directly, avoiding a double-transition that would raise `InvalidJobTransition`.
- `ReleaseLeaseService` no longer decides job outcome. It is reduced to its actual responsibility: deleting the lease record. Lease release is now unconditional and happens regardless of whether the job succeeded, failed, or timed out; job outcome and lease lifecycle are separate concerns, decided in that order by the execution loop, not conflated inside lease bookkeeping.
- `command` and `exit_code` are **not** exposed through `CreateJobRequest` or any public API endpoint. `JobExecutionService` and the full execution path are real and fully tested at the service layer, directly, with real subprocesses. Exposing arbitrary caller-supplied commands over an endpoint that has no authentication yet (see README, "What's Next": API hardening remains pending) would mean shipping unauthenticated remote code execution. This is a deliberate scoping decision, not an oversight: build the capability correctly and prove it works, defer exposing it until authentication exists.
- Both `SqliteJobRepository` and `PostgresJobRepository` gained `command`/`exit_code` columns and round-trip logic, proven by dedicated tests against both backends, so a job's command and execution result survive process restarts and backend switches identically to every other field.

## Consequences

The worker execution loop now does real work: a job with a command genuinely runs, genuinely gets killed if it overruns its timeout, and genuinely reports success or failure based on what actually happened, not a hardcoded assumption.

A job can now be marked `FAILED` during normal execution for the first time; previously this path did not exist in the happy-path loop at all; only reconciliation's `reclaim()` (ADR 0011) could ever fail a job, and only after infrastructure failure, never after the job's own command genuinely failed.

The system currently has real, tested execution capability that is intentionally unreachable from the public API. This is visible and explainable: anyone reading `Job.command`'s docstring or this ADR sees exactly why, and exactly what has to happen (authentication) before it can be safely exposed. This is preferable to either not building it (leaving the placeholder) or building it and exposing it prematurely (creating a real security hole in the name of feature completeness).

`Job.execution_timeout` and `Job.has_timed_out()` existed before this change but were never consulted by anything. They are now load-bearing: `execution_timeout` directly drives `JobExecutionService`'s real subprocess timeout.

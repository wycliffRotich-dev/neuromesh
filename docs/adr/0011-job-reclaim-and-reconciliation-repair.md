# ADR 0011: Job Reclaim Semantics for Reconciliation Repair

## Status

Accepted

## Context

The reconciliation loop (`RecoverExpiredLeaseService`, `RecoverOfflineNodeService`) was built to repair jobs abandoned by a dead worker or an offline node, returning them to the scheduling queue. Both services called `Job.unschedule()` to do this.

`Job.unschedule()` only permits a transition from `SCHEDULED`. Tracing the actual production call path (`AssignWorkerService`) shows a job is moved to `RUNNING` immediately after its lease is acquired, and the default lease duration (30 seconds) is intended to cover the job's execution, not just its dispatch. This means a job whose lease expires, or whose node goes offline mid-execution, is almost always in `RUNNING` state, not `SCHEDULED`, when reconciliation needs to repair it. `SCHEDULED` only describes a narrow window between a worker accepting a job and actually starting it.

Both recovery services' existing tests passed despite this, because neither test called `worker.start()` before triggering recovery, leaving the job in `SCHEDULED` for the entire test. This meant the tests validated a setup that does not reflect how jobs actually behave once a lease is genuinely in effect. Once the tests were corrected to call `worker.start()`, both services failed with `InvalidJobTransition: Only scheduled jobs may be unscheduled.`, confirming reconciliation could not repair the primary case it exists for: a worker dying while genuinely executing a job.

Fixing the transition to allow `RUNNING → QUEUED` on its own would create a second problem: a job that is repeatedly reassigned to, and abandoned by, the same unhealthy node would be requeued indefinitely, with no terminal state, silently consuming scheduling cycles and node capacity forever.

## Decision

- `Job` gains a new `reclaim()` method, distinct from `retry()`. `retry()` handles a job that failed on its own merits (bad exit code, exception) and is only callable from `FAILED`. `reclaim()` handles a job abandoned due to infrastructure failure, a dead worker or offline node, not a fault of the job itself, and is callable from `SCHEDULED` or `RUNNING`.
- `reclaim()` consumes a retry attempt using the same accounting as `retry()` (`record_retry()`, bounded by `max_retries`). If retries remain, the job returns to `QUEUED`. If retries are exhausted, the job transitions directly to `FAILED` instead of requeuing again.
- `_ALLOWED_TRANSITIONS` is updated: `RUNNING` now permits `QUEUED` (the requeue path), and `SCHEDULED` now permits `FAILED` (the narrow case where a worker is reclaimed before ever starting the job, with no retries left).
- `RecoverExpiredLeaseService` and `RecoverOfflineNodeService` call `job.reclaim()` in place of `job.unschedule()`.
- A job with `max_retries=0` fails immediately on its first abandonment rather than ever being requeued. This is deliberate: a job with no configured retry tolerance should not receive an implicit one through reconciliation.

## Consequences

Reconciliation now correctly repairs the case it was built for: a job actually running when its worker or node fails, not only the narrow pre-execution window the original implementation covered.

A job repeatedly abandoned by unhealthy infrastructure reaches a terminal `FAILED` state after exhausting its retry budget, rather than being requeued forever. This bounds the resource cost of a single bad node or worker on overall cluster throughput.

This also means retry budget is now a shared resource between job-level failures and infrastructure-level abandonment. A job that fails twice on its own and is then abandoned once by a dying worker consumes the same `retry_count` either way. This was a deliberate simplification: from the scheduler's perspective, both are "the job did not complete and consumed an attempt," and tracking them as separate budgets was judged to add complexity without a clear benefit. If operational experience later shows these need to be distinguished (for example, to alert differently on infrastructure flakiness versus job-level bugs), the two counters can be split without changing the public transition semantics.

The original test suites for both recovery services only ever exercised the `SCHEDULED` case (`worker.accept()` without `worker.start()`), which is why this gap went undetected. Both suites were rewritten to explicitly cover the requeue path (retries remaining) and the fail-outright path (retries exhausted), rather than relying on a single test that happened to pass for the wrong reason.

# ADR 0013: Job Listing with Repository-Pushed Ordering

## Status

Accepted

## Context

The dashboard's `RecentJobs` component existed but was never connected to real data: `DashboardPage` passed it `jobs={[]}` hardcoded, and its own `Job` type (`name`, `node: string`) matched nothing in the actual domain model or any API response. Separately, there was no way to list jobs at all: `JobRepository` supported `list()` (all jobs, unordered), `list_queued()`, `get_by_id()`, and `save()`, but nothing scoped to "the most recent N jobs," which is what any dashboard or monitoring view actually needs.

The first implementation considered for this simply called `job_repository.list()` inside the application service, then sorted and sliced the result in Python. This works, but for the sqlite and postgres backends it means loading every row in the `jobs` table into memory on every request, only to discard all but the most recent 50. That's application-layer logic doing a database's job, and it doesn't scale with the number of historical jobs even though the response size never changes.

## Decision

- `JobRepository` gains a fourth query method, `list_recent(limit: int) -> list[Job]`, alongside the existing `list()` and `list_queued()`. This is genuine domain vocabulary, "give me the most recent N jobs" is a meaningful request at the repository interface, not a persistence detail leaking upward, the same way `list_queued()` already is.
- Each implementation pushes the ordering and limit down to its own storage engine: `ORDER BY submitted_at DESC LIMIT ?` in SQLite, `ORDER BY submitted_at DESC LIMIT %s` in PostgreSQL, and a Python `sorted(...)[:limit]` in the in-memory repository, since there's no database to push work to there.
- `ListJobsService` is a thin coordinator: it calls `list_recent(MAX_JOBS_RETURNED)` and returns the result directly. It contains no sorting or slicing logic of its own.
- `GET /jobs` is added, returning the 50 most recent jobs via the new `ListJobsResponse`/`JobSummaryResponse` schemas.
- `GetJobResponse` and `JobSummaryResponse` both expose `exit_code`, `submitted_at`, `started_at`, and `completed_at`, the execution outcome fields introduced in ADR 0012. Neither schema exposes `command`, consistent with that ADR's decision to keep job commands internal until authentication exists. This is enforced by an explicit test asserting the field's absence from the response body, not left as a documentation-only claim.

## Consequences

Listing jobs scales with the size of the response (bounded at 50), not with the size of the `jobs` table, regardless of backend.

The dashboard can now be wired to real job data for the first time; this ADR only covers the backend half of that, the frontend components (`RecentJobs`, the job-fetching hook, and the API client) still need to be rebuilt against this real response shape, since the existing `RecentJobs` component was built against an imagined shape that never matched the backend.

`list_recent()` follows the same shared pattern as every other repository query in this codebase: one interface, three implementations, each correct for its own backend rather than a single implementation forcing an inferior strategy onto the others.

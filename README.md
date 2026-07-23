# NeuroMesh

### A distributed AI workload scheduler built to demonstrate Clean Architecture, Domain-Driven Design, and real infrastructural decoupling.

[![Tests](https://img.shields.io/badge/tests-157%20passed-brightgreen)](#test-coverage)
[![License](https://img.shields.io/badge/license-MIT-blue)](#)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](#tech-stack)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](#tech-stack)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)](#tech-stack)
[![React](https://img.shields.io/badge/React-TypeScript-61DAFB?logo=react&logoColor=black)](#tech-stack)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](#tech-stack)

NeuroMesh takes workloads, matches them against available compute nodes based on resource requirements and constraints, and manages the full lifecycle: queued, scheduled, running, completed, failed, retried. Jobs run through workers registered against nodes, and job execution ownership is enforced through time-bound leases rather than a simple assignment flag.

This isn't an attempt to replace Kubernetes or Ray. It's a deliberate implementation of **Clean Architecture** and **Domain-Driven Design** applied to a scheduling problem, where the architectural boundaries are enforced by tests, not just diagrams, and every non-obvious decision is written down as an ADR.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.12 |
| **API Framework** | FastAPI |
| **Database** | PostgreSQL (raw `psycopg`, no ORM), with SQLite for select repositories in local development |
| **Frontend** | React + TypeScript + Vite |
| **Testing** | pytest, contract testing across repository implementations |
| **CI/CD** | GitHub Actions |
| **Containerization** | Docker + Docker Compose |
| **Architecture** | Clean Architecture, Domain-Driven Design, Repository Pattern, SOLID |

---

## Why This Exists

Most scheduler side-projects are a single `main.py` script wrapped in a `while True` loop polling an in-memory dictionary. They work fine, right up until you need to swap the persistence engine, add a new constraint type, or figure out why a job silently disappeared, or why two workers picked up the same job at once.

NeuroMesh was built around one rule: **the domain logic doesn't know or care where the data lives.** Jobs, nodes, workers, and the allocation algorithm are pure Python with zero infrastructure dependencies. The database is a detail, not the foundation. This project is a concrete demonstration that these architectural patterns aren't just conference-talk vocabulary; they're guardrails that keep a codebase understandable as it grows, and as its correctness requirements get harder.

---

## Key Capabilities

- **Job lifecycle management**: explicit state transitions (Queued → Scheduled → Running → Completed/Failed) with configurable retry policies and priority-aware scheduling
- **Constraint-aware best-fit allocator**: matches workloads to nodes based on resource requirements and labels, while skipping nodes that are draining or offline
- **Worker registration and heartbeats**: workers register against a node, report liveness, and are marked dead when heartbeats stop
- **Lease-based execution ownership**: when a worker accepts a job, it holds a renewable, expiring lease on that job, so retries, reconnects, and network failures can't result in two workers executing the same job
- **Node liveness tracking**: heartbeat-based health checks, automatic detection of offline nodes, and resource reclamation when work fails or nodes disappear
- **Live dashboard**: submit jobs, register nodes, and watch cluster health, resource usage, and activity in real time

---

## Architecture

The system is split into four layers, with dependencies pointing inward:

**Domain**: `Job`, `Node`, `Worker`, and `Lease` aggregates enforce their own invariants. The scheduling algorithm and job lifecycle state machine live here as plain Python, with no imports from FastAPI or psycopg. Delete the infrastructure layer entirely and the domain tests still pass.

**Application**: Services such as `ScheduleJobService`, `AssignWorkerService`, `AcquireLeaseService`, and `ClusterHealthService` coordinate domain objects and repositories without embedding business rules that belong one layer down. A `WorkerExecutionLoop` drives a worker through renewing its lease, running its assigned job, and releasing the lease on completion. A `ReconciliationLoop` catches the failure modes the happy path can't: crashed workers, expired leases, state left inconsistent by infrastructure failures. It repairs both jobs abandoned before execution started and, the more common case, jobs abandoned mid-execution, reclaiming them back to the queue within their retry budget and failing them outright once that budget is exhausted, so a single unhealthy node can't cause a job to be reassigned and abandoned indefinitely.

**Infrastructure**: PostgreSQL implementations exist for every repository (`Node`, `Job`, `Worker`, `Lease`, `Event`), written with raw `psycopg` instead of an ORM, a deliberate choice to keep query behavior and transaction boundaries visible rather than abstracted away. `Node`, `Job`, and `Event` additionally have SQLite implementations for local development. Every repository is validated against a shared **contract test suite** run against each backend it supports, so switching between implementations, or trusting that they behave identically, is a tested guarantee rather than an assumption.

**Presentation**: FastAPI endpoints for jobs, nodes, and workers that validate input, call an application service, and return a response. No business logic lives here.

Every non-obvious decision, why domain owns scheduling instead of application, why raw psycopg over an ORM, how job lifecycle transitions are enforced, why leases exist instead of a simple assignment field, why the execution loop and reconciliation loop are separate components, is documented as an ADR in `/docs/adr`.

---

## Test Coverage

157 tests across domain, application, infrastructure, and API layers:

- Full domain logic coverage: job lifecycle, retry policy, constraint matching, node and worker liveness, lease semantics
- Contract tests proving every repository's in-memory, SQLite (where implemented), and PostgreSQL implementations behave identically, including foreign-key-enforced aggregates such as `Worker` and `Lease`
- Application service tests for every use case, including lease acquisition, renewal, release, and reconciliation repair, covering both the requeue-with-retries-remaining path and the fail-outright-once-exhausted path
- API-level tests against real FastAPI endpoints

```bash
pytest
```

---

## Running It

```bash
git clone https://github.com/wycliffRotich-dev/neuromesh.git
cd neuromesh
docker-compose up --build
```

This starts the API and a Postgres instance, and runs migrations. Run the frontend separately:

```bash
cd frontend
npm install
npm run dev
```

CI runs the full test suite against a live Postgres service on every push. See `.github/workflows`.

---

## What's Next

- Wiring real job execution into the worker execution loop; currently the lease renew/release cycle runs around a placeholder step
- Hardening the API for public deployment (rate limiting, structured logging, error tracking)
- Live cloud deployment with CI/CD auto-deploy on merge
- A short demo walkthrough of a job going from submission to completion on the live dashboard

---

## Scope

This isn't trying to compete with Kubernetes or Ray at scale. It's a demonstration of how to build a system that stays understandable as it grows: layered correctly, tested honestly, and documented well enough that someone else could pick it up and know exactly why every piece is where it is, including the pieces that are deliberately half-built and marked as such.

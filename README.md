# NeuroMesh
### A distributed AI workload scheduler built to demonstrate clean architecture, domain-driven design, and real infrastructural decoupling.

[![Tests](https://img.shields.io/badge/tests-111%2B%20passed-brightgreen)](#test-coverage)
[![License](https://img.shields.io/badge/license-MIT-blue)](#)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](#tech-stack)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](#tech-stack)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)](#tech-stack)
[![React](https://img.shields.io/badge/React-TypeScript-61DAFB?logo=react&logoColor=black)](#tech-stack)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](#tech-stack)

NeuroMesh takes workloads, matches them against available compute nodes based on resource requirements and constraints, and manages the full lifecycle; queued, scheduled, running, completed, failed, retried.

This isn't an attempt to replace Kubernetes or Ray. It's a deliberate implementation of **Clean Architecture** and **Domain-Driven Design** applied to a scheduling problem, where the architectural boundaries are enforced by tests, not just diagrams, and every non-obvious decision is written down as an ADR.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.12 |
| **API Framework** | FastAPI |
| **Database** | PostgreSQL (raw `psycopg`, no ORM) + SQLite for local/dev |
| **Frontend** | React + TypeScript + Vite |
| **Testing** | pytest, contract testing across repository implementations |
| **CI/CD** | GitHub Actions |
| **Containerization** | Docker + Docker Compose |
| **Architecture** | Clean Architecture, Domain-Driven Design, Repository Pattern, SOLID |

---

## Why This Exists

Most scheduler side-projects are a single `main.py` script wrapped in a `while True` loop polling an in-memory dictionary. They work fine, right up until you need to swap the persistence engine, add a new constraint type, or figure out why a job silently disappeared.

NeuroMesh was built around one rule: **the domain logic doesn't know or care where the data lives.** Jobs, nodes, and the allocation algorithm are pure Python with zero infrastructure dependencies. The database is a detail, not the foundation. This project is a concrete demonstration that these architectural patterns aren't just conference-talk vocabulary, they're guardrails that keep a codebase understandable as it grows.

---

## Key Capabilities

- **Job lifecycle management**; explicit state transitions (Queued → Scheduled → Running → Completed/Failed) with configurable retry policies and priority-aware scheduling
- **Constraint-aware best-fit allocator**; matches workloads to nodes based on resource requirements and labels, while skipping nodes that are draining or offline
- **Node liveness tracking**; heartbeat-based health checks, automatic detection of offline nodes, and resource reclamation when work fails or nodes disappear
- **Live dashboard**; submit jobs, register nodes, and watch cluster health, resource usage, and activity in real time

---

## Architecture

The system is split into four layers, with dependencies pointing inward:

**Domain**: Job and Node aggregates enforce their own invariants. The scheduling algorithm lives here as plain Python, with no imports from FastAPI or psycopg. Delete the infrastructure layer entirely and the domain tests still pass.

**Application**: Services like `ScheduleJobService`, `AssignWorkerService`, and `ClusterHealthService` coordinate domain objects and repositories without embedding business rules that belong one layer down.

**Infrastructure**: Two repository implementations, SQLite and PostgreSQL, both written with raw `psycopg` instead of an ORM, a deliberate choice to keep query behavior and transaction boundaries visible rather than abstracted away. Both implementations are validated against the same **contract test suite**, so switching between them is a tested guarantee, not an assumption.

**Presentation**: FastAPI endpoints that validate input, call an application service, and return a response. No business logic lives here.

Every non-obvious decision, why domain owns scheduling instead of application, why raw psycopg over an ORM, how job lifecycle transitions are enforced, is documented as an ADR in `/docs/adr`.

---

## Test Coverage

111+ tests across domain, application, infrastructure, and API layers:
- Full domain logic coverage; job lifecycle, retry policy, constraint matching, node liveness
- Contract tests proving SQLite and Postgres repositories behave identically
- Application service tests for every use case
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

CI runs the full test suite against a live Postgres service on every push, see `.github/workflows`.

---

## What's Next

- Hardening the API for public deployment (rate limiting, structured logging, error tracking)
- Live cloud deployment with CI/CD auto-deploy on merge
- A short demo walkthrough of a job going from submission to completion on the live dashboard

---

## Scope

This isn't trying to compete with Kubernetes or Ray at scale, it's a demonstration of how to build a system that stays understandable as it grows: layered correctly, tested honestly, and documented well enough that someone else could pick it up and know exactly why every piece is where it is.

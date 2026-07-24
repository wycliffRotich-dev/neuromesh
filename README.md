# AetherGrid

### An open-source AI control plane for orchestrating inference and batch workloads across distributed compute clusters.

AetherGrid provides intelligent workload scheduling, event-driven orchestration, REST APIs, real-time observability, and infrastructure decoupling for modern AI systems. It is built using Domain-Driven Design (DDD), Clean Architecture, Test-Driven Development (TDD), and modern Python engineering practices.

[![Tests](https://img.shields.io/badge/tests-176%20passed-brightgreen)](#test-coverage)
[![License](https://img.shields.io/badge/license-MIT-blue)](#license)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](#tech-stack)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](#tech-stack)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)](#tech-stack)
[![React](https://img.shields.io/badge/React-TypeScript-61DAFB?logo=react&logoColor=black)](#tech-stack)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](#tech-stack)

---

## Overview

AetherGrid is a lightweight AI control plane designed to orchestrate distributed inference and batch workloads across compute clusters.

It accepts workloads, matches them to available compute nodes based on resource requirements and scheduling constraints, coordinates workers responsible for execution, and manages the complete workload lifecycle from submission to completion. Ownership of running work is protected through renewable execution leases, allowing the platform to recover safely from worker crashes, network interruptions, and infrastructure failures.

Rather than attempting to replace platforms such as Kubernetes or Ray, AetherGrid focuses on demonstrating how modern distributed systems can be engineered using strong architectural boundaries, explicit domain models, and infrastructure-independent business logic.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.12 |
| **API Framework** | FastAPI |
| **Database** | PostgreSQL (`psycopg`) with SQLite implementations for selected repositories |
| **Frontend** | React + TypeScript + Vite |
| **Testing** | pytest + repository contract testing |
| **CI/CD** | GitHub Actions |
| **Containerization** | Docker & Docker Compose |
| **Architecture** | Clean Architecture, Domain-Driven Design, SOLID, Repository Pattern |

---

## Why AetherGrid Exists

Many scheduling projects work well until real-world requirements begin to appear.

Adding multiple persistence backends, recovering abandoned jobs, enforcing worker ownership, tracking infrastructure health, or introducing new scheduling constraints often causes application logic and infrastructure code to become tightly coupled.

AetherGrid approaches the problem differently.

The core scheduling engine is completely independent of databases, APIs, frameworks, and infrastructure concerns. Domain models encapsulate business rules while application services coordinate workflows. Infrastructure exists only to support the domain rather than define it.

This separation makes the platform easier to evolve, easier to test, and easier to understand as complexity grows.

---

## Key Capabilities

- Intelligent workload scheduling across distributed compute nodes
- Resource-aware best-fit allocation
- Job lifecycle management
- Worker registration and heartbeat monitoring
- Lease-based execution ownership
- Automatic recovery of abandoned workloads
- Event-driven architecture with persistent event recording
- REST API built with FastAPI
- PostgreSQL persistence using raw `psycopg`
- SQLite implementations for local development
- Interactive React dashboard
- Repository contract testing across multiple storage implementations

---

## Architecture

AetherGrid follows **Clean Architecture** with strict dependency inversion.

### Domain

The Domain layer contains aggregate roots including Jobs, Nodes, Workers, and Leases. Business rules, scheduling decisions, retry policies, and state transitions are implemented entirely in pure Python without framework or database dependencies.

### Application

Application services coordinate workflows between repositories and domain objects.

Services handle scheduling, worker registration, lease acquisition, lease renewal, reconciliation, cluster health, and job execution orchestration while leaving business rules inside the domain.

### Infrastructure

Infrastructure provides implementations for repositories using PostgreSQL and SQLite.

Every repository implementation is validated using a shared contract test suite, guaranteeing identical behavior across supported storage backends.

### Presentation

The Presentation layer exposes REST APIs through FastAPI.

Endpoints validate requests, invoke application services, and return responses without embedding business logic.

---

## Test Coverage

The project currently contains **176 automated tests** covering:

- Domain entities
- Value objects
- Scheduling algorithms
- Application services
- Repository contract tests
- SQLite repositories
- PostgreSQL repositories
- FastAPI endpoints
- Worker lifecycle
- Lease management
- Event recording
- Cluster reconciliation

Run the complete suite with:

```bash
pytest
```

All tests currently pass.

---

## Running AetherGrid

Clone the repository:

```bash
git clone https://github.com/wycliffRotich-dev/aethergrid.git
cd aethergrid
```

Start the backend services:

```bash
docker compose up --build
```

Run the frontend:

```bash
cd frontend
npm install
npm run dev
```

Continuous Integration executes the complete test suite automatically on every push using GitHub Actions.

---

## Project Structure

```
app/
├── application/
├── domain/
├── infrastructure/
└── presentation/

frontend/
docs/
tests/
```

---

## Roadmap

- Live WebSocket event streaming
- Distributed worker execution
- GPU-aware scheduling
- Multi-node execution
- Kubernetes integration
- Authentication and RBAC
- Metrics and Prometheus integration
- Distributed tracing
- Plugin architecture
- Cloud deployment
- Multi-cluster orchestration

---

## Engineering Principles

- Clean Architecture
- Domain-Driven Design
- Test-Driven Development
- SOLID Principles
- Dependency Inversion
- Repository Pattern
- Event-Driven Design
- Explicit Architectural Decision Records (ADRs)

---

## License

MIT License.

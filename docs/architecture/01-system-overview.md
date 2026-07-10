# System Overview

```mermaid
flowchart LR

User["👤 User"]

Browser["🌐 React Dashboard"]

API["⚡ FastAPI"]

Application["Application Layer"]

Domain["Domain Layer"]

Infrastructure["Infrastructure Layer"]

DB[(PostgreSQL)]

User --> Browser
Browser --> API
API --> Application
Application --> Domain
Domain --> Infrastructure
Infrastructure --> DB
```

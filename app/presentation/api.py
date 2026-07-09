from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.presentation.routers.jobs import (
    router as jobs_router,
)
from app.presentation.routers.nodes import (
    router as nodes_router,
)

app = FastAPI(
    title="NeuroMesh API",
    description="Distributed AI Control Plane",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs_router)
app.include_router(nodes_router)


@app.get("/")
def root() -> dict[str, str]:
    """
    Health endpoint.
    """
    return {
        "message": "Welcome to NeuroMesh API",
    }
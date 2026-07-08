from fastapi import FastAPI

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

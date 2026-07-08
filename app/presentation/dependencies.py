from __future__ import annotations

import os

from app.application.services.create_job_service import (
    CreateJobService,
)
from app.application.services.create_node_service import (
    CreateNodeService,
)
from app.application.services.get_job_service import (
    GetJobService,
)
from app.application.services.get_node_service import (
    GetNodeService,
)
from app.application.services.list_nodes_service import (
    ListNodesService,
)
from app.domain.repositories.job_repository import JobRepository
from app.domain.repositories.node_repository import NodeRepository
from app.infrastructure.repositories.in_memory_job_repository import (
    InMemoryJobRepository,
)
from app.infrastructure.repositories.in_memory_node_repository import (
    InMemoryNodeRepository,
)
from app.infrastructure.repositories.sqlite_connection import (
    create_connection,
)
from app.infrastructure.repositories.sqlite_job_repository import (
    SqliteJobRepository,
)
from app.infrastructure.repositories.sqlite_node_repository import (
    SqliteNodeRepository,
)


def _build_repositories() -> tuple[
    JobRepository,
    NodeRepository,
]:
    """
    Choose the repository backend based on the
    NEUROMESH_STORAGE_BACKEND environment variable.

    Defaults to "memory" for local development and tests,
    so existing behavior is unchanged unless explicitly
    configured otherwise. Set to "sqlite" (optionally with
    NEUROMESH_DB_PATH) for persistence across restarts.
    """
    backend = os.getenv(
        "NEUROMESH_STORAGE_BACKEND",
        "memory",
    ).lower()

    if backend == "sqlite":
        db_path = os.getenv(
            "NEUROMESH_DB_PATH",
            "neuromesh.db",
        )
        connection = create_connection(db_path)

        return (
            SqliteJobRepository(connection),
            SqliteNodeRepository(connection),
        )

    return (
        InMemoryJobRepository(),
        InMemoryNodeRepository(),
    )


_job_repository, _node_repository = _build_repositories()


def get_create_job_service() -> CreateJobService:
    """
    Return the application service responsible
    for creating jobs.
    """
    return CreateJobService(
        job_repository=_job_repository,
    )


def get_get_job_service() -> GetJobService:
    """
    Return the application service responsible
    for retrieving jobs.
    """
    return GetJobService(
        job_repository=_job_repository,
    )


def get_create_node_service() -> CreateNodeService:
    """
    Return the application service responsible
    for creating compute nodes.
    """
    return CreateNodeService(
        node_repository=_node_repository,
    )


def get_get_node_service() -> GetNodeService:
    """
    Return the application service responsible
    for retrieving compute nodes.
    """
    return GetNodeService(
        node_repository=_node_repository,
    )


def get_list_nodes_service() -> ListNodesService:
    """
    Return the application service responsible
    for listing compute nodes.
    """
    return ListNodesService(
        node_repository=_node_repository,
    )

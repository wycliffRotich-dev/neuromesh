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
from app.application.services.scheduler_service import (
    SchedulerService,
)
from app.domain.repositories.job_repository import (
    JobRepository,
)
from app.domain.repositories.node_repository import (
    NodeRepository,
)
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
    Choose the repository backend.
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

        connection = create_connection(
            db_path,
        )

        return (
            SqliteJobRepository(
                connection,
            ),
            SqliteNodeRepository(
                connection,
            ),
        )

    return (
        InMemoryJobRepository(),
        InMemoryNodeRepository(),
    )


_job_repository, _node_repository = (
    _build_repositories()
)


_scheduler_service = SchedulerService(
    node_repository=_node_repository,
    job_repository=_job_repository,
)


def get_create_job_service() -> CreateJobService:
    """
    Return CreateJobService.
    """

    return CreateJobService(
        job_repository=_job_repository,
        scheduler_service=_scheduler_service,
    )


def get_get_job_service() -> GetJobService:
    """
    Return GetJobService.
    """

    return GetJobService(
        job_repository=_job_repository,
    )


def get_create_node_service() -> CreateNodeService:
    """
    Return CreateNodeService.
    """

    return CreateNodeService(
        node_repository=_node_repository,
    )


def get_get_node_service() -> GetNodeService:
    """
    Return GetNodeService.
    """

    return GetNodeService(
        node_repository=_node_repository,
    )


def get_list_nodes_service() -> ListNodesService:
    """
    Return ListNodesService.
    """

    return ListNodesService(
        node_repository=_node_repository,
    )

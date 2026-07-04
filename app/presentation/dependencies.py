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
from app.infrastructure.repositories.in_memory_job_repository import (
    InMemoryJobRepository,
)
from app.infrastructure.repositories.in_memory_node_repository import (
    InMemoryNodeRepository,
)

_job_repository = InMemoryJobRepository()
_node_repository = InMemoryNodeRepository()


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
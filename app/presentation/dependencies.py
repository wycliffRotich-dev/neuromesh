from app.application.services.create_job_service import (
    CreateJobService,
)
from app.application.services.get_job_service import (
    GetJobService,
)
from app.infrastructure.repositories.in_memory_job_repository import (
    InMemoryJobRepository,
)

_job_repository = InMemoryJobRepository()


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
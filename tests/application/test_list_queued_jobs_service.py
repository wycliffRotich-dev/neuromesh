from app.application.services.list_queued_jobs_service import (
    ListQueuedJobsService,
)
from app.domain.entities.job import Job
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.infrastructure.repositories.in_memory_job_repository import (
    InMemoryJobRepository,
)


def test_list_queued_jobs_returns_only_queued_jobs() -> None:
    """
    Only queued jobs should be returned.
    """

    queued = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=2,
            memory_mib=2048,
            vram_mib=1024,
        ),
    )
    queued.queue()

    submitted = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=2,
            memory_mib=2048,
            vram_mib=1024,
        ),
    )

    repository = InMemoryJobRepository(
        [
            queued,
            submitted,
        ],
    )

    service = ListQueuedJobsService(
        repository,
    )

    jobs = service.execute()

    assert queued in jobs
    assert submitted not in jobs

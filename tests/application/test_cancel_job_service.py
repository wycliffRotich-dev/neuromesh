from app.application.services.cancel_job_service import (
    CancelJobService,
)
from app.domain.entities.job import Job
from app.domain.enums.job_status import JobStatus
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.infrastructure.repositories.in_memory_job_repository import (
    InMemoryJobRepository,
)


def test_cancel_job_service_cancels_a_queued_job() -> None:
    """
    A queued job can be cancelled.
    """

    job = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=4,
            memory_mib=4096,
            vram_mib=2048,
        ),
    )

    job.queue()

    repository = InMemoryJobRepository(
        [
            job,
        ],
    )

    service = CancelJobService(
        repository,
    )

    service.execute(
        job.id,
    )

    assert job.status == JobStatus.CANCELLED

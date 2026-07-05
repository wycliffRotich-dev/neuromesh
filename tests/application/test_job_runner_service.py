from app.application.services.job_runner_service import (
    JobRunnerService,
)
from app.domain.entities.job import Job
from app.domain.enums.job_status import JobStatus
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.infrastructure.repositories.in_memory_job_repository import (
    InMemoryJobRepository,
)


def test_job_runner_starts_scheduled_jobs() -> None:
    """
    Scheduled jobs should automatically
    transition to RUNNING.
    """

    job = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=2,
            memory_mib=2048,
            vram_mib=1024,
        ),
    )

    job.queue()
    job.assign_to(NodeId.new())

    repository = InMemoryJobRepository(
        [
            job,
        ],
    )

    service = JobRunnerService(
        repository,
    )

    service.execute()

    assert job.status == JobStatus.RUNNING

from app.application.services.job_completion_service import (
    JobCompletionService,
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


def test_job_completion_service_completes_running_jobs() -> None:
    """
    Running jobs should automatically
    transition to COMPLETED.
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
    job.start()

    repository = InMemoryJobRepository(
        [
            job,
        ],
    )

    service = JobCompletionService(
        repository,
    )

    service.execute()

    assert job.status == JobStatus.COMPLETED

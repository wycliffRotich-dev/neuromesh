from app.application.services.start_job_service import (
    StartJobService,
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


def test_start_job_service_starts_a_scheduled_job() -> None:
    """
    A scheduled job can be started.
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
    job.assign_to(NodeId.new())

    repository = InMemoryJobRepository()
    repository._jobs[str(job.id)] = job

    service = StartJobService(repository)

    service.execute(job.id)

    assert job.status == JobStatus.RUNNING

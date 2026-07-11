from app.application.services.create_job_service import (
    CreateJobService,
)
from app.application.services.scheduler_service import (
    SchedulerService,
)
from app.domain.entities.job import Job
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.infrastructure.repositories.in_memory_job_repository import (
    InMemoryJobRepository,
)
from app.infrastructure.repositories.in_memory_node_repository import (
    InMemoryNodeRepository,
)


def test_create_job_service_creates_and_persists_job() -> None:
    """
    Creating a job should persist it even when no
    compute nodes are currently available.
    """

    job_repository = InMemoryJobRepository()
    node_repository = InMemoryNodeRepository()

    scheduler_service = SchedulerService(
        job_repository=job_repository,
        node_repository=node_repository,
    )

    service = CreateJobService(
        job_repository=job_repository,
        scheduler_service=scheduler_service,
    )

    resources = ResourceRequirements(
        cpu_cores=4,
        memory_mib=8192,
        vram_mib=2048,
    )

    job = service.execute(resources)

    assert isinstance(job, Job)

    stored = job_repository.get_by_id(job.id)

    assert stored is not None
    assert stored.id == job.id
    assert stored.resources == resources

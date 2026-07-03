from app.application.services.create_job_service import (
    CreateJobService,
)
from app.domain.entities.job import Job
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.infrastructure.repositories.in_memory_job_repository import (
    InMemoryJobRepository,
)


def test_create_job_service_creates_and_persists_job() -> None:
    repository = InMemoryJobRepository()

    service = CreateJobService(
        job_repository=repository,
    )

    resources = ResourceRequirements(
        cpu_cores=4,
        memory_mib=8192,
        vram_mib=2048,
    )

    job = service.execute(resources)

    assert isinstance(job, Job)

    stored = repository.get_by_id(job.id)

    assert stored is job
    assert stored.resources == resources
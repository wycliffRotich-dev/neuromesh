from app.domain.entities.job import Job
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


def test_jobs_have_default_priority() -> None:
    """
    Newly created jobs should have
    default priority zero.
    """

    job = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=2,
            memory_mib=2048,
            vram_mib=1024,
        ),
    )

    assert job.priority == 0

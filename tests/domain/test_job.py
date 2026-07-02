from datetime import UTC

from app.domain.entities.job import Job
from app.domain.enums.job_status import JobStatus
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


def test_new_job_defaults_to_submitted() -> None:
    job = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=2,
            memory_mib=4096,
        ),
    )

    assert job.status is JobStatus.SUBMITTED


def test_job_has_submission_timestamp() -> None:
    job = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=1,
            memory_mib=1024,
        ),
    )

    assert job.submitted_at.tzinfo is UTC


def test_job_has_resource_requirements() -> None:
    resources = ResourceRequirements(
        cpu_cores=8,
        memory_mib=32768,
        vram_mib=24576,
    )

    job = Job(
        id=JobId.new(),
        resources=resources,
    )

    assert job.resources == resources
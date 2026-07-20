from app.domain.entities.job import Job
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


def create_job() -> Job:
    return Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=1,
            memory_mib=512,
            vram_mib=0,
        ),
    )


def test_job_lifecycle_happy_path() -> None:
    job = create_job()

    job.queue()

    assert job.is_queued()

    job.assign_to(
        NodeId.new(),
    )

    assert job.is_scheduled()

    job.start()

    assert job.is_running()

    job.complete()

    assert job.is_completed()


def test_job_can_be_unscheduled() -> None:
    job = create_job()

    job.queue()

    job.assign_to(
        NodeId.new(),
    )

    job.unschedule()

    assert job.is_queued()


def test_job_can_fail() -> None:
    job = create_job()

    job.queue()

    job.assign_to(
        NodeId.new(),
    )

    job.start()

    job.fail()

    assert job.is_failed()

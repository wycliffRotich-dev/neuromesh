from app.domain.entities.job import Job
from app.domain.enums.job_status import JobStatus
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


def test_job_can_be_created() -> None:
    job = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=4,
            memory_mib=8192,
            vram_mib=2048,
        ),
    )

    assert isinstance(job.id, JobId)
    assert job.resources.cpu_cores == 4
    assert job.resources.memory_mib == 8192
    assert job.resources.vram_mib == 2048


def test_jobs_with_different_ids_are_not_equal() -> None:
    resources = ResourceRequirements(
        cpu_cores=2,
        memory_mib=4096,
        vram_mib=1024,
    )

    job1 = Job(
        id=JobId.new(),
        resources=resources,
    )

    job2 = Job(
        id=JobId.new(),
        resources=resources,
    )

    assert job1 != job2


def test_job_can_be_assigned_to_a_node() -> None:
    job = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=4,
            memory_mib=4096,
            vram_mib=2048,
        ),
    )

    node_id = NodeId.new()

    job.queue()
    job.assign_to(node_id)

    assert job.assigned_node_id == node_id
    assert job.status == JobStatus.SCHEDULED
from app.domain.entities.job import Job
from app.domain.entities.node import Node
from app.domain.entities.worker import Worker
from app.domain.enums.job_status import JobStatus
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


def test_worker_can_run_job() -> None:
    """
    A ready worker should accept a scheduled job and
    transition it into the RUNNING state.
    """

    node = Node(
        id=NodeId("node-1"),
        capacity=ResourceRequirements(
            cpu_cores=8,
            memory_mib=16_000,
            vram_mib=0,
        ),
    )

    job = Job(
        id="job-1",
        resources=ResourceRequirements(
            cpu_cores=2,
            memory_mib=2_000,
            vram_mib=0,
        ),
    )

    job.queue()
    job.assign_to(node.id)

    worker = Worker(
        id="worker-1",
        node=node,
    )

    worker.ready()
    worker.accept(job)
    worker.start()

    assert worker.running_job is job
    assert worker.status.name == "BUSY"
    assert job.status is JobStatus.RUNNING

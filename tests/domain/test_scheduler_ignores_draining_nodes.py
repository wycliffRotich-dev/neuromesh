from app.domain.entities.job import Job
from app.domain.entities.node import Node
from app.domain.services.scheduler import Scheduler
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


def test_scheduler_ignores_draining_nodes() -> None:
    """
    Draining nodes should not receive
    newly scheduled jobs.
    """

    draining = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=8,
            memory_mib=16384,
            vram_mib=8192,
        ),
    )

    available = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=8,
            memory_mib=16384,
            vram_mib=8192,
        ),
    )

    draining.drain()

    job = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=2,
            memory_mib=2048,
            vram_mib=1024,
        ),
    )

    scheduler = Scheduler()

    selected = scheduler.select_node(
        job,
        [
            draining,
            available,
        ],
    )

    assert selected == available

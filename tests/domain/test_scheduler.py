from app.domain.entities.job import Job
from app.domain.entities.node import Node
from app.domain.services.scheduler import Scheduler
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


def test_scheduler_selects_first_matching_node() -> None:
    scheduler = Scheduler()

    job = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=4,
            memory_mib=4096,
        ),
    )

    nodes = [
        Node(
            id=NodeId.new(),
            capacity=ResourceRequirements(
                cpu_cores=2,
                memory_mib=2048,
            ),
        ),
        Node(
            id=NodeId.new(),
            capacity=ResourceRequirements(
                cpu_cores=8,
                memory_mib=16384,
            ),
        ),
    ]

    selected = scheduler.select_node(job, nodes)

    assert selected is nodes[1]


def test_scheduler_returns_none_when_no_node_matches() -> None:
    scheduler = Scheduler()

    job = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=32,
            memory_mib=65536,
        ),
    )

    nodes = [
        Node(
            id=NodeId.new(),
            capacity=ResourceRequirements(
                cpu_cores=8,
                memory_mib=8192,
            ),
        )
    ]

    assert scheduler.select_node(job, nodes) is None
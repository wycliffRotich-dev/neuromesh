from app.domain.entities.node import Node
from app.domain.services.scheduler import Scheduler
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


def test_scheduler_selects_best_fit_node() -> None:
    scheduler = Scheduler()

    large = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=32,
            memory_mib=65536,
            vram_mib=24576,
        ),
    )

    medium = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=16,
            memory_mib=32768,
            vram_mib=16384,
        ),
    )

    small = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=8,
            memory_mib=16384,
            vram_mib=8192,
        ),
    )

    selected = scheduler.select_node(
        job=type(
            "JobStub",
            (),
            {
                "resources": ResourceRequirements(
                    cpu_cores=4,
                    memory_mib=4096,
                    vram_mib=2048,
                )
            },
        )(),
        nodes=[large, medium, small],
    )

    assert selected == small
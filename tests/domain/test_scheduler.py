from app.domain.entities.node import Node
from app.domain.services.scheduler import Scheduler
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


def test_scheduler_selects_node_with_sufficient_resources() -> None:
    scheduler = Scheduler()

    node = Node(
        id="node-1",
        cpu_cores=16,
        memory_mib=32768,
        vram_mib=16384,
    )

    requirements = ResourceRequirements(
        cpu_cores=4,
        memory_mib=4096,
        vram_mib=2048,
    )

    selected = scheduler.schedule(
        requirements,
        [node],
    )

    assert selected == node


def test_scheduler_returns_none_when_no_node_matches() -> None:
    scheduler = Scheduler()

    node = Node(
        id="node-1",
        cpu_cores=2,
        memory_mib=2048,
        vram_mib=0,
    )

    requirements = ResourceRequirements(
        cpu_cores=8,
        memory_mib=16384,
        vram_mib=8192,
    )

    selected = scheduler.schedule(
        requirements,
        [node],
    )

    assert selected is None
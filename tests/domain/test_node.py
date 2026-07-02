from app.domain.entities.node import Node
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


def test_node_can_host_smaller_job() -> None:
    node = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=16,
            memory_mib=65536,
            vram_mib=24576,
        ),
    )

    job_resources = ResourceRequirements(
        cpu_cores=4,
        memory_mib=8192,
        vram_mib=8192,
    )

    assert node.can_host(job_resources)


def test_node_rejects_large_job() -> None:
    node = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=4,
            memory_mib=8192,
            vram_mib=4096,
        ),
    )

    job_resources = ResourceRequirements(
        cpu_cores=8,
        memory_mib=16384,
        vram_mib=8192,
    )

    assert not node.can_host(job_resources)
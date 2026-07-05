from app.application.services.cluster_utilization_service import (
    ClusterUtilizationService,
)
from app.domain.entities.node import Node
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.infrastructure.repositories.in_memory_node_repository import (
    InMemoryNodeRepository,
)


def test_cluster_utilization_reports_allocated_resources() -> None:
    """
    Cluster utilization should report
    allocated resources.
    """

    node = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=8,
            memory_mib=8192,
            vram_mib=4096,
        ),
    )

    node.allocate(
        ResourceRequirements(
            cpu_cores=2,
            memory_mib=2048,
            vram_mib=1024,
        ),
    )

    repository = InMemoryNodeRepository(
        [
            node,
        ],
    )

    service = ClusterUtilizationService(
        repository,
    )

    utilization = service.execute()

    assert utilization.cpu_cores == 2
    assert utilization.memory_mib == 2048
    assert utilization.vram_mib == 1024

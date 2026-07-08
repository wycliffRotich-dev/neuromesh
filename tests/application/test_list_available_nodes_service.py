from datetime import UTC, datetime, timedelta

from app.application.services.list_nodes_service import (
    ListNodesService,
)
from app.domain.entities.node import Node
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.infrastructure.repositories.in_memory_node_repository import (
    InMemoryNodeRepository,
)


def test_list_nodes_returns_only_alive_nodes() -> None:
    """
    Only alive nodes should be returned.
    """

    alive = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=16,
            memory_mib=32768,
            vram_mib=16384,
        ),
    )

    offline = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=16,
            memory_mib=32768,
            vram_mib=16384,
        ),
    )

    offline.last_seen_at = datetime.now(UTC) - timedelta(minutes=2)

    repository = InMemoryNodeRepository(
        [
            alive,
            offline,
        ],
    )

    service = ListNodesService(
        repository,
    )

    nodes = service.execute()

    assert alive in nodes
    assert offline not in nodes

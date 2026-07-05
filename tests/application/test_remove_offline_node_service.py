from datetime import UTC, datetime, timedelta

from app.application.services.remove_offline_node_service import (
    RemoveOfflineNodeService,
)
from app.domain.entities.node import Node
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.infrastructure.repositories.in_memory_node_repository import (
    InMemoryNodeRepository,
)


def test_remove_offline_node_service_removes_offline_node() -> None:
    """
    An offline node can be removed
    from the cluster.
    """

    node = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=8,
            memory_mib=16384,
            vram_mib=8192,
        ),
    )

    node.last_seen_at = (
        datetime.now(UTC)
        - timedelta(minutes=2)
    )

    repository = InMemoryNodeRepository(
        [
            node,
        ],
    )

    service = RemoveOfflineNodeService(
        repository,
    )

    service.execute(
        node.id,
    )

    assert repository.get_by_id(
        node.id,
    ) is None

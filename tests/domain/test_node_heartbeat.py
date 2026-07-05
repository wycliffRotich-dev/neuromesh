from datetime import UTC, datetime

from app.domain.entities.node import Node
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


def test_node_heartbeat_updates_last_seen_at() -> None:
    """
    A heartbeat updates the node's last seen timestamp.
    """

    node = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=16,
            memory_mib=32768,
            vram_mib=16384,
        ),
    )

    before = datetime.now(UTC)

    node.heartbeat()

    assert node.last_seen_at >= before

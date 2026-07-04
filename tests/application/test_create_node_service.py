from __future__ import annotations

from app.application.services.create_node_service import (
    CreateNodeService,
)
from app.domain.entities.node import Node
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.infrastructure.repositories.in_memory_node_repository import (
    InMemoryNodeRepository,
)


def test_create_node_service_creates_and_persists_node() -> None:
    """
    Creating a node should persist it in the repository.
    """
    repository = InMemoryNodeRepository()

    service = CreateNodeService(
        node_repository=repository,
    )

    capacity = ResourceRequirements(
        cpu_cores=8,
        memory_mib=16384,
        vram_mib=4096,
    )

    node = service.execute(capacity)

    assert isinstance(node, Node)

    stored = repository.get_by_id(node.id)

    assert stored is node
    assert stored.capacity == capacity
    assert stored.available == capacity
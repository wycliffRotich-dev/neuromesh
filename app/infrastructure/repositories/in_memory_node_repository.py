from __future__ import annotations

from app.domain.entities.node import Node
from app.domain.repositories.node_repository import NodeRepository
from app.domain.value_objects.node_id import NodeId


class InMemoryNodeRepository(NodeRepository):
    """
    In-memory implementation of the NodeRepository.
    """

    def __init__(
        self,
        nodes: list[Node] | None = None,
    ) -> None:
        self._nodes: dict[str, Node] = {
            str(node.id): node for node in (nodes or [])
        }

    def list_available(self) -> list[Node]:
        return list(self._nodes.values())

    def get_by_id(
        self,
        node_id: NodeId,
    ) -> Node | None:
        return self._nodes.get(str(node_id))
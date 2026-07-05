from __future__ import annotations

from app.domain.entities.node import Node
from app.domain.repositories.node_repository import (
    NodeRepository,
)
from app.domain.value_objects.node_id import NodeId


class InMemoryNodeRepository(NodeRepository):
    """
    In-memory implementation of the node repository.
    """

    def __init__(
        self,
        nodes: list[Node] | None = None,
    ) -> None:
        self._nodes: dict[NodeId, Node] = {}

        if nodes is not None:
            for node in nodes:
                self.save(node)

    def save(
        self,
        node: Node,
    ) -> None:
        """
        Persist a compute node.
        """
        self._nodes[node.id] = node

    def list(
        self,
    ) -> list[Node]:
        """
        Return all registered compute nodes.
        """
        return list(self._nodes.values())

    def get_by_id(
        self,
        node_id: NodeId,
    ) -> Node | None:
        """
        Return a node by its identifier.
        """
        return self._nodes.get(node_id)
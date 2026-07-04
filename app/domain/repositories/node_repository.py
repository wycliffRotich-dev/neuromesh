from __future__ import annotations

from typing import Protocol

from app.domain.entities.node import Node
from app.domain.value_objects.node_id import NodeId


class NodeRepository(Protocol):
    """
    Contract for persisting and retrieving compute nodes.
    """

    def save(
        self,
        node: Node,
    ) -> None:
        """
        Persist a compute node.
        """
        ...

    def list(
        self,
    ) -> list[Node]:
        """
        Return all registered compute nodes.
        """
        ...

    def list_available(
        self,
    ) -> list[Node]:
        """
        Return all nodes currently available for scheduling.
        """
        ...

    def get_by_id(
        self,
        node_id: NodeId,
    ) -> Node | None:
        """
        Return a node by its identifier.
        """
        ...
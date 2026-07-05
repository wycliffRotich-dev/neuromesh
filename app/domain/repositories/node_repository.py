from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.node import Node
from app.domain.value_objects.node_id import NodeId


class NodeRepository(ABC):
    """
    Repository abstraction for compute nodes.
    """

    @abstractmethod
    def save(
        self,
        node: Node,
    ) -> None:
        ...

    @abstractmethod
    def list(
        self,
    ) -> list[Node]:
        ...

    @abstractmethod
    def list_available(
        self,
    ) -> list[Node]:
        ...

    @abstractmethod
    def get_by_id(
        self,
        node_id: NodeId,
    ) -> Node | None:
        ...

    @abstractmethod
    def delete(
        self,
        node_id: NodeId,
    ) -> None:
        """
        Remove a node from the repository.
        """
        ...
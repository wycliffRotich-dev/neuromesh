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

        print(
            f"[INIT] Repository id={id(self)}"
        )

        if nodes is not None:
            for node in nodes:
                self.save(node)

    def save(
        self,
        node: Node,
    ) -> None:
        print(
            f"[SAVE] Repository id={id(self)}"
        )

        self._nodes[node.id] = node

        print(
            f"[SAVE] Nodes stored={len(self._nodes)}"
        )

    def list(
        self,
    ) -> list[Node]:
        print(
            f"[LIST] Repository id={id(self)}"
        )

        print(
            f"[LIST] Nodes stored={len(self._nodes)}"
        )

        return list(
            self._nodes.values(),
        )

    def list_available(
        self,
    ) -> list[Node]:
        return [
            node
            for node in self._nodes.values()
            if node.is_alive()
            and not node.is_draining()
        ]

    def get_by_id(
        self,
        node_id: NodeId,
    ) -> Node | None:
        return self._nodes.get(
            node_id,
        )

    def delete(
        self,
        node_id: NodeId,
    ) -> None:
        self._nodes.pop(
            node_id,
            None,
        )

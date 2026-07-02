from __future__ import annotations

from app.domain.entities.node import Node
from app.domain.repositories.node_repository import NodeRepository


class InMemoryNodeRepository(NodeRepository):
    """
    In-memory implementation of the NodeRepository.
    """

    def __init__(
        self,
        nodes: list[Node] | None = None,
    ) -> None:
        self._nodes = nodes or []

    def list_available(self) -> list[Node]:
        return list(self._nodes)
from __future__ import annotations

from app.domain.entities.node import Node
from app.domain.repositories.node_repository import (
    NodeRepository,
)


class ListNodesService:
    """
    Application service responsible for retrieving
    all registered compute nodes.
    """

    def __init__(
        self,
        node_repository: NodeRepository,
    ) -> None:
        self._node_repository = node_repository

    def execute(self) -> list[Node]:
        """
        Return all registered compute nodes.
        """
        return self._node_repository.list_available()
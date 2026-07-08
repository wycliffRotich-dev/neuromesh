from __future__ import annotations

from app.domain.entities.node import Node
from app.domain.repositories.node_repository import (
    NodeRepository,
)


class ListOfflineNodesService:
    """
    Application service responsible for listing
    offline compute nodes.
    """

    def __init__(
        self,
        node_repository: NodeRepository,
    ) -> None:
        self._node_repository = node_repository

    def execute(
        self,
    ) -> list[Node]:
        """
        Retrieve all offline compute nodes.
        """
        return [node for node in self._node_repository.list() if not node.is_alive()]

from __future__ import annotations

from app.domain.entities.node import Node
from app.domain.repositories.node_repository import (
    NodeRepository,
)


class ListNodesService:
    """
    Application service responsible for listing
    registered compute nodes that are currently
    alive.
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
        Retrieve all compute nodes that have sent
        a heartbeat within the configured timeout.
        """
        return [
            node
            for node in self._node_repository.list()
            if node.is_alive()
        ]

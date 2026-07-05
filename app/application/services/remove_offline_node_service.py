from __future__ import annotations

from app.domain.repositories.node_repository import (
    NodeRepository,
)
from app.domain.value_objects.node_id import NodeId


class RemoveOfflineNodeService:
    """
    Application service responsible for removing
    offline compute nodes.
    """

    def __init__(
        self,
        node_repository: NodeRepository,
    ) -> None:
        self._node_repository = node_repository

    def execute(
        self,
        node_id: NodeId,
    ) -> None:
        """
        Remove an offline compute node.
        """
        node = self._node_repository.get_by_id(
            node_id,
        )

        if node is None:
            return

        if node.is_alive():
            return

        self._node_repository.delete(
            node_id,
        )

from __future__ import annotations

from app.domain.value_objects.node_id import NodeId


class NodeNotFoundError(Exception):
    """
    Raised when a compute node with the specified
    identifier cannot be found.
    """

    def __init__(
        self,
        node_id: NodeId,
    ) -> None:
        super().__init__(f"Node with id '{node_id}' was not found.")
        self.node_id = node_id

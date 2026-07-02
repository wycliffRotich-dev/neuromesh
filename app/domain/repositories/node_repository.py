from __future__ import annotations

from typing import Protocol

from app.domain.entities.node import Node


class NodeRepository(Protocol):
    """
    Contract for retrieving compute nodes.
    """

    def list_available(self) -> list[Node]:
        """
        Return all nodes currently available for scheduling.
        """
        ...
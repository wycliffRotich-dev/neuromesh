from __future__ import annotations

from dataclasses import dataclass

from app.domain.repositories.node_repository import (
    NodeRepository,
)


@dataclass(slots=True)
class ClusterHealth:
    """
    Represents the health status of the cluster.
    """

    total_nodes: int
    alive_nodes: int
    offline_nodes: int


class ClusterHealthService:
    """
    Application service responsible for reporting
    cluster health.
    """

    def __init__(
        self,
        node_repository: NodeRepository,
    ) -> None:
        self._node_repository = node_repository

    def execute(
        self,
    ) -> ClusterHealth:
        """
        Return a summary of the cluster health.
        """
        nodes = self._node_repository.list()

        total_nodes = len(nodes)
        alive_nodes = sum(1 for node in nodes if node.is_alive())
        offline_nodes = total_nodes - alive_nodes

        return ClusterHealth(
            total_nodes=total_nodes,
            alive_nodes=alive_nodes,
            offline_nodes=offline_nodes,
        )

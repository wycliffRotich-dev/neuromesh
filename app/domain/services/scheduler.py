from __future__ import annotations

from app.domain.entities.job import Job
from app.domain.entities.node import Node


class Scheduler:
    """
    Domain service responsible for selecting the most
    appropriate node for a job.
    """

    def select_node(
        self,
        job: Job,
        nodes: list[Node],
    ) -> Node | None:
        """
        Select the best-fit node capable of hosting the job.

        The best-fit node is the one that leaves the least
        remaining CPU capacity after allocation.
        """
        candidates = [
            node
            for node in nodes
            if node.can_host(job.resources)
        ]

        if not candidates:
            return None

        return min(
            candidates,
            key=lambda node: (
                node.available.cpu_cores
                - job.resources.cpu_cores
            ),
        )
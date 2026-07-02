from __future__ import annotations

from app.domain.entities.job import Job
from app.domain.entities.node import Node


class Scheduler:
    """
    Domain service responsible for selecting an appropriate
    node for a job.
    """

    def select_node(
        self,
        job: Job,
        nodes: list[Node],
    ) -> Node | None:
        """
        Return the first node capable of hosting the job.

        Returns:
            A suitable Node if one exists, otherwise None.
        """
        for node in nodes:
            if node.can_host(job.resources):
                return node

        return None
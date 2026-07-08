from __future__ import annotations

from app.domain.entities.job import Job
from app.domain.entities.node import Node


class Scheduler:
    """
    Domain service responsible for selecting the most
    appropriate node for a job.
    """

    def _matches_constraints(
        self,
        job: Job,
        node: Node,
    ) -> bool:
        """
        Return True if the node satisfies all job
        scheduling constraints.

        Jobs without a constraints attribute are
        considered compatible with every node.
        """
        constraints = getattr(
            job,
            "constraints",
            {},
        )

        for key, value in constraints.items():
            if node.labels.get(key) != value:
                return False

        return True

    def select_node(
        self,
        job: Job,
        nodes: list[Node],
    ) -> Node | None:
        """
        Select the best-fit node capable of hosting
        the given job.

        A node must:
        - be alive
        - not be draining
        - satisfy all job constraints
        - have sufficient available resources

        Among all valid candidates, choose the node
        that leaves the least remaining CPU capacity
        after allocation.
        """
        candidates = [
            node
            for node in nodes
            if (
                node.is_alive()
                and not node.is_draining()
                and self._matches_constraints(
                    job,
                    node,
                )
                and node.can_host(
                    job.resources,
                )
            )
        ]

        if not candidates:
            return None

        return min(
            candidates,
            key=lambda node: node.available.cpu_cores - job.resources.cpu_cores,
        )

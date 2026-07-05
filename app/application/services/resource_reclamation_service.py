from __future__ import annotations

from app.domain.enums.job_status import JobStatus
from app.domain.repositories.job_repository import JobRepository
from app.domain.repositories.node_repository import (
    NodeRepository,
)


class ResourceReclamationService:
    """
    Application service responsible for releasing
    resources occupied by completed jobs.
    """

    def __init__(
        self,
        job_repository: JobRepository,
        node_repository: NodeRepository,
    ) -> None:
        self._job_repository = job_repository
        self._node_repository = node_repository

    def execute(
        self,
    ) -> None:
        """
        Release resources for completed jobs.
        """
        for job in self._job_repository.list():
            if job.status != JobStatus.COMPLETED:
                continue

            if job.assigned_node_id is None:
                continue

            node = self._node_repository.get_by_id(
                job.assigned_node_id,
            )

            if node is None:
                continue

            node.release(
                job.resources,
            )

            self._node_repository.save(
                node,
            )

from __future__ import annotations

from app.domain.repositories.job_repository import JobRepository
from app.domain.repositories.node_repository import (
    NodeRepository,
)


class RescheduleJobsService:
    """
    Application service responsible for
    rescheduling jobs from offline nodes.
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
        Return scheduled jobs assigned to
        offline nodes back to the queue.
        """

        for node in self._node_repository.list():
            if node.is_alive():
                continue

            for job in self._job_repository.list():
                if job.assigned_node_id != node.id:
                    continue

                job.assigned_node_id = None
                job.status = job.status.QUEUED

                self._job_repository.save(job)

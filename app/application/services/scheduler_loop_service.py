from __future__ import annotations

from app.domain.repositories.job_repository import JobRepository
from app.domain.repositories.node_repository import (
    NodeRepository,
)
from app.domain.services.scheduler import Scheduler
from app.domain.enums.job_status import JobStatus


class SchedulerLoopService:
    """
    Application service responsible for
    scheduling queued jobs onto healthy nodes.
    """

    def __init__(
        self,
        job_repository: JobRepository,
        node_repository: NodeRepository,
        scheduler: Scheduler,
    ) -> None:
        self._job_repository = job_repository
        self._node_repository = node_repository
        self._scheduler = scheduler

    def execute(
        self,
    ) -> None:
        """
        Schedule every queued job.
        """
        nodes = self._node_repository.list_available()

        for job in self._job_repository.list():
            if job.status != JobStatus.QUEUED:
                continue

            node = self._scheduler.select_node(
                job,
                nodes,
            )

            if node is None:
                continue

            node.allocate(
                job.resources,
            )

            job.assign_to(
                node.id,
            )

            self._node_repository.save(
                node,
            )

            self._job_repository.save(
                job,
            )

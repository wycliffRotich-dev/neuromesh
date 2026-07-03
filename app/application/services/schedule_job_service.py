from __future__ import annotations

from app.domain.entities.job import Job
from app.domain.entities.node import Node
from app.domain.repositories.job_repository import JobRepository
from app.domain.repositories.node_repository import NodeRepository
from app.domain.services.scheduler import Scheduler
from app.domain.value_objects.job_id import JobId


class ScheduleJobService:
    """
    Application service responsible for assigning a job
    to the most appropriate compute node.
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
        job_id: JobId,
    ) -> Node | None:
        """
        Attempt to schedule a job.

        Returns:
            The selected node if scheduling succeeds,
            otherwise None.
        """
        job = self._job_repository.get_by_id(job_id)

        if job is None:
            return None

        nodes = self._node_repository.list_available()

        return self._scheduler.select_node(
            job,
            nodes,
        )
from __future__ import annotations

from app.domain.entities.node import Node
from app.domain.repositories.job_repository import JobRepository
from app.domain.repositories.node_repository import NodeRepository
from app.domain.services.scheduler import Scheduler
from app.domain.value_objects.job_id import JobId


class ScheduleJobService:
    """
    Application service responsible for scheduling jobs
    onto compute nodes.
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
        Schedule a job onto a compute node.

        Returns:
            The selected node if scheduling succeeds,
            otherwise None.
        """
        job = self._job_repository.get_by_id(job_id)

        if job is None:
            return None

        # Move the job into the scheduling queue.
        job.queue()

        # Retrieve all registered nodes.
        nodes = self._node_repository.list()

        # Let the Domain decide which node is suitable.
        node = self._scheduler.select_node(
            job,
            nodes,
        )

        if node is None:
            return None

        # Consume node resources.
        node.allocate(job.resources)

        # Record where the job has been scheduled.
        job.assign_to(node.id)

        # Persist both updated aggregates.
        self._node_repository.save(node)
        self._job_repository.save(job)

        return node
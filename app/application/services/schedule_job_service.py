from __future__ import annotations

from app.application.services.record_job_events_service import (
    RecordJobEventsService,
)
from app.domain.entities.node import Node
from app.domain.repositories.job_repository import JobRepository
from app.domain.repositories.node_repository import NodeRepository
from app.domain.services.job_lifecycle import JobLifecycle
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
        lifecycle: JobLifecycle,
        record_job_events_service: RecordJobEventsService,
    ) -> None:
        self._job_repository = job_repository
        self._node_repository = node_repository
        self._scheduler = scheduler
        self._lifecycle = lifecycle
        self._record_job_events_service = record_job_events_service

    def execute(
        self,
        job_id: JobId,
    ) -> Node | None:
        """
        Schedule a job onto a compute node.
        """
        job = self._job_repository.get_by_id(
            job_id,
        )

        if job is None:
            return None

        self._lifecycle.queue(
            job,
        )

        nodes = self._node_repository.list()

        node = self._scheduler.select_node(
            job,
            nodes,
        )

        if node is None:
            return None

        node.allocate(
            job.resources,
        )

        self._lifecycle.schedule(
            job,
            node.id,
        )

        self._record_job_events_service.record(
            aggregate_id=str(job.id),
            aggregate_type="Job",
            event_type="JobScheduled",
        )

        self._node_repository.save(
            node,
        )

        self._job_repository.save(
            job,
        )

        return node

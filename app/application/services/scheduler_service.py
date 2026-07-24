from __future__ import annotations

from app.application.services.record_job_events_service import (
    RecordJobEventsService,
)
from app.domain.entities.job import Job
from app.domain.entities.node import Node
from app.domain.exceptions.no_available_node_error import (
    NoAvailableNodeError,
)
from app.domain.repositories.job_repository import (
    JobRepository,
)
from app.domain.repositories.node_repository import (
    NodeRepository,
)


class SchedulerService:
    """
    Select the best node for a queued job and
    reserve its resources.
    """

    def __init__(
        self,
        node_repository: NodeRepository,
        job_repository: JobRepository,
        record_job_events_service: RecordJobEventsService,
    ) -> None:
        self._node_repository = node_repository
        self._job_repository = job_repository
        self._record_job_events_service = record_job_events_service

    def execute(
        self,
        job: Job,
    ) -> Node:
        """
        Schedule one queued job.
        """
        candidates: list[tuple[int, Node]] = []

        for node in self._node_repository.list():
            if not node.is_alive():
                continue
            if node.is_draining():
                continue
            if not node.can_host(
                job.resources,
            ):
                continue

            score = (
                (
                    node.available.cpu_cores
                    - job.resources.cpu_cores
                )
                + (
                    node.available.memory_mib
                    - job.resources.memory_mib
                )
                + (
                    node.available.vram_mib
                    - job.resources.vram_mib
                )
            )

            candidates.append(
                (
                    score,
                    node,
                )
            )

        if len(candidates) == 0:
            raise NoAvailableNodeError(
                "No node has enough free resources."
            )

        candidates.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        selected = candidates[0][1]

        selected.allocate(
            job.resources,
        )

        job.assign_to(
            selected.id,
        )

        self._node_repository.save(
            selected,
        )

        self._job_repository.save(
            job,
        )

        self._record_job_events_service.record(
            aggregate_id=str(job.id),
            aggregate_type="Job",
            event_type="JobScheduled",
        )

        return selected

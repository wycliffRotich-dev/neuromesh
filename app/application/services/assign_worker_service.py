from __future__ import annotations

from app.domain.entities.job import Job
from app.domain.entities.worker import Worker
from app.domain.exceptions.no_available_node_error import (
    NoAvailableNodeError,
)
from app.domain.repositories.worker_repository import (
    WorkerRepository,
)


class AssignWorkerService:
    """
    Assigns a scheduled job to an idle worker.

    Only workers that:

    - are IDLE
    - belong to the node already selected by the scheduler

    are eligible to execute the job.
    """

    def __init__(
        self,
        worker_repository: WorkerRepository,
    ) -> None:
        self._worker_repository = worker_repository

    def execute(
        self,
        job: Job,
    ) -> Worker:
        """
        Locate an idle worker on the assigned node,
        accept the job and transition it to RUNNING.
        """
        if job.assigned_node_id is None:
            raise ValueError(
                "Job has not been assigned to a node."
            )

        for worker in self._worker_repository.list():
            if worker.node.id != job.assigned_node_id:
                continue

            if not worker.is_idle():
                continue

            worker.accept(job)
            worker.start()

            self._worker_repository.save(
                worker,
            )

            return worker

        raise NoAvailableNodeError(
            "No idle worker is available on the assigned node."
        )

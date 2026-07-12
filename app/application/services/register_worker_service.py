from __future__ import annotations

from app.domain.entities.worker import Worker
from app.domain.repositories.worker_repository import (
    WorkerRepository,
)


class RegisterWorkerService:
    """
    Registers a worker with the cluster.

    A worker starts in the STARTING state before
    transitioning to IDLE once it is ready to
    receive work.
    """

    def __init__(
        self,
        worker_repository: WorkerRepository,
    ) -> None:
        self._worker_repository = worker_repository

    def execute(
        self,
        worker: Worker,
    ) -> Worker:
        """
        Register a worker in the repository.

        Newly registered workers are transitioned
        to the IDLE state, indicating they are
        available to accept scheduled jobs.
        """
        worker.ready()

        self._worker_repository.save(
            worker,
        )

        stored_worker = self._worker_repository.get_by_id(
            worker.id,
        )

        if stored_worker is None:
            raise RuntimeError(
                "Worker disappeared after registration."
            )

        return stored_worker

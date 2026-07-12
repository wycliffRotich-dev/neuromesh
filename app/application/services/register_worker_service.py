from __future__ import annotations

from app.domain.entities.worker import Worker
from app.domain.repositories.worker_repository import (
    WorkerRepository,
)


class RegisterWorkerService:
    """
    Registers a worker with the cluster.

    Newly registered workers begin in the
    STARTING state. They transition to IDLE
    only after successfully reporting their
    first heartbeat.
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
        Persist a newly registered worker.
        """
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
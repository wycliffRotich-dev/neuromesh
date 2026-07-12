from __future__ import annotations

from app.domain.entities.worker import Worker
from app.domain.exceptions.node_not_found_error import (
    NodeNotFoundError,
)
from app.domain.repositories.worker_repository import (
    WorkerRepository,
)


class HeartbeatWorkerService:
    """
    Records worker heartbeats.

    Workers periodically report liveness to the
    control plane. Every heartbeat updates the
    worker's last_seen_at timestamp.
    """

    def __init__(
        self,
        worker_repository: WorkerRepository,
    ) -> None:
        self._worker_repository = worker_repository

    def execute(
        self,
        worker_id: str,
    ) -> Worker:
        worker = self._worker_repository.get_by_id(
            worker_id,
        )

        if worker is None:
            raise NodeNotFoundError(
                f"Worker '{worker_id}' does not exist."
            )

        worker.heartbeat()

        self._worker_repository.save(
            worker,
        )

        return worker

from __future__ import annotations

from app.domain.entities.worker import Worker
from app.domain.repositories.worker_repository import (
    WorkerRepository,
)


class ListWorkersService:
    """
    Lists all registered workers.
    """

    def __init__(
        self,
        worker_repository: WorkerRepository,
    ) -> None:
        self._worker_repository = worker_repository

    def execute(
        self,
    ) -> list[Worker]:
        """
        Return every registered worker.
        """
        return self._worker_repository.list()

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.worker import Worker
from app.domain.value_objects.worker_id import WorkerId


class WorkerRepository(ABC):
    """
    Repository contract for persisting workers.
    """

    @abstractmethod
    def save(
        self,
        worker: Worker,
    ) -> None:
        """
        Persist a worker.
        """

    @abstractmethod
    def get_by_id(
        self,
        worker_id: WorkerId,
    ) -> Worker | None:
        """
        Retrieve a worker by its identifier.
        """

    @abstractmethod
    def list(
        self,
    ) -> list[Worker]:
        """
        Return every registered worker.
        """

    @abstractmethod
    def delete(
        self,
        worker_id: WorkerId,
    ) -> None:
        """
        Remove a worker.
        """
from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.worker import Worker


class WorkerRepository(ABC):
    """
    Repository interface for Worker aggregates.
    """

    @abstractmethod
    def save(
        self,
        worker: Worker,
    ) -> None:
        """Persist a worker."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        worker_id: str,
    ) -> Worker:
        """Retrieve a worker by its identifier."""
        raise NotImplementedError

    @abstractmethod
    def list_all(
        self,
    ) -> list[Worker]:
        """Return all registered workers."""
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        worker_id: str,
    ) -> None:
        """Remove a worker."""
        raise NotImplementedError

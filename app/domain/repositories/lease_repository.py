from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.lease import Lease
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.worker_id import WorkerId


class LeaseRepository(ABC):
    """
    Repository contract for managing leases.

    A lease represents temporary ownership of a job by a
    worker. Implementations may store leases in memory,
    SQLite, PostgreSQL, or any other persistence backend.
    """

    @abstractmethod
    def save(
        self,
        lease: Lease,
    ) -> None:
        """
        Persist a lease.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_job_id(
        self,
        job_id: JobId,
    ) -> Lease | None:
        """
        Return the lease for a job.

        Returns None when no lease exists.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_worker_id(
        self,
        worker_id: WorkerId,
    ) -> Lease | None:
        """
        Return the lease owned by a worker.

        Returns None when the worker owns no lease.
        """
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
    ) -> list[Lease]:
        """
        Return all leases.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        job_id: JobId,
    ) -> None:
        """
        Remove a lease by job id.
        """
        raise NotImplementedError

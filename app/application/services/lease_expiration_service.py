from __future__ import annotations

from app.domain.repositories.job_repository import JobRepository
from app.domain.repositories.lease_repository import LeaseRepository
from app.domain.repositories.worker_repository import WorkerRepository


class LeaseExpirationService:
    """
    Releases expired worker leases.
    """

    def __init__(
        self,
        lease_repository: LeaseRepository,
        worker_repository: WorkerRepository,
        job_repository: JobRepository,
    ) -> None:
        self._lease_repository = lease_repository
        self._worker_repository = worker_repository
        self._job_repository = job_repository

    def execute(
        self,
    ) -> None:
        """
        Release every expired lease.
        """
        for lease in self._lease_repository.list():

            if not lease.is_expired():
                continue

            worker = self._worker_repository.get_by_id(
                lease.worker_id,
            )

            if worker is not None:
                worker.ready()
                self._worker_repository.save(
                    worker,
                )

            self._lease_repository.delete(
                lease.job_id,
            )

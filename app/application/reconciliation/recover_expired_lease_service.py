from __future__ import annotations

from app.domain.repositories.job_repository import (
    JobRepository,
)
from app.domain.repositories.lease_repository import (
    LeaseRepository,
)
from app.domain.repositories.worker_repository import (
    WorkerRepository,
)


class RecoverExpiredLeaseService:
    """
    Recover work abandoned by expired leases.

    This application service coordinates recovery by
    restoring workers, jobs and leases to a
    consistent state after lease expiration.
    """

    def __init__(
        self,
        worker_repository: WorkerRepository,
        job_repository: JobRepository,
        lease_repository: LeaseRepository,
    ) -> None:
        self._worker_repository = worker_repository
        self._job_repository = job_repository
        self._lease_repository = lease_repository

    def execute(
        self,
    ) -> None:
        """
        Recover every expired lease.

        Leases that have not yet expired are left untouched;
        their worker is still the legitimate owner of the job.
        """
        for lease in self._lease_repository.list():

            if not lease.is_expired():
                continue

            worker = self._worker_repository.get_by_id(
                lease.worker_id,
            )

            job = self._job_repository.get_by_id(
                lease.job_id,
            )

            if worker is not None:
                worker.recover()

                self._worker_repository.save(
                    worker,
                )

            if job is not None:
                job.unschedule()

                self._job_repository.save(
                    job,
                )

            self._lease_repository.delete(
                lease.job_id,
            )

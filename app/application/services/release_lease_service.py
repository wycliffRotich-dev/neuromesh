from __future__ import annotations

from app.domain.repositories.lease_repository import (
    LeaseRepository,
)
from app.domain.repositories.worker_repository import (
    WorkerRepository,
)
from app.domain.value_objects.worker_id import WorkerId


class ReleaseLeaseService:
    """
    Release the active lease owned by a worker.
    """

    def __init__(
        self,
        lease_repository: LeaseRepository,
        worker_repository: WorkerRepository,
    ) -> None:
        self._lease_repository = lease_repository
        self._worker_repository = worker_repository

    def execute(
        self,
        worker_id: WorkerId,
    ) -> None:
        lease = self._lease_repository.get_by_worker_id(
            worker_id,
        )

        if lease is None:
            raise ValueError(
                "Worker does not own an active lease."
            )

        worker = self._worker_repository.get_by_id(
            worker_id,
        )

        if worker is None:
            raise ValueError(
                "Worker does not exist."
            )

        worker.complete()

        self._worker_repository.save(
            worker,
        )

        self._lease_repository.delete(
            lease.job_id,
        )

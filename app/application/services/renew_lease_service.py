from __future__ import annotations

from datetime import timedelta

from app.domain.entities.lease import DEFAULT_LEASE_DURATION
from app.domain.repositories.lease_repository import (
    LeaseRepository,
)
from app.domain.value_objects.worker_id import WorkerId


class RenewLeaseService:
    """
    Extend the lifetime of a worker's active lease.

    Workers periodically renew their lease while
    executing a job. If renewal stops, the lease
    eventually expires and the scheduler can
    recover the job.
    """

    def __init__(
        self,
        lease_repository: LeaseRepository,
    ) -> None:
        self._lease_repository = lease_repository

    def execute(
        self,
        worker_id: WorkerId,
        duration: timedelta = DEFAULT_LEASE_DURATION,
    ) -> None:
        """
        Renew the worker's active lease.
        """
        lease = self._lease_repository.get_by_worker_id(
            worker_id,
        )

        if lease is None:
            raise ValueError(
                "Worker does not own an active lease."
            )

        lease.renew(
            duration,
        )

        self._lease_repository.save(
            lease,
        )

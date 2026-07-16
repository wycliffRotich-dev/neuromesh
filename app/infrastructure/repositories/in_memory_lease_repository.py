from __future__ import annotations

from app.domain.entities.lease import Lease
from app.domain.repositories.lease_repository import (
    LeaseRepository,
)
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.worker_id import WorkerId


class InMemoryLeaseRepository(
    LeaseRepository,
):
    """
    In-memory implementation of the LeaseRepository.
    """

    def __init__(
        self,
    ) -> None:
        self._leases: dict[str, Lease] = {}

    def save(
        self,
        lease: Lease,
    ) -> None:
        self._leases[
            str(lease.job_id)
        ] = lease

    def get_by_job_id(
        self,
        job_id: JobId,
    ) -> Lease | None:
        return self._leases.get(
            str(job_id),
        )

    def get_by_worker_id(
        self,
        worker_id: WorkerId,
    ) -> Lease | None:
        for lease in self._leases.values():
            if lease.worker_id == worker_id:
                return lease

        return None

    def list(
        self,
    ) -> list[Lease]:
        return list(
            self._leases.values(),
        )

    def delete(
        self,
        job_id: JobId,
    ) -> None:
        self._leases.pop(
            str(job_id),
            None,
        )

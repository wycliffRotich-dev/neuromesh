from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.worker_id import WorkerId


def utc_now() -> datetime:
    return datetime.now(UTC)


DEFAULT_LEASE_DURATION = timedelta(seconds=30)


@dataclass(slots=True)
class Lease:
    """
    Represents exclusive ownership of a job by
    a worker for a limited period of time.
    """

    id: UUID

    worker_id: WorkerId

    job_id: JobId

    acquired_at: datetime

    expires_at: datetime

    @classmethod
    def create(
        cls,
        *,
        worker_id: WorkerId,
        job_id: JobId,
        duration: timedelta = DEFAULT_LEASE_DURATION,
    ) -> "Lease":
        """
        Create a new worker lease.
        """
        acquired_at = utc_now()

        return cls(
            id=uuid4(),
            worker_id=worker_id,
            job_id=job_id,
            acquired_at=acquired_at,
            expires_at=acquired_at + duration,
        )

    def is_expired(
        self,
    ) -> bool:
        """
        Return True when the lease has expired.
        """
        return utc_now() >= self.expires_at

    def renew(
        self,
        duration: timedelta = DEFAULT_LEASE_DURATION,
    ) -> None:
        """
        Extend the lease.
        """
        self.expires_at = utc_now() + duration

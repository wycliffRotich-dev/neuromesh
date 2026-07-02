from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.enums.job_status import JobStatus
from app.domain.exceptions.invalid_job_transition import (
    InvalidJobTransition,
)
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class Job:
    id: JobId
    resources: ResourceRequirements

    status: JobStatus = JobStatus.SUBMITTED

    submitted_at: datetime = field(default_factory=utc_now)

    _ALLOWED_TRANSITIONS = {
        JobStatus.SUBMITTED: {JobStatus.QUEUED},
        JobStatus.QUEUED: {
            JobStatus.SCHEDULED,
            JobStatus.CANCELLED,
        },
        JobStatus.SCHEDULED: {
            JobStatus.RUNNING,
            JobStatus.CANCELLED,
        },
        JobStatus.RUNNING: {
            JobStatus.COMPLETED,
            JobStatus.FAILED,
        },
        JobStatus.COMPLETED: set(),
        JobStatus.FAILED: set(),
        JobStatus.CANCELLED: set(),
    }

    def _transition_to(self, new_status: JobStatus) -> None:
        allowed = self._ALLOWED_TRANSITIONS[self.status]

        if new_status not in allowed:
            raise InvalidJobTransition(
                f"Cannot transition from "
                f"{self.status.name} to "
                f"{new_status.name}."
            )

        self.status = new_status

    def queue(self) -> None:
        self._transition_to(JobStatus.QUEUED)
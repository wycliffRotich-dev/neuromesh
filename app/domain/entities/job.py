from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.enums.job_status import JobStatus
from app.domain.exceptions.invalid_job_transition import (
    InvalidJobTransition,
)
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class Job:
    """
    Represents a schedulable job in the system.
    """

    id: JobId
    resources: ResourceRequirements
    priority: int = 0
    constraints: dict[str, str] = field(
        default_factory=dict,
    )
    max_retries: int = 0
    retry_count: int = 0
    status: JobStatus = JobStatus.SUBMITTED
    assigned_node_id: NodeId | None = None
    submitted_at: datetime = field(
        default_factory=utc_now,
    )

    _ALLOWED_TRANSITIONS = {
        JobStatus.SUBMITTED: {
            JobStatus.QUEUED,
        },
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
        JobStatus.FAILED: {
            JobStatus.QUEUED,
        },
        JobStatus.CANCELLED: set(),
    }

    def __post_init__(self) -> None:
        """
        Validate that this job requests a meaningful
        amount of work.

        A job requesting zero CPU or zero memory cannot
        actually be scheduled or executed, so this is
        rejected here at job-creation time rather than
        inside ResourceRequirements itself -- that value
        object also represents remaining node capacity,
        where zero is a valid state (a fully-allocated
        node). VRAM is exempt since CPU-only jobs are
        legitimate.
        """
        if self.resources.cpu_cores <= 0:
            raise ValueError("Job must request at least one CPU core.")

        if self.resources.memory_mib <= 0:
            raise ValueError("Job must request a positive amount of memory.")

    def _transition_to(
        self,
        new_status: JobStatus,
    ) -> None:
        allowed = self._ALLOWED_TRANSITIONS[self.status]

        if new_status not in allowed:
            raise InvalidJobTransition(
                f"Cannot transition from {self.status.name} to {new_status.name}."
            )

        self.status = new_status

    def queue(self) -> None:
        self._transition_to(
            JobStatus.QUEUED,
        )

    def assign_to(
        self,
        node_id: NodeId,
    ) -> None:
        self.assigned_node_id = node_id
        self._transition_to(
            JobStatus.SCHEDULED,
        )

    def start(self) -> None:
        self._transition_to(
            JobStatus.RUNNING,
        )

    def complete(self) -> None:
        self._transition_to(
            JobStatus.COMPLETED,
        )

    def fail(self) -> None:
        self._transition_to(
            JobStatus.FAILED,
        )

    def cancel(self) -> None:
        self._transition_to(
            JobStatus.CANCELLED,
        )

    def can_retry(self) -> bool:
        """
        Return True if the job has retries remaining.
        """
        return self.retry_count < self.max_retries

    def record_retry(self) -> None:
        """
        Consume one retry attempt.
        """
        if not self.can_retry():
            raise ValueError("Job has exhausted all retries.")

        self.retry_count += 1

    def retry(self) -> None:
        """
        Retry a failed job by consuming one retry
        attempt and placing it back into the queue.
        """
        if self.status != JobStatus.FAILED:
            raise InvalidJobTransition("Only failed jobs may be retried.")

        self.record_retry()
        self.assigned_node_id = None
        self._transition_to(
            JobStatus.QUEUED,
        )

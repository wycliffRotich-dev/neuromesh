from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

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


DEFAULT_EXECUTION_TIMEOUT = timedelta(
    hours=1,
)


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

    execution_timeout: timedelta = (
        DEFAULT_EXECUTION_TIMEOUT
    )

    status: JobStatus = JobStatus.SUBMITTED

    assigned_node_id: NodeId | None = None

    submitted_at: datetime = field(
        default_factory=utc_now,
    )

    started_at: datetime | None = None

    completed_at: datetime | None = None

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
            JobStatus.QUEUED,
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

    def __post_init__(
        self,
    ) -> None:
        """
        Validate that this job requests a meaningful
        amount of work.
        """
        if self.resources.cpu_cores <= 0:
            raise ValueError(
                "Job must request at least one CPU core."
            )

        if self.resources.memory_mib <= 0:
            raise ValueError(
                "Job must request a positive amount of memory."
            )

    def _transition_to(
        self,
        new_status: JobStatus,
    ) -> None:
        allowed = self._ALLOWED_TRANSITIONS[
            self.status
        ]

        if new_status not in allowed:
            raise InvalidJobTransition(
                f"Cannot transition from {self.status.name} to {new_status.name}."
            )

        self.status = new_status

    #
    # Queries
    #

    def is_submitted(
        self,
    ) -> bool:
        return self.status is JobStatus.SUBMITTED

    def is_queued(
        self,
    ) -> bool:
        return self.status is JobStatus.QUEUED

    def is_scheduled(
        self,
    ) -> bool:
        return self.status is JobStatus.SCHEDULED

    def is_running(
        self,
    ) -> bool:
        return self.status is JobStatus.RUNNING

    def is_completed(
        self,
    ) -> bool:
        return self.status is JobStatus.COMPLETED

    def is_failed(
        self,
    ) -> bool:
        return self.status is JobStatus.FAILED

    def is_cancelled(
        self,
    ) -> bool:
        return self.status is JobStatus.CANCELLED

    def has_timed_out(
        self,
    ) -> bool:
        """
        Return True when a running job has exceeded
        its execution timeout.
        """
        if self.started_at is None:
            return False

        return (
            utc_now() - self.started_at
        ) >= self.execution_timeout

    #
    # Commands
    #

    def queue(
        self,
    ) -> None:
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

    def unschedule(
        self,
    ) -> None:
        """
        Return a scheduled job to the queue.
        """
        if not self.is_scheduled():
            raise InvalidJobTransition(
                "Only scheduled jobs may be unscheduled."
            )

        self.assigned_node_id = None

        self._transition_to(
            JobStatus.QUEUED,
        )

    def start(
        self,
    ) -> None:
        self.started_at = utc_now()

        self._transition_to(
            JobStatus.RUNNING,
        )

    def complete(
        self,
    ) -> None:
        self.completed_at = utc_now()

        self._transition_to(
            JobStatus.COMPLETED,
        )

    def fail(
        self,
    ) -> None:
        self.completed_at = utc_now()

        self._transition_to(
            JobStatus.FAILED,
        )

    def cancel(
        self,
    ) -> None:
        self._transition_to(
            JobStatus.CANCELLED,
        )

    def can_retry(
        self,
    ) -> bool:
        """
        Return True if the job has retries remaining.
        """
        return self.retry_count < self.max_retries

    def record_retry(
        self,
    ) -> None:
        """
        Consume one retry attempt.
        """
        if not self.can_retry():
            raise ValueError(
                "Job has exhausted all retries."
            )

        self.retry_count += 1

    def retry(
        self,
    ) -> None:
        """
        Retry a failed job.
        """
        if not self.is_failed():
            raise InvalidJobTransition(
                "Only failed jobs may be retried."
            )

        self.record_retry()

        self.assigned_node_id = None

        self.started_at = None
        self.completed_at = None

        self._transition_to(
            JobStatus.QUEUED,
        )

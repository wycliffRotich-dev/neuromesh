from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.entities.job import Job
from app.domain.entities.node import Node
from app.domain.enums.worker_status import WorkerStatus


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class Worker:
    """
    Represents a worker process responsible for
    executing jobs on a compute node.
    """

    id: str
    node: Node

    status: WorkerStatus = WorkerStatus.STARTING

    running_job: Job | None = None

    last_seen_at: datetime = field(
        default_factory=utc_now,
    )

    def heartbeat(self) -> None:
        """
        Record that this worker is alive.
        """
        self.last_seen_at = utc_now()

    def ready(self) -> None:
        """
        Mark this worker as ready to accept work.
        """
        self.status = WorkerStatus.IDLE

    def accept(self, job: Job) -> None:
        """
        Accept a scheduled job.
        """
        if self.status != WorkerStatus.IDLE:
            raise ValueError(
                "Worker is not accepting jobs."
            )

        if job.assigned_node_id != self.node.id:
            raise ValueError(
                "Job is assigned to another node."
            )

        self.running_job = job
        self.status = WorkerStatus.BUSY

    def start(self) -> None:
        """
        Start the assigned job.
        """
        if self.running_job is None:
            raise ValueError(
                "No assigned job."
            )

        self.running_job.start()

    def complete(self) -> None:
        """
        Complete the running job.
        """
        if self.running_job is None:
            raise ValueError(
                "No running job."
            )

        self.running_job.complete()

        self.running_job = None
        self.status = WorkerStatus.IDLE

    def fail(self) -> None:
        """
        Fail the running job.
        """
        if self.running_job is None:
            raise ValueError(
                "No running job."
            )

        self.running_job.fail()

        self.running_job = None
        self.status = WorkerStatus.IDLE

    def drain(self) -> None:
        """
        Prevent new work from being assigned.
        """
        self.status = WorkerStatus.DRAINING

from __future__ import annotations

from app.domain.entities.job import Job
from app.domain.value_objects.node_id import NodeId


class JobLifecycle:
    """
    Encapsulates valid job lifecycle transitions.

    This domain service coordinates lifecycle operations
    while leaving state validation inside the Job aggregate.
    """

    def queue(
        self,
        job: Job,
    ) -> None:
        job.queue()

    def schedule(
        self,
        job: Job,
        node_id: NodeId,
    ) -> None:
        job.assign_to(
            node_id,
        )

    def unschedule(
        self,
        job: Job,
    ) -> None:
        job.unschedule()

    def start(
        self,
        job: Job,
    ) -> None:
        job.start()

    def complete(
        self,
        job: Job,
    ) -> None:
        job.complete()

    def fail(
        self,
        job: Job,
    ) -> None:
        job.fail()

    def retry(
        self,
        job: Job,
    ) -> None:
        job.retry()

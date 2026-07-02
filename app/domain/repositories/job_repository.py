from __future__ import annotations

from typing import Protocol

from app.domain.entities.job import Job
from app.domain.value_objects.job_id import JobId


class JobRepository(Protocol):
    """
    Contract for persisting and retrieving jobs.

    Infrastructure implementations are responsible for
    storing jobs in databases or other persistence layers.
    """

    def save(self, job: Job) -> None:
        """
        Persist a job.
        """
        ...

    def get_by_id(self, job_id: JobId) -> Job | None:
        """
        Retrieve a job by its identifier.

        Returns:
            The matching Job if found, otherwise None.
        """
        ...
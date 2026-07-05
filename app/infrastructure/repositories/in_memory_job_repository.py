from __future__ import annotations

from app.domain.entities.job import Job
from app.domain.repositories.job_repository import JobRepository
from app.domain.value_objects.job_id import JobId


class InMemoryJobRepository(JobRepository):
    """
    In-memory implementation of the JobRepository.

    This repository stores jobs in memory and is intended
    for testing and local development. It should not be
    used in production.
    """

    def __init__(
        self,
        jobs: list[Job] | None = None,
    ) -> None:
        self._jobs: dict[str, Job] = {}

        if jobs is not None:
            for job in jobs:
                self.save(job)

    def save(
        self,
        job: Job,
    ) -> None:
        """
        Persist a job in memory.
        """
        self._jobs[str(job.id)] = job

    def get_by_id(
        self,
        job_id: JobId,
    ) -> Job | None:
        """
        Retrieve a job by its identifier.

        Returns:
            The matching Job if found, otherwise None.
        """
        return self._jobs.get(str(job_id))
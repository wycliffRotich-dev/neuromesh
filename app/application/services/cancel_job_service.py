from __future__ import annotations

from app.domain.entities.job import Job
from app.domain.repositories.job_repository import JobRepository
from app.domain.value_objects.job_id import JobId


class CancelJobService:
    """
    Application service responsible for cancelling
    a queued job.
    """

    def __init__(
        self,
        job_repository: JobRepository,
    ) -> None:
        self._job_repository = job_repository

    def execute(
        self,
        job_id: JobId,
    ) -> Job | None:
        """
        Cancel a queued job.

        Returns:
            The cancelled job if found,
            otherwise None.
        """
        job = self._job_repository.get_by_id(
            job_id,
        )

        if job is None:
            return None

        job.cancel()

        self._job_repository.save(
            job,
        )

        return job

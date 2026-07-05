from __future__ import annotations

from app.domain.enums.job_status import JobStatus
from app.domain.repositories.job_repository import (
    JobRepository,
)


class JobCompletionService:
    """
    Application service responsible for completing
    running jobs.
    """

    def __init__(
        self,
        job_repository: JobRepository,
    ) -> None:
        self._job_repository = job_repository

    def execute(
        self,
    ) -> None:
        """
        Complete every running job.
        """
        for job in self._job_repository.list():
            if job.status != JobStatus.RUNNING:
                continue

            job.complete()

            self._job_repository.save(
                job,
            )

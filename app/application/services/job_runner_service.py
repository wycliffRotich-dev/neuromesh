from __future__ import annotations

from app.domain.enums.job_status import JobStatus
from app.domain.repositories.job_repository import (
    JobRepository,
)


class JobRunnerService:
    """
    Application service responsible for starting
    scheduled jobs.
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
        Start every scheduled job.
        """
        for job in self._job_repository.list():
            if job.status != JobStatus.SCHEDULED:
                continue

            job.start()

            self._job_repository.save(
                job,
            )

from __future__ import annotations

from app.domain.entities.job import Job
from app.domain.repositories.job_repository import (
    JobRepository,
)


class ListQueuedJobsService:
    """
    Application service responsible for
    listing queued jobs.
    """

    def __init__(
        self,
        job_repository: JobRepository,
    ) -> None:
        self._job_repository = job_repository

    def execute(
        self,
    ) -> list[Job]:
        """
        Return all queued jobs.
        """
        return self._job_repository.list_queued()

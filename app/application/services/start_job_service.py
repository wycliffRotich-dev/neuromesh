from __future__ import annotations

from app.domain.entities.job import Job
from app.domain.exceptions.job_not_found_error import (
    JobNotFoundError,
)
from app.domain.repositories.job_repository import JobRepository
from app.domain.value_objects.job_id import JobId


class StartJobService:
    """
    Application service responsible for starting
    a scheduled job.
    """

    def __init__(
        self,
        job_repository: JobRepository,
    ) -> None:
        self._job_repository = job_repository

    def execute(
        self,
        job_id: JobId,
    ) -> Job:
        """
        Start a scheduled job.

        Raises:
            JobNotFoundError:
                If the job does not exist.
        """
        job = self._job_repository.get_by_id(job_id)

        if job is None:
            raise JobNotFoundError(job_id)

        job.start()

        self._job_repository.save(job)

        return job

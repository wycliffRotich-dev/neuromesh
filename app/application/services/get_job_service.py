from __future__ import annotations

from ...domain.exceptions.job_not_found_error import JobNotFoundError
from ...domain.entities.job import Job
from ...domain.repositories.job_repository import JobRepository
from ...domain.value_objects.job_id import JobId


class GetJobService:
    """
    Application service responsible for retrieving
    an existing job.
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
        Retrieve an existing job.

        Args:
            job_id:
                Identifier of the job to retrieve.

        Returns:
            The matching job.

        Raises:
            JobNotFoundError:
                If no job exists with the given identifier.
        """
        job = self._job_repository.get_by_id(job_id)

        if job is None:
            raise JobNotFoundError(job_id)

        return job
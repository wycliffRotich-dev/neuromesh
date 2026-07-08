from __future__ import annotations

from app.domain.entities.job import Job
from app.domain.repositories.job_repository import JobRepository
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


class CreateJobService:
    """
    Application service responsible for creating
    and persisting new jobs.
    """

    def __init__(
        self,
        job_repository: JobRepository,
    ) -> None:
        self._job_repository = job_repository

    def execute(
        self,
        resources: ResourceRequirements,
    ) -> Job:
        """
        Create and persist a new job.

        Returns:
            The newly created job.
        """
        job = Job(
            id=JobId.new(),
            resources=resources,
        )

        self._job_repository.save(job)

        return job

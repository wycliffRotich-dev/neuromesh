from __future__ import annotations

from app.application.dto.submit_job import SubmitJobRequest
from app.domain.entities.job import Job
from app.domain.repositories.job_repository import JobRepository
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


class JobService:
    """
    Application service responsible for orchestrating
    job-related use cases.

    This layer coordinates the domain model without
    containing business rules.
    """

    def __init__(
        self,
        repository: JobRepository,
    ) -> None:
        self._repository = repository

    def submit(
        self,
        request: SubmitJobRequest,
    ) -> JobId:
        """
        Create and persist a new job.

        Args:
            request:
                The data required to submit a new job.

        Returns:
            The identifier of the newly created job.
        """
        resources = ResourceRequirements(
            cpu_cores=request.cpu_cores,
            memory_mib=request.memory_mib,
            vram_mib=request.vram_mib,
        )

        job = Job(
            id=JobId.new(),
            resources=resources,
        )

        self._repository.save(job)

        return job.id
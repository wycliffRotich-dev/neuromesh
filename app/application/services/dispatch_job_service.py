from __future__ import annotations

from app.application.services.assign_worker_service import (
    AssignWorkerService,
)
from app.application.services.schedule_job_service import (
    ScheduleJobService,
)
from app.domain.repositories.job_repository import (
    JobRepository,
)
from app.domain.value_objects.job_id import JobId


class DispatchJobService:
    """
    Schedule a job and immediately dispatch it
    to an available worker.
    """

    def __init__(
        self,
        job_repository: JobRepository,
        schedule_job_service: ScheduleJobService,
        assign_worker_service: AssignWorkerService,
    ) -> None:
        self._job_repository = job_repository
        self._schedule_job_service = schedule_job_service
        self._assign_worker_service = assign_worker_service

    def execute(
        self,
        job_id: JobId,
    ) -> None:
        """
        Dispatch a submitted job.
        """
        job = self._job_repository.get_by_id(
            job_id,
        )

        if job is None:
            raise ValueError(
                "Job does not exist."
            )

        self._schedule_job_service.execute(
            job.id,
        )

        job = self._job_repository.get_by_id(
            job.id,
        )

        if job is None:
            raise ValueError(
                "Job disappeared after scheduling."
            )

        self._assign_worker_service.execute(
            job,
        )

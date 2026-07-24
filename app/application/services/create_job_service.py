from __future__ import annotations

from app.application.services.record_job_events_service import (
    RecordJobEventsService,
)
from app.application.services.scheduler_service import (
    SchedulerService,
)
from app.domain.entities.job import Job
from app.domain.exceptions.no_available_node_error import (
    NoAvailableNodeError,
)
from app.domain.repositories.job_repository import (
    JobRepository,
)
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


class CreateJobService:
    """
    Creates a job and immediately attempts scheduling.
    """

    def __init__(
        self,
        job_repository: JobRepository,
        scheduler_service: SchedulerService,
        record_job_events_service: RecordJobEventsService,
    ) -> None:
        self._job_repository = job_repository
        self._scheduler_service = scheduler_service
        self._record_job_events_service = record_job_events_service

    def execute(
        self,
        resources: ResourceRequirements,
    ) -> Job:
        job = Job(
            id=JobId.new(),
            resources=resources,
        )

        job.queue()

        self._job_repository.save(
            job,
        )

        self._record_job_events_service.record(
            aggregate_id=str(job.id),
            aggregate_type="Job",
            event_type="JobCreated",
        )

        try:
            self._scheduler_service.execute(
                job,
            )
        except NoAvailableNodeError:
            # No node currently has enough capacity.
            # Leave the job queued.
            pass

        stored_job = self._job_repository.get_by_id(
            job.id,
        )

        if stored_job is None:
            raise RuntimeError(
                "Job disappeared after being saved."
            )

        return stored_job

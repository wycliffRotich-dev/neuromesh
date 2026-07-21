from app.application.services.record_job_events_service import (
    RecordJobEventsService,
)
from app.application.services.schedule_job_service import (
    ScheduleJobService,
)
from app.domain.entities.job import Job
from app.domain.entities.node import Node
from app.domain.enums.job_status import JobStatus
from app.domain.services.job_lifecycle import JobLifecycle
from app.domain.services.scheduler import Scheduler
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.infrastructure.repositories.in_memory_event_repository import (
    InMemoryEventRepository,
)
from app.infrastructure.repositories.in_memory_job_repository import (
    InMemoryJobRepository,
)
from app.infrastructure.repositories.in_memory_node_repository import (
    InMemoryNodeRepository,
)


def test_schedule_job_service_schedules_a_job() -> None:
    resources = ResourceRequirements(
        cpu_cores=4,
        memory_mib=4096,
        vram_mib=2048,
    )

    job = Job(
        id=JobId.new(),
        resources=resources,
    )

    node = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=16,
            memory_mib=32768,
            vram_mib=16384,
        ),
    )

    job_repository = InMemoryJobRepository()

    job_repository.save(
        job,
    )

    node_repository = InMemoryNodeRepository(
        [
            node,
        ],
    )

    event_repository = InMemoryEventRepository()

    record_job_events_service = RecordJobEventsService(
        event_repository=event_repository,
    )

    service = ScheduleJobService(
        job_repository=job_repository,
        node_repository=node_repository,
        scheduler=Scheduler(),
        lifecycle=JobLifecycle(),
        record_job_events_service=record_job_events_service,
    )

    selected = service.execute(
        job.id,
    )

    assert selected == node
    assert job.assigned_node_id == node.id
    assert job.status == JobStatus.SCHEDULED

    events = event_repository.list_by_aggregate(
        str(job.id),
    )

    assert len(events) == 1
    assert events[0].event_type == "JobScheduled"

from __future__ import annotations

from app.application.services.create_job_service import (
    CreateJobService,
)
from app.application.services.record_job_events_service import (
    RecordJobEventsService,
)
from app.application.services.scheduler_service import (
    SchedulerService,
)
from app.domain.entities.job import Job
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


def test_create_job_service_creates_and_persists_job() -> None:
    """
    Creating a job should persist it even when no
    compute nodes are currently available.
    """
    job_repository = InMemoryJobRepository()
    node_repository = InMemoryNodeRepository()
    event_repository = InMemoryEventRepository()

    record_job_events_service = RecordJobEventsService(
        event_repository=event_repository,
    )

    scheduler_service = SchedulerService(
        job_repository=job_repository,
        node_repository=node_repository,
        record_job_events_service=record_job_events_service,
    )

    service = CreateJobService(
        job_repository=job_repository,
        scheduler_service=scheduler_service,
        record_job_events_service=record_job_events_service,
    )

    resources = ResourceRequirements(
        cpu_cores=4,
        memory_mib=8192,
        vram_mib=2048,
    )

    job = service.execute(resources)

    assert isinstance(job, Job)

    stored = job_repository.get_by_id(job.id)
    assert stored is not None
    assert stored.id == job.id
    assert stored.resources == resources


def test_create_job_service_records_job_created_event() -> None:
    """
    Creating a job must record a JobCreated event, even
    when no node is available to schedule it onto -- event
    recording and scheduling are independent concerns, and
    a job that never gets scheduled should still show up in
    a live event feed as having been created.
    """
    job_repository = InMemoryJobRepository()
    node_repository = InMemoryNodeRepository()
    event_repository = InMemoryEventRepository()

    record_job_events_service = RecordJobEventsService(
        event_repository=event_repository,
    )

    scheduler_service = SchedulerService(
        job_repository=job_repository,
        node_repository=node_repository,
        record_job_events_service=record_job_events_service,
    )

    service = CreateJobService(
        job_repository=job_repository,
        scheduler_service=scheduler_service,
        record_job_events_service=record_job_events_service,
    )

    resources = ResourceRequirements(
        cpu_cores=4,
        memory_mib=8192,
        vram_mib=2048,
    )

    job = service.execute(resources)

    events = event_repository.list_by_aggregate(
        str(job.id),
    )

    event_types = [event.event_type for event in events]

    assert "JobCreated" in event_types

    # No node exists in this test, so scheduling must fail
    # silently; JobScheduled must NOT be recorded.
    assert "JobScheduled" not in event_types


def test_create_job_service_records_both_events_when_node_available() -> (
    None
):
    """
    When a node is available and scheduling succeeds, both
    JobCreated and JobScheduled must be recorded, in that
    order, reflecting the real sequence of what happened.
    """
    from app.domain.entities.node import Node
    from app.domain.value_objects.node_id import NodeId

    job_repository = InMemoryJobRepository()
    node_repository = InMemoryNodeRepository()
    event_repository = InMemoryEventRepository()

    node = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=8,
            memory_mib=16384,
            vram_mib=8192,
        ),
    )
    node_repository.save(node)

    record_job_events_service = RecordJobEventsService(
        event_repository=event_repository,
    )

    scheduler_service = SchedulerService(
        job_repository=job_repository,
        node_repository=node_repository,
        record_job_events_service=record_job_events_service,
    )

    service = CreateJobService(
        job_repository=job_repository,
        scheduler_service=scheduler_service,
        record_job_events_service=record_job_events_service,
    )

    resources = ResourceRequirements(
        cpu_cores=1,
        memory_mib=512,
        vram_mib=0,
    )

    job = service.execute(resources)

    events = event_repository.list_by_aggregate(
        str(job.id),
    )

    event_types = [event.event_type for event in events]

    assert event_types == ["JobCreated", "JobScheduled"]

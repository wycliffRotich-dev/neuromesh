from datetime import UTC, datetime, timedelta

from app.application.services.reschedule_jobs_service import (
    RescheduleJobsService,
)
from app.domain.entities.job import Job
from app.domain.entities.node import Node
from app.domain.enums.job_status import JobStatus
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.infrastructure.repositories.in_memory_job_repository import (
    InMemoryJobRepository,
)
from app.infrastructure.repositories.in_memory_node_repository import (
    InMemoryNodeRepository,
)


def test_reschedule_jobs_from_offline_node() -> None:
    """
    Jobs assigned to an offline node should
    return to the QUEUED state.
    """

    node = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=8,
            memory_mib=16384,
            vram_mib=8192,
        ),
    )

    node.last_seen_at = (
        datetime.now(UTC)
        - timedelta(minutes=2)
    )

    job = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=2,
            memory_mib=2048,
            vram_mib=1024,
        ),
    )

    job.queue()
    job.assign_to(node.id)

    job_repository = InMemoryJobRepository()
    job_repository.save(job)

    node_repository = InMemoryNodeRepository(
        [
            node,
        ],
    )

    service = RescheduleJobsService(
        job_repository,
        node_repository,
    )

    service.execute()

    assert job.status == JobStatus.QUEUED
    assert job.assigned_node_id is None

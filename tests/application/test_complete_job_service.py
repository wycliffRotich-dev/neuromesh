from __future__ import annotations

from app.application.services.complete_job_service import (
    CompleteJobService,
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


def test_complete_job_service_completes_job() -> None:
    # 1. Instantiate the domain entity safely using its native dataclass fields
    node = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=8,
            memory_mib=16384,
            vram_mib=4096,
        ),
    )

    # 2. Seed the repository through the constructor as your code specifies
    node_repository = InMemoryNodeRepository(nodes=[node])
    job_repository = InMemoryJobRepository()

    job = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=4,
            memory_mib=8192,
            vram_mib=2048,
        ),
    )

    # 3. Follow your exact strict FSM state transitions to reach a valid running state
    job.queue()
    job.assign_to(node.id)
    node.allocate(job.resources)
    job.start()

    # 4. Persist the valid job aggregate
    job_repository.save(job)

    service = CompleteJobService(
        job_repository=job_repository,
        node_repository=node_repository,
    )

    completed = service.execute(job.id)

    assert completed is job
    assert completed.status == JobStatus.COMPLETED


def test_complete_job_service_returns_none_when_job_does_not_exist() -> None:
    job_repository = InMemoryJobRepository()
    node_repository = InMemoryNodeRepository()

    service = CompleteJobService(
        job_repository=job_repository,
        node_repository=node_repository,
    )

    result = service.execute(JobId.new())

    assert result is None


def test_complete_job_service_returns_none_when_job_has_no_assigned_node() -> None:
    job_repository = InMemoryJobRepository()
    node_repository = InMemoryNodeRepository()

    job = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=4,
            memory_mib=8192,
            vram_mib=2048,
        ),
    )
    job_repository.save(job)

    service = CompleteJobService(
        job_repository=job_repository,
        node_repository=node_repository,
    )

    result = service.execute(job.id)

    assert result is None


def test_complete_job_service_returns_none_when_node_does_not_exist() -> None:
    job_repository = InMemoryJobRepository()
    node_repository = InMemoryNodeRepository()

    job = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=4,
            memory_mib=8192,
            vram_mib=2048,
        ),
    )

    # Transition to an assigned state using an unmapped NodeId boundary
    job.queue()
    fake_node_id = NodeId.new()
    job.assign_to(fake_node_id)

    job_repository.save(job)

    service = CompleteJobService(
        job_repository=job_repository,
        node_repository=node_repository,
    )

    result = service.execute(job.id)

    assert result is None

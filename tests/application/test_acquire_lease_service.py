from app.application.services.acquire_lease_service import (
    AcquireLeaseService,
)
from app.domain.entities.job import Job
from app.domain.entities.node import Node
from app.domain.entities.worker import Worker
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.domain.value_objects.worker_id import WorkerId
from app.infrastructure.repositories.in_memory_lease_repository import (
    InMemoryLeaseRepository,
)


def test_worker_can_acquire_job_lease() -> None:
    node = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=4,
            memory_mib=4096,
            vram_mib=0,
        ),
    )

    worker = Worker(
        id=WorkerId.new(),
        node=node,
    )

    job = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=1,
            memory_mib=512,
            vram_mib=0,
        ),
    )

    repository = InMemoryLeaseRepository()

    service = AcquireLeaseService(
        repository,
    )

    lease = service.execute(
        worker,
        job,
    )

    assert lease.worker_id == worker.id
    assert lease.job_id == job.id
    assert repository.get_by_job_id(job.id) is not None

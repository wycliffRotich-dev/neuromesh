from datetime import timedelta

from app.application.services.lease_expiration_service import (
    LeaseExpirationService,
)
from app.domain.entities.job import Job
from app.domain.entities.lease import Lease
from app.domain.entities.node import Node
from app.domain.entities.worker import Worker
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.domain.value_objects.worker_id import WorkerId
from app.infrastructure.repositories.in_memory_job_repository import (
    InMemoryJobRepository,
)
from app.infrastructure.repositories.in_memory_lease_repository import (
    InMemoryLeaseRepository,
)
from app.infrastructure.repositories.in_memory_worker_repository import (
    InMemoryWorkerRepository,
)


def test_execute_releases_expired_lease() -> None:
    node = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=8,
            memory_mib=16384,
            vram_mib=0,
        ),
    )

    worker = Worker(
        id=WorkerId.new(),
        node=node,
    )
    worker.ready()

    job = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=1,
            memory_mib=512,
            vram_mib=0,
        ),
    )

    lease = Lease.create(
        worker_id=worker.id,
        job_id=job.id,
        duration=timedelta(seconds=-1),
    )

    worker_repository = InMemoryWorkerRepository(
        [
            worker,
        ],
    )

    lease_repository = InMemoryLeaseRepository()

    lease_repository.save(
        lease,
    )

    job_repository = InMemoryJobRepository(
        [
            job,
        ],
    )

    service = LeaseExpirationService(
        lease_repository=lease_repository,
        worker_repository=worker_repository,
        job_repository=job_repository,
    )

    service.execute()

    assert (
        lease_repository.get_by_job_id(
            job.id,
        )
        is None
    )

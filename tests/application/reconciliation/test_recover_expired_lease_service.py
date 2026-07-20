from app.application.reconciliation.recover_expired_lease_service import (
    RecoverExpiredLeaseService,
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


def test_recover_expired_lease_recovers_job() -> None:
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

    job.queue()

    job.assign_to(
        node.id,
    )

    worker.accept(
        job,
    )

    lease = Lease.create(
        worker_id=worker.id,
        job_id=job.id,
    )

    worker_repository = InMemoryWorkerRepository(
        [
            worker,
        ],
    )

    job_repository = InMemoryJobRepository(
        [
            job,
        ],
    )

    lease_repository = InMemoryLeaseRepository()

    lease_repository.save(
        lease,
    )

    service = RecoverExpiredLeaseService(
        worker_repository=worker_repository,
        job_repository=job_repository,
        lease_repository=lease_repository,
    )

    service.execute()

    recovered_worker = worker_repository.get_by_id(
        worker.id,
    )

    recovered_job = job_repository.get_by_id(
        job.id,
    )

    assert recovered_worker is not None
    assert recovered_worker.is_idle()

    assert recovered_job is not None
    assert recovered_job.is_queued()

    assert (
        lease_repository.get_by_worker_id(
            worker.id,
        )
        is None
    )


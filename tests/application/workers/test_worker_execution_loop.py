from app.application.services.release_lease_service import (
    ReleaseLeaseService,
)
from app.application.services.renew_lease_service import (
    RenewLeaseService,
)
from app.application.workers.worker_execution_loop import (
    WorkerExecutionLoop,
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
from app.infrastructure.repositories.in_memory_lease_repository import (
    InMemoryLeaseRepository,
)
from app.infrastructure.repositories.in_memory_worker_repository import (
    InMemoryWorkerRepository,
)


def test_run_once_executes_assigned_job() -> None:
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

    # Respect the state machine
    job.queue()
    job.assign_to(node.id)

    worker.accept(job)

    lease = Lease.create(
        worker_id=worker.id,
        job_id=job.id,
    )

    lease_repository = InMemoryLeaseRepository()
    lease_repository.save(lease)

    worker_repository = InMemoryWorkerRepository(
        [
            worker,
        ],
    )

    renew_lease_service = RenewLeaseService(
        lease_repository=lease_repository,
    )

    release_lease_service = ReleaseLeaseService(
        lease_repository=lease_repository,
        worker_repository=worker_repository,
    )

    loop = WorkerExecutionLoop(
        worker_repository=worker_repository,
        renew_lease_service=renew_lease_service,
        release_lease_service=release_lease_service,
    )

    loop.execute(
        worker.id,
    )

    saved_worker = worker_repository.get_by_id(
        worker.id,
    )

    assert saved_worker is not None
    assert saved_worker.is_idle()
    assert saved_worker.running_job is None

    assert (
        lease_repository.get_by_worker_id(
            worker.id,
        )
        is None
    )

from app.application.services.acquire_lease_service import (
    AcquireLeaseService,
)
from app.application.services.assign_worker_service import (
    AssignWorkerService,
)
from app.application.services.dispatch_job_service import (
    DispatchJobService,
)
from app.application.services.schedule_job_service import (
    ScheduleJobService,
)
from app.domain.entities.job import Job
from app.domain.entities.node import Node
from app.domain.entities.worker import Worker
from app.domain.enums.job_status import (
    JobStatus,
)
from app.domain.services.scheduler import (
    Scheduler,
)
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
from app.infrastructure.repositories.in_memory_node_repository import (
    InMemoryNodeRepository,
)
from app.infrastructure.repositories.in_memory_worker_repository import (
    InMemoryWorkerRepository,
)


def test_execute_dispatches_job() -> None:
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

    job_repository = InMemoryJobRepository(
        [
            job,
        ],
    )

    node_repository = InMemoryNodeRepository(
        [
            node,
        ],
    )

    worker_repository = InMemoryWorkerRepository(
        [
            worker,
        ],
    )

    lease_repository = InMemoryLeaseRepository()

    scheduler = Scheduler()

    acquire_lease_service = AcquireLeaseService(
        lease_repository=lease_repository,
    )

    schedule_job_service = ScheduleJobService(
        job_repository=job_repository,
        node_repository=node_repository,
        scheduler=scheduler,
    )

    assign_worker_service = AssignWorkerService(
        worker_repository=worker_repository,
        acquire_lease_service=acquire_lease_service,
    )

    service = DispatchJobService(
        job_repository=job_repository,
        schedule_job_service=schedule_job_service,
        assign_worker_service=assign_worker_service,
    )

    service.execute(
        job.id,
    )

    saved_job = job_repository.get_by_id(
        job.id,
    )

    assert saved_job is not None
    assert saved_job.status is JobStatus.RUNNING

    saved_worker = worker_repository.get_by_id(
        worker.id,
    )

    assert saved_worker is not None
    assert saved_worker.running_job is not None

    lease = lease_repository.get_by_job_id(
        job.id,
    )

    assert lease is not None

from __future__ import annotations

from app.application.services.job_execution_service import (
    JobExecutionService,
)
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
from app.infrastructure.repositories.in_memory_job_repository import (
    InMemoryJobRepository,
)
from app.infrastructure.repositories.in_memory_lease_repository import (
    InMemoryLeaseRepository,
)
from app.infrastructure.repositories.in_memory_worker_repository import (
    InMemoryWorkerRepository,
)


def _make_worker_and_job(
    command: list[str] | None = None,
) -> tuple[Worker, Job]:
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
        command=command,
    )

    # Respect the state machine
    job.queue()
    job.assign_to(node.id)

    worker.accept(job)

    return worker, job


def _build_loop(
    worker: Worker,
    job: Job,
) -> tuple[
    WorkerExecutionLoop,
    InMemoryWorkerRepository,
    InMemoryJobRepository,
    InMemoryLeaseRepository,
]:
    lease = Lease.create(
        worker_id=worker.id,
        job_id=job.id,
    )

    lease_repository = InMemoryLeaseRepository()
    lease_repository.save(lease)

    worker_repository = InMemoryWorkerRepository([worker])
    job_repository = InMemoryJobRepository([job])

    renew_lease_service = RenewLeaseService(
        lease_repository=lease_repository,
    )

    release_lease_service = ReleaseLeaseService(
        lease_repository=lease_repository,
        worker_repository=worker_repository,
    )

    job_execution_service = JobExecutionService()

    loop = WorkerExecutionLoop(
        worker_repository=worker_repository,
        job_repository=job_repository,
        renew_lease_service=renew_lease_service,
        release_lease_service=release_lease_service,
        job_execution_service=job_execution_service,
    )

    return loop, worker_repository, job_repository, lease_repository


def test_run_once_with_no_command_completes_successfully() -> None:
    """
    A job with no command (today's API default) is treated
    as an immediate no-op success, matching
    JobExecutionService's own behavior for command=None.
    """
    worker, job = _make_worker_and_job()

    loop, worker_repository, job_repository, lease_repository = (
        _build_loop(worker, job)
    )

    loop.execute(worker.id)

    saved_worker = worker_repository.get_by_id(worker.id)
    saved_job = job_repository.get_by_id(job.id)

    assert saved_worker is not None
    assert saved_worker.is_idle()
    assert saved_worker.running_job is None

    assert saved_job is not None
    assert saved_job.is_completed()
    assert saved_job.exit_code == 0

    assert lease_repository.get_by_worker_id(worker.id) is None


def test_run_once_executes_real_successful_command() -> None:
    """
    Proves this is real subprocess execution, not simulated:
    the job's command actually runs, and its real exit code
    flows through to the persisted job.
    """
    worker, job = _make_worker_and_job(
        command=["python3", "-c", "pass"],
    )

    loop, worker_repository, job_repository, lease_repository = (
        _build_loop(worker, job)
    )

    loop.execute(worker.id)

    saved_worker = worker_repository.get_by_id(worker.id)
    saved_job = job_repository.get_by_id(job.id)

    assert saved_worker is not None
    assert saved_worker.is_idle()

    assert saved_job is not None
    assert saved_job.is_completed()
    assert saved_job.exit_code == 0

    assert lease_repository.get_by_worker_id(worker.id) is None


def test_run_once_marks_job_and_worker_failed_on_nonzero_exit() -> None:
    """
    A command that genuinely fails must result in the job
    being marked FAILED with its real exit code, not
    COMPLETED. This is the path that did not exist at all
    before this loop actually ran real commands.
    """
    worker, job = _make_worker_and_job(
        command=["python3", "-c", "import sys; sys.exit(7)"],
    )

    loop, worker_repository, job_repository, lease_repository = (
        _build_loop(worker, job)
    )

    loop.execute(worker.id)

    saved_worker = worker_repository.get_by_id(worker.id)
    saved_job = job_repository.get_by_id(job.id)

    assert saved_worker is not None
    assert saved_worker.is_idle()

    assert saved_job is not None
    assert saved_job.is_failed()
    assert saved_job.exit_code == 7

    # The lease must still be released even though the job
    # failed -- outcome and lease lifecycle are independent.
    assert lease_repository.get_by_worker_id(worker.id) is None


def test_run_once_marks_job_failed_when_command_exceeds_timeout() -> None:
    """
    A command that runs past the job's execution_timeout
    must be killed and marked FAILED, with the timeout
    itself enforced by real subprocess termination, not a
    simulated clock.
    """
    from datetime import timedelta

    worker, job = _make_worker_and_job(
        command=["python3", "-c", "import time; time.sleep(30)"],
    )
    job.execution_timeout = timedelta(seconds=0.5)

    loop, worker_repository, job_repository, lease_repository = (
        _build_loop(worker, job)
    )

    loop.execute(worker.id)

    saved_worker = worker_repository.get_by_id(worker.id)
    saved_job = job_repository.get_by_id(job.id)

    assert saved_worker is not None
    assert saved_worker.is_idle()

    assert saved_job is not None
    assert saved_job.is_failed()

    assert lease_repository.get_by_worker_id(worker.id) is None


def test_run_once_returns_early_when_worker_has_no_running_job() -> None:
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

    worker_repository = InMemoryWorkerRepository([worker])
    job_repository = InMemoryJobRepository()
    lease_repository = InMemoryLeaseRepository()

    loop = WorkerExecutionLoop(
        worker_repository=worker_repository,
        job_repository=job_repository,
        renew_lease_service=RenewLeaseService(
            lease_repository=lease_repository,
        ),
        release_lease_service=ReleaseLeaseService(
            lease_repository=lease_repository,
            worker_repository=worker_repository,
        ),
        job_execution_service=JobExecutionService(),
    )

    # Should return without error and without attempting to
    # renew or release a lease that was never acquired.
    loop.execute(worker.id)

    saved_worker = worker_repository.get_by_id(worker.id)
    assert saved_worker is not None
    assert saved_worker.is_idle()

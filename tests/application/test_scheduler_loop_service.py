from app.application.services.scheduler_loop_service import (
    SchedulerLoopService,
)
from app.domain.entities.job import Job
from app.domain.entities.node import Node
from app.domain.enums.job_status import JobStatus
from app.domain.services.scheduler import Scheduler
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


def test_scheduler_loop_schedules_queued_jobs() -> None:
    """
    Queued jobs should automatically be scheduled
    onto healthy compute nodes.
    """

    node = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=16,
            memory_mib=32768,
            vram_mib=16384,
        ),
    )

    job = Job(
        id=JobId.new(),
        resources=ResourceRequirements(
            cpu_cores=4,
            memory_mib=4096,
            vram_mib=2048,
        ),
    )

    job.queue()

    jobs = InMemoryJobRepository([job])
    nodes = InMemoryNodeRepository([node])

    service = SchedulerLoopService(
        jobs,
        nodes,
        Scheduler(),
    )

    service.execute()

    assert job.status == JobStatus.SCHEDULED
    assert job.assigned_node_id == node.id

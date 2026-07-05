from app.application.services.fail_job_service import (
    FailJobService,
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


def test_fail_job_service_marks_running_job_as_failed() -> None:
    """
    A running job can transition to FAILED and
    release the resources allocated on its node.
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
    job.assign_to(node.id)

    node.allocate(
        job.resources,
    )

    job.start()

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

    service = FailJobService(
        job_repository,
        node_repository,
    )

    service.execute(
        job.id,
    )

    assert job.status == JobStatus.FAILED

    assert node.available == node.capacity

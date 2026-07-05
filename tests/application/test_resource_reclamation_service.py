from app.application.services.resource_reclamation_service import (
    ResourceReclamationService,
)
from app.domain.entities.job import Job
from app.domain.entities.node import Node
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


def test_completed_jobs_release_node_resources() -> None:
    """
    Completed jobs should release
    allocated node resources.
    """

    node = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=8,
            memory_mib=8192,
            vram_mib=4096,
        ),
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

    node.allocate(job.resources)

    job.start()
    job.complete()

    jobs = InMemoryJobRepository([job])
    nodes = InMemoryNodeRepository([node])

    service = ResourceReclamationService(
        jobs,
        nodes,
    )

    service.execute()

    assert node.available == node.capacity

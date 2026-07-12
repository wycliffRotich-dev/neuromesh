from app.application.services.create_worker_service import (
    CreateWorkerService,
)
from app.domain.entities.node import Node
from app.domain.entities.worker import Worker
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.infrastructure.repositories.in_memory_worker_repository import (
    InMemoryWorkerRepository,
)


def test_create_worker_service_creates_and_persists_worker() -> None:
    repository = InMemoryWorkerRepository()

    service = CreateWorkerService(
        worker_repository=repository,
    )

    node = Node(
        id=NodeId("node-1"),
        capacity=ResourceRequirements(
            cpu_cores=8,
            memory_mib=16384,
            vram_mib=0,
        ),
    )

    worker = service.execute(
        node=node,
    )

    assert isinstance(
        worker,
        Worker,
    )

    stored = repository.get_by_id(
        worker.id,
    )

    assert stored is worker
    assert stored.node is node

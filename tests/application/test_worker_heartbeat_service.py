from app.application.services.worker_heartbeat_service import (
    WorkerHeartbeatService,
)
from app.domain.entities.node import Node
from app.domain.entities.worker import Worker
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.domain.value_objects.worker_id import WorkerId
from app.infrastructure.repositories.in_memory_worker_repository import (
    InMemoryWorkerRepository,
)


def test_execute_refreshes_worker_heartbeat() -> None:
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

    repository = InMemoryWorkerRepository(
        [
            worker,
        ],
    )

    original = worker.last_seen_at

    service = WorkerHeartbeatService(
        repository,
    )

    service.execute(
        worker.id,
    )

    stored_worker = repository.get_by_id(
        worker.id,
    )

    assert stored_worker is not None
    assert stored_worker.last_seen_at > original

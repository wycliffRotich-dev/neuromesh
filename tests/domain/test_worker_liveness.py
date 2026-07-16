from __future__ import annotations

from datetime import timedelta

from app.domain.entities.node import Node
from app.domain.entities.worker import (
    HEARTBEAT_TIMEOUT,
    Worker,
    utc_now,
)
from app.domain.enums.worker_status import WorkerStatus
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.domain.value_objects.worker_id import WorkerId


def create_worker() -> Worker:
    node = Node(
        id=NodeId.new(),
        capacity=ResourceRequirements(
            cpu_cores=8,
            memory_mib=16384,
            vram_mib=8192,
        ),
    )

    return Worker(
        id=WorkerId.new(),
        node=node,
    )


def test_worker_is_alive_by_default() -> None:
    worker = create_worker()

    assert worker.is_alive()


def test_worker_becomes_offline_after_heartbeat_timeout() -> None:
    worker = create_worker()

    worker.last_seen_at = (
        utc_now()
        - HEARTBEAT_TIMEOUT
        - timedelta(seconds=1)
    )

    assert not worker.is_alive()


def test_offline_transitions_worker_to_offline_status() -> None:
    worker = create_worker()

    worker.offline()

    assert worker.status is WorkerStatus.OFFLINE

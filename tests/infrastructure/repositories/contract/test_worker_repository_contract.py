from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.node import Node
from app.domain.entities.worker import Worker
from app.domain.repositories.worker_repository import WorkerRepository
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


class WorkerRepositoryContract(ABC):
    """
    Contract test suite for every WorkerRepository implementation.
    """

    @abstractmethod
    def repository(
        self,
    ) -> WorkerRepository:
        """
        Return a fresh repository instance.
        """

    def test_save_and_get_by_id(self) -> None:
        repository = self.repository()

        node = Node(
            id=NodeId("node-1"),
            capacity=ResourceRequirements(
                cpu_cores=8,
                memory_mib=16000,
                vram_mib=0,
            ),
        )

        worker = Worker(
            id="worker-1",
            node=node,
        )

        repository.save(
            worker,
        )

        stored = repository.get_by_id(
            "worker-1",
        )

        assert stored is worker

    def test_list_workers(self) -> None:
        repository = self.repository()

        node = Node(
            id=NodeId("node-1"),
            capacity=ResourceRequirements(
                cpu_cores=8,
                memory_mib=16000,
                vram_mib=0,
            ),
        )

        worker = Worker(
            id="worker-1",
            node=node,
        )

        repository.save(
            worker,
        )

        workers = repository.list()

        assert worker in workers
        assert len(workers) == 1

    def test_remove_worker(self) -> None:
        repository = self.repository()

        node = Node(
            id=NodeId("node-1"),
            capacity=ResourceRequirements(
                cpu_cores=8,
                memory_mib=16000,
                vram_mib=0,
            ),
        )

        worker = Worker(
            id="worker-1",
            node=node,
        )

        repository.save(
            worker,
        )

        repository.delete(
            "worker-1",
        )

        assert repository.get_by_id(
            "worker-1",
        ) is None

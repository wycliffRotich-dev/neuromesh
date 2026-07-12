from __future__ import annotations

from app.domain.repositories.worker_repository import (
    WorkerRepository,
)
from app.infrastructure.repositories.in_memory_worker_repository import (
    InMemoryWorkerRepository,
)
from tests.infrastructure.repositories.contract.test_worker_repository_contract import (
    WorkerRepositoryContract,
)


class TestInMemoryWorkerRepositoryContract(
    WorkerRepositoryContract,
):
    """
    Verify that the in-memory repository satisfies
    the WorkerRepository contract.
    """

    def repository(
        self,
    ) -> WorkerRepository:
        return InMemoryWorkerRepository()

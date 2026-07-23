from __future__ import annotations

import os

import pytest
from psycopg_pool import ConnectionPool

from app.infrastructure.repositories.postgres_node_repository import (
    PostgresNodeRepository,
)
from app.infrastructure.repositories.postgres_worker_repository import (
    PostgresWorkerRepository,
)
from tests.infrastructure.repositories.contract.test_worker_repository_contract import (
    WorkerRepositoryContract,
)

TEST_DATABASE_URL = os.environ.get(
    "NEUROMESH_TEST_DATABASE_URL",
    "postgresql://neuromesh:neuromesh@localhost:5432/neuromesh_test",
)


@pytest.fixture(scope="session")
def pool():
    test_pool = ConnectionPool(
        TEST_DATABASE_URL,
        min_size=1,
        max_size=5,
        open=True,
        kwargs={"autocommit": True},
    )
    yield test_pool
    test_pool.close()


class TestPostgresWorkerRepositoryContract(WorkerRepositoryContract):
    @pytest.fixture
    def repository(self, pool):
        with pool.connection() as conn:
            conn.execute("TRUNCATE workers, nodes CASCADE")

        node_repository = PostgresNodeRepository(pool)
        worker_repository = PostgresWorkerRepository(pool)

        original_make_worker = self._make_worker

        def _make_worker_and_persist_node():
            worker = original_make_worker()
            node_repository.save(worker.node)
            return worker

        self._make_worker = _make_worker_and_persist_node

        return worker_repository

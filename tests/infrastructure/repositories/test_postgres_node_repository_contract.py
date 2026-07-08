from __future__ import annotations

import os

import pytest
from psycopg_pool import ConnectionPool

from app.infrastructure.repositories.postgres_node_repository import (
    PostgresNodeRepository,
)
from tests.infrastructure.repositories.contract.node_repository_contract import (
    NodeRepositoryContract,
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
        kwargs={"autocommit": True},
    )
    yield test_pool
    test_pool.close()


class TestPostgresNodeRepositoryContract(NodeRepositoryContract):
    @pytest.fixture
    def repository(self, pool):
        with pool.connection() as conn:
            conn.execute("TRUNCATE nodes CASCADE")
        return PostgresNodeRepository(pool)
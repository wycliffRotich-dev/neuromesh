from __future__ import annotations

import pytest

from app.infrastructure.repositories.in_memory_node_repository import (
    InMemoryNodeRepository,
)
from tests.infrastructure.repositories.contract.node_repository_contract import (
    NodeRepositoryContract,
)


class TestInMemoryNodeRepositoryContract(NodeRepositoryContract):
    @pytest.fixture
    def repository(self):
        return InMemoryNodeRepository()

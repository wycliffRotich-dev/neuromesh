from __future__ import annotations

import pytest

from app.infrastructure.repositories.in_memory_lease_repository import (
    InMemoryLeaseRepository,
)
from tests.infrastructure.repositories.contract.lease_repository_contract import (
    LeaseRepositoryContract,
)


class TestInMemoryLeaseRepositoryContract(
    LeaseRepositoryContract,
):
    """
    Verify the in-memory implementation satisfies
    the LeaseRepository contract.
    """

    @pytest.fixture
    def repository(self):
        return InMemoryLeaseRepository()

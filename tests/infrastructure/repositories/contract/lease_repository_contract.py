from __future__ import annotations

import pytest

from app.domain.entities.job import Job
from app.domain.entities.lease import Lease
from app.domain.entities.node import Node
from app.domain.entities.worker import Worker
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.domain.value_objects.worker_id import WorkerId


class LeaseRepositoryContract:
    """
    Shared behavioral contract that every
    LeaseRepository implementation must satisfy.
    """

    @pytest.fixture
    def repository(self):
        raise NotImplementedError(
            "Subclasses must provide a `repository` fixture."
        )

    def _make_lease(self) -> Lease:
        node = Node(
            id=NodeId.new(),
            capacity=ResourceRequirements(
                cpu_cores=8,
                memory_mib=16384,
                vram_mib=8192,
            ),
        )

        worker = Worker(
            id=WorkerId.new(),
            node=node,
        )

        job = Job(
            id=JobId.new(),
            resources=ResourceRequirements(
                cpu_cores=1,
                memory_mib=512,
                vram_mib=0,
            ),
        )

        return Lease.create(
            worker_id=worker.id,
            job_id=job.id,
        )

    def test_save_and_get_by_job_id(
        self,
        repository,
    ) -> None:
        lease = self._make_lease()

        repository.save(lease)

        fetched = repository.get_by_job_id(
            lease.job_id,
        )

        assert fetched is not None
        assert fetched.id == lease.id
        assert fetched.job_id == lease.job_id
        assert fetched.worker_id == lease.worker_id

    def test_save_and_get_by_worker_id(
        self,
        repository,
    ) -> None:
        lease = self._make_lease()

        repository.save(lease)

        fetched = repository.get_by_worker_id(
            lease.worker_id,
        )

        assert fetched is not None
        assert fetched.id == lease.id

    def test_list_returns_all_leases(
        self,
        repository,
    ) -> None:
        lease1 = self._make_lease()
        lease2 = self._make_lease()

        repository.save(lease1)
        repository.save(lease2)

        ids = {
            lease.id
            for lease in repository.list()
        }

        assert ids == {
            lease1.id,
            lease2.id,
        }

    def test_delete_removes_lease(
        self,
        repository,
    ) -> None:
        lease = self._make_lease()

        repository.save(lease)

        repository.delete(
            lease.job_id,
        )

        assert (
            repository.get_by_job_id(
                lease.job_id,
            )
            is None
        )

        assert (
            repository.get_by_worker_id(
                lease.worker_id,
            )
            is None
        )

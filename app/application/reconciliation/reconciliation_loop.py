from __future__ import annotations

from app.domain.repositories.lease_repository import (
    LeaseRepository,
)
from app.domain.repositories.worker_repository import (
    WorkerRepository,
)


class ReconciliationLoop:
    """
    Executes one reconciliation cycle.

    The reconciliation loop inspects the current state of the
    worker fleet and active leases. It detects inconsistencies
    and delegates recovery work to dedicated application
    services. It does not perform repairs directly.
    """

    def __init__(
        self,
        worker_repository: WorkerRepository,
        lease_repository: LeaseRepository,
    ) -> None:
        self._worker_repository = worker_repository
        self._lease_repository = lease_repository

    def execute(
        self,
    ) -> None:
        """
        Execute one reconciliation iteration.
        """
        workers = self._worker_repository.list()

        for worker in workers:
            self._reconcile_worker(
                worker,
            )

    def _reconcile_worker(
        self,
        worker,
    ) -> None:
        """
        Inspect one worker.

        Recovery logic will be added in future iterations.
        """
        return

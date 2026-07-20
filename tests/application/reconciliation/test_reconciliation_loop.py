from app.application.reconciliation.reconciliation_loop import (
    ReconciliationLoop,
)


class FakeWorkerRepository:
    def list(
        self,
    ) -> list:
        return []


class FakeLeaseRepository:
    def list(
        self,
    ) -> list:
        return []


def test_reconciliation_loop_runs_without_error() -> None:
    loop = ReconciliationLoop(
        worker_repository=FakeWorkerRepository(),
        lease_repository=FakeLeaseRepository(),
    )

    loop.execute()

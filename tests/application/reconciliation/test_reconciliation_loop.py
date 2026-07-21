from __future__ import annotations

from app.application.reconciliation.reconciliation_loop import (
    ReconciliationLoop,
)


class FakeRecoverExpiredLeaseService:
    """
    Fake expired lease recovery service.
    """

    def __init__(
        self,
    ) -> None:
        self.executed = False

    def execute(
        self,
    ) -> None:
        self.executed = True


class FakeRecoverOfflineNodeService:
    """
    Fake offline node recovery service.
    """

    def __init__(
        self,
    ) -> None:
        self.executed = False

    def execute(
        self,
    ) -> None:
        self.executed = True


def test_reconciliation_loop_runs_services_in_order() -> None:
    expired_service = FakeRecoverExpiredLeaseService()
    offline_service = FakeRecoverOfflineNodeService()

    loop = ReconciliationLoop(
        recover_expired_lease_service=expired_service,
        recover_offline_node_service=offline_service,
    )

    loop.execute()

    assert expired_service.executed is True
    assert offline_service.executed is True

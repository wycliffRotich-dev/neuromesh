from __future__ import annotations

from app.application.reconciliation.recover_expired_lease_service import (
    RecoverExpiredLeaseService,
)
from app.application.reconciliation.recover_offline_node_service import (
    RecoverOfflineNodeService,
)


class ReconciliationLoop:
    """
    Executes one reconciliation cycle.

    The reconciliation loop inspects the current state of the
    worker fleet, active leases, and node liveness. It does not
    decide how to repair inconsistencies itself, it delegates
    each concern to a dedicated recovery service and simply
    runs them in a fixed, predictable order each cycle.
    """

    def __init__(
        self,
        recover_expired_lease_service: RecoverExpiredLeaseService,
        recover_offline_node_service: RecoverOfflineNodeService,
    ) -> None:
        self._recover_expired_lease_service = recover_expired_lease_service
        self._recover_offline_node_service = recover_offline_node_service

    def execute(
        self,
    ) -> None:
        """
        Execute one reconciliation iteration.

        Expired leases are reclaimed first so that a job
        abandoned by a dead worker is freed before offline-node
        recovery re-evaluates what that worker was doing.
        """
        self._recover_expired_lease_service.execute()

        self._recover_offline_node_service.execute()

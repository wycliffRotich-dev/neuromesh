from __future__ import annotations

from app.application.services.release_lease_service import (
    ReleaseLeaseService,
)
from app.application.services.renew_lease_service import (
    RenewLeaseService,
)
from app.domain.repositories.worker_repository import (
    WorkerRepository,
)
from app.domain.value_objects.worker_id import (
    WorkerId,
)


class WorkerExecutionLoop:
    """
    Executes one worker iteration.

    A worker renews its lease, executes its assigned
    job, completes it, and finally releases the lease.
    """

    def __init__(
        self,
        worker_repository: WorkerRepository,
        renew_lease_service: RenewLeaseService,
        release_lease_service: ReleaseLeaseService,
    ) -> None:
        self._worker_repository = worker_repository
        self._renew_lease_service = renew_lease_service
        self._release_lease_service = release_lease_service

    def execute(
        self,
        worker_id: WorkerId,
    ) -> None:
        """
        Execute one worker iteration.
        """
        worker = self._worker_repository.get_by_id(
            worker_id,
        )

        if worker is None:
            raise ValueError(
                "Worker does not exist."
            )

        if worker.running_job is None:
            return

        self._renew_lease_service.execute(
            worker_id,
        )

        worker.start()

        # Job execution would happen here.

        self._release_lease_service.execute(
            worker_id,
        )

from __future__ import annotations

from app.domain.entities.event import Event
from app.domain.repositories.event_repository import (
    EventRepository,
)


class GetJobHistoryService:
    """
    Returns the complete event history
    for a job aggregate.
    """

    def __init__(
        self,
        event_repository: EventRepository,
    ) -> None:
        self._event_repository = event_repository

    def execute(
        self,
        aggregate_id: str,
    ) -> list[Event]:
        """
        Return all events recorded for
        the supplied aggregate.
        """
        return self._event_repository.list_by_aggregate(
            aggregate_id,
        )

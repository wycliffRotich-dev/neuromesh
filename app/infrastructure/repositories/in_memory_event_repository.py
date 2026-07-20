from __future__ import annotations

from app.domain.entities.event import Event
from app.domain.repositories.event_repository import (
    EventRepository,
)


class InMemoryEventRepository(EventRepository):
    """
    In-memory implementation of the EventRepository.
    """

    def __init__(self) -> None:
        self._events: list[Event] = []

    def save(
        self,
        event: Event,
    ) -> None:
        self._events.append(event)

    def list(
        self,
    ) -> list[Event]:
        return list(self._events)

    def list_by_aggregate(
        self,
        aggregate_id: str,
    ) -> list[Event]:
        return [
            event
            for event in self._events
            if event.aggregate_id == aggregate_id
        ]

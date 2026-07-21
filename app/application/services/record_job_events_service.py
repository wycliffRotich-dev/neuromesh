from __future__ import annotations

from app.domain.entities.event import Event
from app.domain.repositories.event_repository import EventRepository
from app.domain.value_objects.event_id import EventId


class RecordJobEventsService:
    """
    Application service responsible for recording
    domain events.
    """

    def __init__(
        self,
        event_repository: EventRepository,
    ) -> None:
        self._event_repository = event_repository

    def record(
        self,
        aggregate_id: str,
        event_type: str,
        aggregate_type: str = "Job",
    ) -> Event:
        """
        Record a domain event.
        """
        event = Event(
            id=EventId.new(),
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            event_type=event_type,
        )

        self._event_repository.save(
            event,
        )

        return event

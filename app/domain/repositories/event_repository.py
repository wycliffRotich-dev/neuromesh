from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.event import Event


class EventRepository(ABC):
    """
    Repository abstraction for domain events.
    """

    @abstractmethod
    def save(
        self,
        event: Event,
    ) -> None:
        """
        Persist a domain event.
        """

    @abstractmethod
    def list(
        self,
    ) -> list[Event]:
        """
        Return every recorded event.
        """

    @abstractmethod
    def list_by_aggregate(
        self,
        aggregate_id: str,
    ) -> list[Event]:
        """
        Return every event belonging to an aggregate.
        """

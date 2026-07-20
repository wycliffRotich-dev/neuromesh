from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.value_objects.event_id import EventId


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass(
    frozen=True,
    slots=True,
)
class Event:
    """
    Immutable record describing a domain event.
    """

    id: EventId
    aggregate_id: str
    aggregate_type: str
    event_type: str
    occurred_at: datetime = field(
        default_factory=utc_now,
    )
    payload: dict[str, str] = field(
        default_factory=dict,
    )

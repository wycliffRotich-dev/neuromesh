from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class EventId:
    """
    Unique identifier for a domain event.
    """

    value: str

    @classmethod
    def new(
        cls,
    ) -> EventId:
        return cls(
            value=str(uuid4()),
        )

    def __str__(
        self,
    ) -> str:
        return self.value

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(
    frozen=True,
    slots=True,
)
class EventId:
    """
    Unique identifier for a domain event.
    """

    value: str

    @classmethod
    def new(
        cls,
    ) -> EventId:
        """
        Create a new unique EventId.
        """
        return cls(
            value=str(uuid4()),
        )

    @classmethod
    def from_string(
        cls,
        value: str,
    ) -> EventId:
        """
        Reconstruct an EventId from persisted storage.

        Validation is performed to ensure the supplied value
        is a valid UUID before creating the value object.
        """
        UUID(
            value,
        )

        return cls(
            value=value,
        )

    def __str__(
        self,
    ) -> str:
        return self.value

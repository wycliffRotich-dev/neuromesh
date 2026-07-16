from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class LeaseId:
    """
    Strongly typed identifier for a lease.
    """

    value: UUID

    @classmethod
    def new(cls) -> "LeaseId":
        return cls(uuid4())

    def __str__(self) -> str:
        return str(self.value)

    def __init__(
        self,
        value: str | UUID,
    ) -> None:
        object.__setattr__(
            self,
            "value",
            UUID(str(value)),
        )

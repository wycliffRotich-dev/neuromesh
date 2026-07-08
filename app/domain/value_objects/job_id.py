from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class JobId:
    """
    Strongly typed identifier for a Job.
    """

    value: UUID

    @classmethod
    def new(cls) -> JobId:
        """
        Create a new unique Job identifier.
        """
        return cls(uuid4())

    def __str__(self) -> str:
        return str(self.value)

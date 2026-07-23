from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class NodeId:
    """
    Strongly typed identifier for a compute node.
    """

    value: UUID

    def __init__(
        self,
        value: str | UUID,
    ) -> None:
        object.__setattr__(
            self,
            "value",
            UUID(str(value)),
        )

    @classmethod
    def new(cls) -> NodeId:
        return cls(uuid4())

    @classmethod
    def from_string(
        cls,
        value: str,
    ) -> NodeId:
        return cls(UUID(value))

    def __str__(self) -> str:
        return str(self.value)

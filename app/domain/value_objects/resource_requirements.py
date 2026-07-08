from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResourceRequirements:
    """
    Value object representing a bundle of compute
    resources: CPU cores, memory, and VRAM.

    Immutable. Validates only against negative values --
    zero is a legitimate state (e.g. a fully-allocated
    node has zero cores remaining). Requirements that
    must be strictly positive (a job cannot request zero
    CPU) are validated at the point of request creation,
    not here.
    """

    cpu_cores: int
    memory_mib: int
    vram_mib: int = 0

    def __post_init__(self) -> None:
        if self.cpu_cores < 0:
            raise ValueError("cpu_cores cannot be negative")

        if self.memory_mib < 0:
            raise ValueError("memory_mib cannot be negative")

        if self.vram_mib < 0:
            raise ValueError("vram_mib cannot be negative")

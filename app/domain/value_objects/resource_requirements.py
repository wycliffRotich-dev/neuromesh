from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResourceRequirements:
    """
    Immutable resource requirements for a workload.
    """

    cpu_cores: int
    memory_mib: int
    vram_mib: int = 0

    def __post_init__(self) -> None:
        if self.cpu_cores <= 0:
            raise ValueError("cpu_cores must be greater than zero")

        if self.memory_mib <= 0:
            raise ValueError("memory_mib must be greater than zero")

        if self.vram_mib < 0:
            raise ValueError("vram_mib cannot be negative")
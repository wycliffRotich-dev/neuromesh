from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SubmitJobRequest:
    """
    Data required to submit a new job.
    """

    cpu_cores: int
    memory_mib: int
    vram_mib: int = 0
from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


@dataclass(slots=True)
class Node:
    """
    Represents a compute node capable of executing jobs.
    """

    id: NodeId
    capacity: ResourceRequirements

    available: ResourceRequirements = field(init=False)

    def __post_init__(self) -> None:
        self.available = self.capacity

    def can_host(
        self,
        requirements: ResourceRequirements,
    ) -> bool:
        """
        Return True if this node has sufficient available resources.
        """
        return (
            self.available.cpu_cores >= requirements.cpu_cores
            and self.available.memory_mib >= requirements.memory_mib
            and self.available.vram_mib >= requirements.vram_mib
        )

    def allocate(
        self,
        requirements: ResourceRequirements,
    ) -> None:
        """
        Allocate resources for a scheduled job.
        """
        if not self.can_host(requirements):
            raise ValueError(
                "Node does not have enough available resources."
            )

        self.available = ResourceRequirements(
            cpu_cores=(
                self.available.cpu_cores
                - requirements.cpu_cores
            ),
            memory_mib=(
                self.available.memory_mib
                - requirements.memory_mib
            ),
            vram_mib=(
                self.available.vram_mib
                - requirements.vram_mib
            ),
        )

    def release(
        self,
        requirements: ResourceRequirements,
    ) -> None:
        """
        Release previously allocated resources back to the node.
        """
        self.available = ResourceRequirements(
            cpu_cores=min(
                self.available.cpu_cores
                + requirements.cpu_cores,
                self.capacity.cpu_cores,
            ),
            memory_mib=min(
                self.available.memory_mib
                + requirements.memory_mib,
                self.capacity.memory_mib,
            ),
            vram_mib=min(
                self.available.vram_mib
                + requirements.vram_mib,
                self.capacity.vram_mib,
            ),
        )
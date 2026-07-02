from __future__ import annotations

from dataclasses import dataclass

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

    def can_host(
        self,
        requirements: ResourceRequirements,
    ) -> bool:
        """
        Return True if this node has sufficient resources.
        """
        return (
            self.capacity.cpu_cores >= requirements.cpu_cores
            and self.capacity.memory_mib >= requirements.memory_mib
            and self.capacity.vram_mib >= requirements.vram_mib
        )
from __future__ import annotations

from app.domain.repositories.node_repository import (
    NodeRepository,
)
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


class ClusterCapacityService:
    """
    Application service responsible for reporting
    the total available capacity of the cluster.
    """

    def __init__(
        self,
        node_repository: NodeRepository,
    ) -> None:
        self._node_repository = node_repository

    def execute(
        self,
    ) -> ResourceRequirements:
        """
        Return the total available resources across
        all alive compute nodes.
        """
        cpu_cores = 0
        memory_mib = 0
        vram_mib = 0

        for node in self._node_repository.list():
            if not node.is_alive():
                continue

            cpu_cores += node.available.cpu_cores
            memory_mib += node.available.memory_mib
            vram_mib += node.available.vram_mib

        return ResourceRequirements(
            cpu_cores=cpu_cores,
            memory_mib=memory_mib,
            vram_mib=vram_mib,
        )

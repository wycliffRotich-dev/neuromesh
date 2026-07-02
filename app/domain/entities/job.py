from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.enums.job_status import JobStatus
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)


@dataclass(slots=True)
class Job:
    """
    Aggregate root representing a workload managed by NeuroMesh.

    A Job owns its lifecycle and is responsible for protecting
    its business invariants.
    """

    id: JobId
    resources: ResourceRequirements
    status: JobStatus = JobStatus.SUBMITTED
    submitted_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
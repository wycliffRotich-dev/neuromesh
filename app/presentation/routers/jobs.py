from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.services.create_job_service import (
    CreateJobService,
)
from app.application.services.get_job_history_service import (
    GetJobHistoryService,
)
from app.application.services.get_job_service import (
    GetJobService,
)
from app.domain.exceptions.job_not_found_error import (
    JobNotFoundError,
)
from app.domain.value_objects.job_id import JobId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.presentation.dependencies import (
    get_create_job_service,
    get_get_job_history_service,
    get_get_job_service,
)
from app.presentation.schemas.create_job_request import (
    CreateJobRequest,
)
from app.presentation.schemas.create_job_response import (
    CreateJobResponse,
)
from app.presentation.schemas.get_job_response import (
    GetJobResponse,
)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post(
    "",
    response_model=CreateJobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    request: CreateJobRequest,
    service: Annotated[
        CreateJobService,
        Depends(get_create_job_service),
    ],
) -> CreateJobResponse:
    """
    Create a new job.
    """
    resources = ResourceRequirements(
        cpu_cores=request.cpu_cores,
        memory_mib=request.memory_mib,
        vram_mib=request.vram_mib,
    )

    job = service.execute(
        resources,
    )

    return CreateJobResponse(
        id=str(job.id),
        status=job.status.name,
    )


@router.get(
    "/{job_id}",
    response_model=GetJobResponse,
    status_code=status.HTTP_200_OK,
)
def get_job(
    job_id: str,
    service: Annotated[
        GetJobService,
        Depends(get_get_job_service),
    ],
) -> GetJobResponse:
    """
    Retrieve an existing job.
    """
    try:
        job = service.execute(
            JobId(
                value=UUID(job_id),
            ),
        )
    except JobNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return GetJobResponse(
        id=str(job.id),
        status=job.status.name,
        cpu_cores=job.resources.cpu_cores,
        memory_mib=job.resources.memory_mib,
        vram_mib=job.resources.vram_mib,
    )


@router.get(
    "/{job_id}/history",
    status_code=status.HTTP_200_OK,
)
def get_job_history(
    job_id: str,
    service: Annotated[
        GetJobHistoryService,
        Depends(get_get_job_history_service),
    ],
) -> list[dict[str, str]]:
    """
    Return every recorded event for a job.
    """

    events = service.execute(
        aggregate_id=job_id,
    )

    return [
        {
            "id": str(event.id),
            "aggregate_type": event.aggregate_type,
            "aggregate_id": event.aggregate_id,
            "event_type": event.event_type,
        }
        for event in events
    ]

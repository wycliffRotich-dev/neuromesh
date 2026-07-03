from fastapi import APIRouter, Depends, status

from app.application.services.create_job_service import (
    CreateJobService,
)
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.presentation.dependencies import (
    get_create_job_service,
)
from app.presentation.schemas.create_job_request import (
    CreateJobRequest,
)
from app.presentation.schemas.create_job_response import (
    CreateJobResponse,
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
    service: CreateJobService = Depends(
        get_create_job_service,
    ),
) -> CreateJobResponse:
    """
    Create a new job.
    """
    resources = ResourceRequirements(
        cpu_cores=request.cpu_cores,
        memory_mib=request.memory_mib,
        vram_mib=request.vram_mib,
    )

    job = service.execute(resources)

    return CreateJobResponse(
        id=str(job.id),
        status=job.status.name,
    )
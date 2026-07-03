from fastapi import APIRouter, Depends, status

from app.application.create_job_service import CreateJobService
from app.domain.value_objects.resource_requirements import ResourceRequirements
from app.presentation.dependencies import get_create_job_service

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_job(
    payload: dict,
    service: CreateJobService = Depends(get_create_job_service),
) -> dict:
    """
    Endpoint to handle incoming job creation requests.
    """
    # 1. Map the raw dict payload values directly to your domain Value Object
    resources = ResourceRequirements(
        cpu_cores=payload["cpu_cores"],
        memory_mib=payload["memory_mib"],
        vram_mib=payload["vram_mib"],
    )

    # 2. Execute the service using the expected domain contract
    job = service.execute(resources=resources)

    # 3. Return the response dict expected by your integration tests
    return {
        "id": str(job.id),
        "status": getattr(job, "status", "SUBMITTED"),
    }
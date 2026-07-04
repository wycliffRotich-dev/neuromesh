from fastapi import APIRouter, Depends, status

from app.application.services.create_node_service import (
    CreateNodeService,
)
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.presentation.dependencies import (
    get_create_node_service,
)
from app.presentation.schemas.create_node_request import (
    CreateNodeRequest,
)
from app.presentation.schemas.create_node_response import (
    CreateNodeResponse,
)

router = APIRouter(
    prefix="/nodes",
    tags=["Nodes"],
)


@router.post(
    "",
    response_model=CreateNodeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_node(
    request: CreateNodeRequest,
    service: CreateNodeService = Depends(
        get_create_node_service,
    ),
) -> CreateNodeResponse:
    """
    Create a new compute node.
    """
    capacity = ResourceRequirements(
        cpu_cores=request.cpu_cores,
        memory_mib=request.memory_mib,
        vram_mib=request.vram_mib,
    )

    node = service.execute(capacity)

    return CreateNodeResponse(
        id=str(node.id),
    )
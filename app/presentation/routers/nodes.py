from fastapi import APIRouter, Depends, HTTPException, status

from app.application.services.create_node_service import (
    CreateNodeService,
)
from app.application.services.get_node_service import (
    GetNodeService,
)
from app.domain.exceptions.node_not_found_error import (
    NodeNotFoundError,
)
from app.domain.value_objects.node_id import NodeId
from app.domain.value_objects.resource_requirements import (
    ResourceRequirements,
)
from app.presentation.dependencies import (
    get_create_node_service,
    get_get_node_service,
)
from app.presentation.schemas.create_node_request import (
    CreateNodeRequest,
)
from app.presentation.schemas.create_node_response import (
    CreateNodeResponse,
)
from app.presentation.schemas.get_node_response import (
    GetNodeResponse,
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


@router.get(
    "/{node_id}",
    response_model=GetNodeResponse,
)
def get_node(
    node_id: str,
    service: GetNodeService = Depends(
        get_get_node_service,
    ),
) -> GetNodeResponse:
    """
    Retrieve a compute node by its identifier.
    """
    try:
        node = service.execute(
            NodeId.from_string(node_id),
        )
    except NodeNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Node not found.",
        )

    return GetNodeResponse(
        id=str(node.id),
        cpu_cores=node.capacity.cpu_cores,
        memory_mib=node.capacity.memory_mib,
        vram_mib=node.capacity.vram_mib,
        available_cpu_cores=node.available.cpu_cores,
        available_memory_mib=node.available.memory_mib,
        available_vram_mib=node.available.vram_mib,
    )
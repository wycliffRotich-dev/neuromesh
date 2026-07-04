from pydantic import BaseModel


class CreateNodeResponse(BaseModel):
    """
    Response returned after creating a compute node.
    """

    id: str
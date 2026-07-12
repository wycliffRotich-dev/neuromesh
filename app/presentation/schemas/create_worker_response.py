from pydantic import BaseModel


class CreateWorkerResponse(BaseModel):
    """
    Response returned after registering a worker.
    """

    id: str
    status: str

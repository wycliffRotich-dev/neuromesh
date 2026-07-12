from pydantic import BaseModel


class CreateWorkerRequest(BaseModel):
    """
    Request payload for registering a worker.
    """

    node_id: str
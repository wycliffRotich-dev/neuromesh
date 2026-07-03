from pydantic import BaseModel


class CreateJobResponse(BaseModel):
    """
    HTTP response returned after creating a job.
    """

    id: str
    status: str
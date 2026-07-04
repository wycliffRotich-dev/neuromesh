from pydantic import BaseModel


class GetJobResponse(BaseModel):
    """
    Response returned when retrieving a job.
    """

    id: str
    status: str
    cpu_cores: int
    memory_mib: int
    vram_mib: int
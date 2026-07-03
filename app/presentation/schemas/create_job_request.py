from pydantic import BaseModel, Field


class CreateJobRequest(BaseModel):
    """
    Request payload for creating a new job.
    """

    cpu_cores: int = Field(gt=0)
    memory_mib: int = Field(gt=0)
    vram_mib: int = Field(ge=0)
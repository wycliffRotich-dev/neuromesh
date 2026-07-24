from datetime import datetime

from pydantic import BaseModel


class GetJobResponse(BaseModel):
    """
    Response returned when retrieving a job.

    Deliberately excludes `command`: job commands are not
    exposed over the public API yet (see ADR 0012).
    """

    id: str
    status: str
    cpu_cores: int
    memory_mib: int
    vram_mib: int
    exit_code: int | None
    submitted_at: datetime
    started_at: datetime | None
    completed_at: datetime | None

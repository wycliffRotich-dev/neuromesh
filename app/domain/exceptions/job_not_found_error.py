from __future__ import annotations

from app.domain.value_objects.job_id import JobId


class JobNotFoundError(Exception):
    """
    Raised when a job with the specified identifier
    cannot be found.
    """

    def __init__(self, job_id: JobId) -> None:
        super().__init__(f"Job with id '{job_id}' was not found.")
        self.job_id = job_id

from __future__ import annotations

from app.domain.exceptions.domain_error import DomainError


class JobAlreadyCompleted(DomainError):
    """
    Raised when an operation is attempted on a completed job.
    """

    pass
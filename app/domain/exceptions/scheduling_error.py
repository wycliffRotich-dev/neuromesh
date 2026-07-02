from __future__ import annotations

from app.domain.exceptions.domain_error import DomainError


class SchedulingError(DomainError):
    """
    Raised when a scheduling operation cannot be completed.
    """

    pass
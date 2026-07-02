from __future__ import annotations

from app.domain.exceptions.domain_error import DomainError


class InvalidJobTransition(DomainError):
    """
    Raised when a job attempts an invalid lifecycle transition.
    """

    pass
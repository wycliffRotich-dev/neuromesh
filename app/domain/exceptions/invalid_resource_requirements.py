from __future__ import annotations

from app.domain.exceptions.domain_error import DomainError


class InvalidResourceRequirements(DomainError):
    """
    Raised when a workload specifies invalid compute resource
    requirements.

    This exception represents a violation of a domain invariant.
    Examples include requesting zero CPU cores, negative memory,
    or negative VRAM.
    """

    pass

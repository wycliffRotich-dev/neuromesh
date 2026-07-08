from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities.job import Job
from app.domain.value_objects.job_id import JobId


class JobRepository(ABC):
    """
    Repository abstraction for jobs.
    """

    @abstractmethod
    def save(
        self,
        job: Job,
    ) -> None: ...

    @abstractmethod
    def get_by_id(
        self,
        job_id: JobId,
    ) -> Job | None: ...

    @abstractmethod
    def list(
        self,
    ) -> list[Job]: ...

    @abstractmethod
    def list_queued(
        self,
    ) -> list[Job]:
        """
        Return all queued jobs.
        """
        ...

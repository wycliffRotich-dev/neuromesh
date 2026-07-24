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

    @abstractmethod
    def list_recent(
        self,
        limit: int,
    ) -> list[Job]:
        """
        Return the most recently submitted jobs, ordered
        newest first, capped at `limit`.

        This is a genuine domain-level query, not a
        persistence detail leaking upward: "give me the
        most recent N jobs" is meaningful vocabulary at the
        repository interface, the same way list_queued()
        already is. Each implementation is responsible for
        pushing the ordering and limit down to its own
        storage engine rather than loading every job into
        memory and discarding most of it.
        """
        ...

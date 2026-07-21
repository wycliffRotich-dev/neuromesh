from sqlite3 import Connection

from app.domain.entities.event import Event
from app.domain.value_objects.event_id import EventId
from app.infrastructure.repositories.sqlite_connection import (
    create_connection,
)
from app.infrastructure.repositories.sqlite_event_repository import (
    SqliteEventRepository,
)


class TestSqliteEventRepositoryContract:
    """
    Contract tests for the SQLite EventRepository implementation.
    """

    connection: Connection

    def setup_method(self) -> None:
        self.connection = create_connection(
            ":memory:",
        )

        self.repository = SqliteEventRepository(
            self.connection,
        )

    def test_save_and_list_returns_saved_event(
        self,
    ) -> None:
        event = Event(
            id=EventId.new(),
            aggregate_id="job-123",
            aggregate_type="Job",
            event_type="JobCreated",
        )

        self.repository.save(
            event,
        )

        events = self.repository.list()

        assert len(events) == 1

        assert events[0].id == event.id
        assert events[0].aggregate_id == event.aggregate_id
        assert events[0].aggregate_type == event.aggregate_type
        assert events[0].event_type == event.event_type

    def test_list_by_aggregate_returns_only_matching_events(
        self,
    ) -> None:
        first = Event(
            id=EventId.new(),
            aggregate_id="job-1",
            aggregate_type="Job",
            event_type="JobCreated",
        )

        second = Event(
            id=EventId.new(),
            aggregate_id="job-2",
            aggregate_type="Job",
            event_type="JobCreated",
        )

        third = Event(
            id=EventId.new(),
            aggregate_id="job-1",
            aggregate_type="Job",
            event_type="JobScheduled",
        )

        self.repository.save(
            first,
        )

        self.repository.save(
            second,
        )

        self.repository.save(
            third,
        )

        events = self.repository.list_by_aggregate(
            "job-1",
        )

        assert len(events) == 2

        assert events[0].id == first.id
        assert events[1].id == third.id

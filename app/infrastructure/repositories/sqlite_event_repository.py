from __future__ import annotations

import json
from datetime import UTC, datetime
from sqlite3 import Connection

from app.domain.entities.event import Event
from app.domain.repositories.event_repository import (
    EventRepository,
)
from app.domain.value_objects.event_id import EventId


class SqliteEventRepository(EventRepository):
    """
    SQLite implementation of the EventRepository contract.
    """

    def __init__(
        self,
        connection: Connection,
    ) -> None:
        self._connection = connection

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                aggregate_id TEXT NOT NULL,
                aggregate_type TEXT NOT NULL,
                event_type TEXT NOT NULL,
                occurred_at TEXT NOT NULL,
                payload TEXT NOT NULL
            )
            """
        )

        self._connection.commit()

    def save(
        self,
        event: Event,
    ) -> None:
        """
        Persist an event.
        """

        self._connection.execute(
            """
            INSERT INTO events (
                id,
                aggregate_id,
                aggregate_type,
                event_type,
                occurred_at,
                payload
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                str(event.id),
                event.aggregate_id,
                event.aggregate_type,
                event.event_type,
                event.occurred_at.isoformat(),
                json.dumps(
                    event.payload,
                ),
            ),
        )

        self._connection.commit()

    def list(
        self,
    ) -> list[Event]:
        """
        Return every stored event.
        """

        rows = self._connection.execute(
            """
            SELECT
                id,
                aggregate_id,
                aggregate_type,
                event_type,
                occurred_at,
                payload
            FROM events
            ORDER BY rowid
            """
        ).fetchall()

        return [
            Event(
                id=EventId(
                    row[0],
                ),
                aggregate_id=row[1],
                aggregate_type=row[2],
                event_type=row[3],
                occurred_at=datetime.fromisoformat(
                    row[4],
                ).astimezone(
                    UTC,
                ),
                payload=json.loads(
                    row[5],
                ),
            )
            for row in rows
        ]

    def list_by_aggregate(
        self,
        aggregate_id: str,
    ) -> list[Event]:
        """
        Return every event belonging to one aggregate.
        """

        rows = self._connection.execute(
            """
            SELECT
                id,
                aggregate_id,
                aggregate_type,
                event_type,
                occurred_at,
                payload
            FROM events
            WHERE aggregate_id = ?
            ORDER BY rowid
            """,
            (
                aggregate_id,
            ),
        ).fetchall()

        return [
            Event(
                id=EventId(
                    row[0],
                ),
                aggregate_id=row[1],
                aggregate_type=row[2],
                event_type=row[3],
                occurred_at=datetime.fromisoformat(
                    row[4],
                ).astimezone(
                    UTC,
                ),
                payload=json.loads(
                    row[5],
                ),
            )
            for row in rows
        ]

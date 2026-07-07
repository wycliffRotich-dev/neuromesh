from __future__ import annotations

import sqlite3


def create_connection(db_path: str) -> sqlite3.Connection:
    """
    Create a SQLite connection configured for use across
    the repository layer.

    check_same_thread=False allows the connection to be
    reused across the async request lifecycle in FastAPI;
    callers are responsible for serializing writes if used
    concurrently from multiple threads.
    """
    connection = sqlite3.connect(
        db_path,
        check_same_thread=False,
    )
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection

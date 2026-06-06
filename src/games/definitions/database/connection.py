"""SQLite connection helpers for game data storage."""

import sqlite3
from pathlib import Path


def create_connection(database_path: str | Path) -> sqlite3.Connection:
    """Create a SQLite database connection.

    Args:
        database_path: Path to the SQLite database file.

    Returns:
        Active SQLite connection.
    """
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection

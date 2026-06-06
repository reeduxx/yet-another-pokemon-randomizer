import sqlite3


def create_schema(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS game_definitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            generation INTEGER NOT NULL,
            internal_title TEXT NOT NULL,
            language_code TEXT NOT NULL,
            revision TEXT NOT NULL,
            version_byte INTEGER,
            header_checksum INTEGER,
            global_checksum INTEGER,
            UNIQUE (
                generation,
                internal_title,
                language_code,
                revision,
                version_byte,
                header_checksum,
                global_checksum
            )
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS game_offsets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_definition_id INTEGER NOT NULL,
            offset_name TEXT NOT NULL,
            offset_value INTEGER,
            FOREIGN KEY (game_definition_id)
                REFERENCES game_definitions(id)
                ON DELETE CASCADE
        )
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_game_definitions_identity
        ON game_definitions (
            generation,
            internal_title,
            language_code,
            revision
        )
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_game_offsets_definition_id
        ON game_offsets (game_definition_id)
        """
    )
    connection.commit()

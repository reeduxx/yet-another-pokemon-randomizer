import sqlite3
from typing import Any


class GameDefinitionRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def insert_definition(self, definition: dict[str, Any]) -> int:
        metadata = definition["metadata"]
        cursor = self.connection.execute(
            """
            INSERT INTO game_definitions (
                name,
                generation,
                internal_title,
                language_code,
                revision,
                version_byte,
                header_checksum,
                global_checksum
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                metadata["name"],
                definition["generation"],
                metadata["internal_title"],
                metadata["language_code"],
                metadata["revision"],
                metadata.get("version_byte"),
                metadata.get("header_checksum"),
                metadata.get("global_checksum"),
            ),
        )

        game_definition_id = cursor.lastrowid

        for offset_name, offset_value in definition["offsets"].items():
            if isinstance(offset_value, list):
                for value in offset_value:
                    self._insert_offset(game_definition_id, offset_name, value)
            else:
                self._insert_offset(game_definition_id, offset_name, offset_value)

        self.connection.commit()

        return game_definition_id

    def get_definition(self, definition_id: int) -> dict[str, Any] | None:
        row = self.connection.execute(
            """
            SELECT *
            FROM game_definitions
            WHERE id = ?
            """,
            (definition_id,),
        ).fetchone()

        if row is None:
            return None

        offsets = self._get_offsets(definition_id)

        return {
            "id": row["id"],
            "generation": row["generation"],
            "metadata": {
                "name": row["name"],
                "internal_title": row["internal_title"],
                "language_code": row["language_code"],
                "revision": row["revision"],
                "version_byte": row["version_byte"],
                "header_checksum": row["header_checksum"],
                "global_checksum": row["global_checksum"],
            },
            "offsets": offsets,
        }

    def get_all_definitions(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT id
            FROM game_definitions
            ORDER BY id
            """
        ).fetchall()

        return [
            definition
            for row in rows
            if (definition := self.get_definition(row["id"])) is not None
        ]

    def find_definition(
        self, internal_title: str, language_code: str, revision: str
    ) -> dict[str, Any] | None:
        row = self.connection.execute(
            """
            SELECT id
            FROM game_definitions
            WHERE internal_title = ?
            AND language_code = ?
            AND revision = ?
            LIMIT 1
            """,
            (
                internal_title,
                language_code,
                revision,
            ),
        ).fetchone()

        if row is None:
            return None

        return self.get_definition(row["id"])

    def _insert_offset(
        self, game_definition_id: int, offset_name: str, offset_value: int | None
    ) -> None:
        self.connection.execute(
            """
            INSERT INTO game_offsets (
                game_definition_id,
                offset_name,
                offset_value
            )
            VALUES (?, ?, ?)
            """,
            (game_definition_id, offset_name, offset_value),
        )

    def _get_offsets(self, definition_id: int) -> dict[str, Any]:
        rows = self.connection.execute(
            """
            SELECT offset_name, offset_value
            FROM game_offsets
            WHERE game_definition_id = ?
            """,
            (definition_id,),
        ).fetchall()

        offsets: dict[str, Any] = {}

        for row in rows:
            name = row["offset_name"]
            value = row["offset_value"]

            if name in offsets:
                if not isinstance(offsets[name], list):
                    offsets[name] = [offsets[name]]

                offsets[name].append(value)
            else:
                offsets[name] = value

        return offsets

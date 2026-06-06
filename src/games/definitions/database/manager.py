from pathlib import Path
from typing import Any
from src.games.definitions.database.connection import create_connection
from src.games.definitions.database.importer import GameDefinitionImporter
from src.games.definitions.database.repository import GameDefinitionRepository
from src.games.definitions.database.schema import create_schema


class GameDefinitionDatabase:
    def __init__(self, database_path: str | Path):
        self.connection = create_connection(database_path)
        self.repository = GameDefinitionRepository(self.connection)
        self.importer = GameDefinitionImporter(self.repository)

    def init(self) -> None:
        create_schema(self.connection)

    def import_definitions(self, definitions: list[dict[str, Any]]) -> list[int]:
        return self.importer.import_definitions(definitions)

    def get_definition(self, definition_id: int) -> dict[str, Any] | None:
        return self.repository.get_definition(definition_id)

    def get_all_definitions(self) -> list[dict[str, Any]]:
        return self.repository.get_all_definitions()

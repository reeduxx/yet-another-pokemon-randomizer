from typing import Any
from src.games.definitions.database.repository import GameDefinitionRepository


class GameDefinitionImporter:
    def __init__(self, repository: GameDefinitionRepository):
        self.repository = repository

    def import_definitions(self, definitions: list[dict[str, Any]]) -> list[int]:
        return [
            self.repository.insert_definition(definition) for definition in definitions
        ]

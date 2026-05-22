from pathlib import Path
from src.games.definitions.factory import DefinitionFactory
from src.games.definitions.loader import DefinitionLoader


class GameRegistry:
    def __init__(self):
        self.loader = DefinitionLoader()
        self.factory = DefinitionFactory()
        self.games = []

    def load_definitions(self, directory: str | Path) -> None:
        definitions = self.loader.load_directory(directory)
        self.games = [self.factory.create(definition) for definition in definitions]

    def detect_game(self, metadata):
        for game in self.games:
            if game.matches(metadata):
                return game

        return None

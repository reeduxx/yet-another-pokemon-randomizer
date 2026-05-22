"""Game definition registry and ROM detection utilities."""

from pathlib import Path
from src.games.base import GameDefinition, ROMMetadata
from src.games.definitions.factory import DefinitionFactory
from src.games.definitions.loader import DefinitionLoader


class GameRegistry:
    """Registry for loaded game definitions."""

    def __init__(self):
        """Initialize an empty game registry."""
        self.loader = DefinitionLoader()
        self.factory = DefinitionFactory()
        self.games: list[GameDefinition] = []

    def load_definitions(self, directory: str | Path) -> None:
        """Load all game definitions from a directory.

        Args:
            directory: Directory containing ROM definition files.
        """
        definitions = self.loader.load_directory(directory)
        self.games = [self.factory.create(definition) for definition in definitions]

    def detect_game(self, metadata: ROMMetadata) -> GameDefinition | None:
        """Detect the game matching the provided ROM metadata.

        Args:
            metadata: ROM metadata used for detection.

        Returns:
            Matching game definition if found, else None.
        """
        for game in self.games:
            if game.matches(metadata):
                return game

        return None

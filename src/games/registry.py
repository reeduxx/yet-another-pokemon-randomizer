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

    def load_definitions(
        self, app_directory: str | Path, user_directory: str | Path | None = None
    ) -> None:
        """Load built-in and optional user game definitions.

        Args:
            app_directory: Directory containing bundled ROM definition files.
            user_directory: Optional directory containing user ROM definition files.
        """
        definitions = self.loader.load_directory(app_directory)

        if user_directory is not None and Path(user_directory).exists():
            definitions.extend(self.loader.load_directory(user_directory))

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

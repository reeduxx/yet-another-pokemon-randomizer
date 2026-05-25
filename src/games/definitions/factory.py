"""ROM definition factory utilities."""

from typing import Any
from src.games.base import GameDefinition
from src.games.gen1.base import Gen1GameDefinition


class DefinitionFactoryError(Exception):
    """Raised when a ROM definition cannot be converted."""


class DefinitionFactory:
    """Create GameDefinition objects from loaded definition dictionaries."""

    def create(self, definition: dict[str, Any]) -> GameDefinition:
        """Create a game definition object from loaded definition data.

        Args:
            definition: Loaded and validated ROM definition dictionary.

        Returns:
            Game definition instance for the requested generation.

        Raises:
            DefinitionFactoryError: If the generation is unsupported.
        """
        metadata = definition["metadata"]
        offsets = definition["offsets"]
        generation = definition["generation"]

        if generation == 1:
            return Gen1GameDefinition(
                generation=generation,
                **metadata,
                **offsets,
            )

        raise DefinitionFactoryError(f"Unsupported game generation: {generation}")

from typing import Any
from src.games.gen1.base import Gen1GameDefinition


class DefinitionFactoryError(Exception):
    """Raised when a ROM definition cannot be converted."""


class DefinitionFactory:
    def create(self, definition: dict[str, Any]):
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

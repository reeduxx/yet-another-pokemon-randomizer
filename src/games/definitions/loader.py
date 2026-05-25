"""ROM definition loading utilities."""

import json
from pathlib import Path
from typing import Any
from pydantic import ValidationError
from src.games.definitions.models import GameDefinitionModel


class DefinitionLoaderError(Exception):
    """Raised when a ROM definition file cannot be loaded."""


class DefinitionLoader:
    """Load and normalize ROM definition files."""

    def load_file(self, path: str | Path) -> dict[str, Any]:
        """Load and validate a ROM definition file.

        Args:
            path: Path to the ROM definition JSON file.

        Returns:
            Loaded and validated ROM definition dictionary.

        Raises:
            DefinitionLoaderError: If the file cannot be read, parsed, or validated.
        """
        path = Path(path)

        try:
            with path.open("r", encoding="utf-8") as file:
                definition = json.load(file)

            parsed = GameDefinitionModel.model_validate(definition)
        except OSError as e:
            raise DefinitionLoaderError(
                f"Could not read definition file: {path}"
            ) from e
        except json.JSONDecodeError as e:
            raise DefinitionLoaderError(
                f"Invalid JSON in definition file: {path}"
            ) from e
        except ValidationError as e:
            raise DefinitionLoaderError(f"Invalid definition file: {path}") from e

        return parsed.model_dump()

    def load_directory(self, directory: str | Path) -> list[dict[str, Any]]:
        """Load all ROM definition files from a directory.

        Args:
            directory: Directory containing ROM definition files.

        Returns:
            List of loaded and normalized ROM definition dictionaries.

        Raises:
            DefinitionLoaderError: If the directory does not exist.
        """
        directory = Path(directory)

        if not directory.exists():
            raise DefinitionLoaderError(
                f"Definition directory does not exist: {directory}"
            )

        return [self.load_file(path) for path in sorted(directory.rglob("*.json"))]

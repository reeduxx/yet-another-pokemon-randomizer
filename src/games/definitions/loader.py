"""ROM definition loading utilities."""

import json
from pathlib import Path
from typing import Any
from src.games.definitions.validator import (
    DefinitionValidator,
    DefinitionValidationError,
)


class DefinitionLoaderError(Exception):
    """Raised when a ROM definition file cannot be loaded."""


class DefinitionLoader:
    """Load and normalize ROM definition files."""

    def __init__(self, validator: DefinitionValidator | None = None):
        """Initialize the definition loader.

        Args:
            validator: Optional validator used to validate loaded definitions.
        """
        self.validator = validator or DefinitionValidator()

    def load_file(self, path: str | Path) -> dict[str, Any]:
        """Load, normalize, and validate a ROM definition file.

        Args:
            path: Path to the ROM definition JSON file.

        Returns:
            Loaded and normalized ROM definition dictionary.

        Raises:
            DefinitionLoaderError: If the file cannot be read, parsed, or validated.
        """
        path = Path(path)

        try:
            with path.open("r", encoding="utf-8") as file:
                definition = json.load(file)

            normalized = self._normalize_values(definition)
            self.validator.validate(normalized)
        except OSError as e:
            raise DefinitionLoaderError(
                f"Could not read definition file: {path}"
            ) from e
        except json.JSONDecodeError as e:
            raise DefinitionLoaderError(
                f"Invalid JSON in definition file: {path}"
            ) from e
        except DefinitionValidationError as e:
            raise DefinitionLoaderError(f"Invalid definition file: {path}") from e

        return normalized

    def load_directory(self, directory: str | Path) -> list[dict[str, Any]]:
        """Load all ROM definition files from a directory.

        Args:
            directory: Directory containing ROM definition files.

        Returns:
            List of loaded and normalized ROM definition dictionaries.
        """
        directory = Path(directory)

        return [self.load_file(path) for path in sorted(directory.rglob("*.json"))]

    def _normalize_values(self, value: Any) -> Any:
        """Recursively normalize definition values.

        Hexadecimal string values are converted to integers.

        Args:
            value: Value to normalize.

        Returns:
            Normalized value.
        """
        if isinstance(value, dict):
            return {
                key: self._normalize_values(inner_value)
                for key, inner_value in value.items()
            }

        if isinstance(value, list):
            return [self._normalize_values(item) for item in value]

        if isinstance(value, str) and value.lower().startswith("0x"):
            return int(value, 16)

        return value

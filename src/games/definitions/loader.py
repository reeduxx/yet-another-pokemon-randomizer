import json
from pathlib import Path
from typing import Any
from src.games.definitions.validator import DefinitionValidator


class DefinitionLoaderError(Exception):
    """Raised when a ROM definition file cannot be loaded."""


class DefinitionLoader:
    def __init__(self, validator: DefinitionValidator | None = None):
        self.validator = validator or DefinitionValidator()

    def load_file(self, path: str | Path) -> dict[str, Any]:
        path = Path(path)

        try:
            with path.open("r", encoding="utf-8") as file:
                definition = json.load(file)
        except OSError as e:
            raise DefinitionLoaderError(
                f"Could not read definition file: {path}"
            ) from e
        except json.JSONDecodeError as e:
            raise DefinitionLoaderError(
                f"Invalid JSON in definition file: {path}"
            ) from e

        normalized = self._normalize_values(definition)
        self.validator.validate(normalized)

        return normalized

    def load_directory(self, directory: str | Path) -> list[dict[str, Any]]:
        directory = Path(directory)

        return [self.load_file(path) for path in sorted(directory.rglob("*.json"))]

    def _normalize_values(self, value: Any) -> Any:
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

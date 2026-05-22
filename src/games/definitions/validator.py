from typing import Any


class DefinitionValidationError(Exception):
    """Raised when a ROM definition is invalid."""


class DefinitionValidator:
    REQUIRED_TOP_LEVEL_KEYS = {
        "version",
        "generation",
        "metadata",
        "offsets",
    }
    REQUIRED_METADATA_KEYS = {
        "name",
        "internal_title",
        "language_code",
        "revision",
    }

    def validate(self, definition: dict[str, Any]) -> None:
        self._validate_top_level(definition)
        self._validate_metadata(definition["metadata"])
        self._validate_offsets(definition["offsets"])

    def _validate_top_level(self, definition: dict[str, Any]) -> None:
        missing = self.REQUIRED_TOP_LEVEL_KEYS - definition.keys()

        if missing:
            raise DefinitionValidationError(
                f"Missing required top-level key(s): {', '.join(sorted(missing))}"
            )

        if definition["version"] != 1:
            raise DefinitionValidationError(
                f"Unsupported definition version: {definition['version']}"
            )

    def _validate_metadata(self, metadata: dict[str, Any]) -> None:
        missing = self.REQUIRED_METADATA_KEYS - metadata.keys()

        if missing:
            raise DefinitionValidationError(
                f"Missing required metadata key(s): {', '.join(sorted(missing))}"
            )

    def _validate_offsets(self, offsets: dict[str, Any]) -> None:
        for key, value in offsets.items():
            if isinstance(value, list):
                if not all(isinstance(item, int) for item in value):
                    raise DefinitionValidationError(
                        f"Offset list '{key}' must contain only integers."
                    )
            elif value is not None and not isinstance(value, int):
                raise DefinitionValidationError(
                    f"Offset '{key}' must be an integer or null."
                )

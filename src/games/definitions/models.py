"""Pydantic models for ROM definition files."""

from typing import Any
from pydantic import BaseModel, ConfigDict, field_validator


class MetadataDefinitionModel(BaseModel):
    """Metadata section of a ROM definition file."""

    model_config = ConfigDict(extra="forbid")
    name: str
    internal_title: str
    language_code: str
    revision: str
    version_byte: int | None = None
    header_checksum: int | None = None
    global_checksum: int | None = None

    @field_validator(
        "version_byte", "header_checksum", "global_checksum", mode="before"
    )
    @classmethod
    def parse_hex_values(cls, value: Any) -> Any:
        """Convert hexadecimal string values to integers."""
        if isinstance(value, str) and value.lower().startswith("0x"):
            return int(value, 16)

        return value


class OffsetsDefinitionModel(BaseModel):
    """Offsets section of a ROM definition file."""

    model_config = ConfigDict(extra="allow")

    @field_validator("*", mode="before")
    @classmethod
    def parse_hex_values(cls, value: Any) -> Any:
        """Convert hexadecimal string values to integers."""
        if isinstance(value, str) and value.lower().startswith("0x"):
            return int(value, 16)
        if isinstance(value, list):
            return [
                int(item, 16)
                if isinstance(item, str) and item.lower().startswith("0x")
                else item
                for item in value
            ]

        return value


class GameDefinitionModel(BaseModel):
    """Top-level ROM definition schema."""

    model_config = ConfigDict(extra="forbid")
    version: int
    generation: int
    metadata: MetadataDefinitionModel
    offsets: OffsetsDefinitionModel

    @field_validator("version")
    @classmethod
    def validate_version(cls, value: int) -> int:
        """Validate the supported schema version."""
        if value != 1:
            raise ValueError(f"Unsupported definition version: {value}")

        return value

"""Base game definition models and ROM metadata structures."""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

# Mapping of ROM language codes to display names.
LANGUAGE_NAMES = {
    "D": "German",
    "E": "English",
    "F": "French",
    "I": "Italian",
    "J": "Japanese",
    "K": "Korean",
    "P": "European",
    "S": "Spanish",
}


@dataclass(slots=True)
class ROMMetadata:
    """Metadata extracted from a ROM header for game detection."""

    size: int

    # Shared
    title: str | None = None
    game_code: str | None = None
    language_code: str | None = None

    # GB/GBC
    version_byte: int | None = None
    header_checksum: int | None = None
    global_checksum: int | None = None

    # Verification
    sha1: str | None = None


@dataclass(slots=True)
class GameDefinition(ABC):
    """Base class for supported game definitions."""

    name: str
    internal_title: str
    generation: int
    language_code: str | None = None
    revision: str | None = None
    species_info_table_offset: int | None = None
    species_name_table_offset: int | None = None
    starting_pc_item_offset: int | None = None
    player_starter_offsets: list[int] | None = None
    rival_starter_offsets: list[int] | None = None

    @abstractmethod
    def get_species_ids(self) -> tuple[int, ...]:
        """Return valid species IDs for this game.

        Returns:
            List of valid species IDs.

        Raises:
            NotImplementedError: If a subclass does not implement this method.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement get_species_ids()"
        )

    @property
    def language_name(self) -> str:
        """Return the display name for the game's language."""
        if self.language_code is None:
            return "Unknown"

        return LANGUAGE_NAMES.get(self.language_code, self.language_code)

    @abstractmethod
    def matches(self, rom_metadata: ROMMetadata) -> bool:
        """Determine whether ROM metadata matches this game definition.

        Args:
            rom_metadata: ROM metadata to compare.

        Returns:
            True if the ROM matches this definition, else False.
        """
        pass

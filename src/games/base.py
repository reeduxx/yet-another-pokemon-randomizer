from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

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

    def get_species_ids(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement get_species_ids()"
        )

    @property
    def language_name(self) -> str:
        if self.language_code is None:
            return "Unknown"

        return LANGUAGE_NAMES.get(self.language_code, self.language_code)

    @abstractmethod
    def matches(self, rom_metadata: ROMMetadata) -> bool:
        pass

"""ROM loading and metadata utilities."""

from src.games.base import ROMMetadata


class ROM:
    """Represents a loaded ROM file and provides metadata access helpers."""

    def __init__(self, data: bytearray, path: str = ""):
        """Initialize a ROM instance.

        Args:
            data: Raw ROM data.
            path: Original ROM file path.
        """
        self.data = data
        self.path = path

    @classmethod
    def load(cls, path: str) -> "ROM":
        """Load a ROM from disk.

        Args:
            path: Path to the ROM file.

        Returns:
            Loaded ROM instance.
        """
        with open(path, "rb") as f:
            return cls(bytearray(f.read()), path)

    def save(self, path: str) -> None:
        """Save the ROM to disk.

        Args:
            path: Output file path.
        """
        with open(path, "wb") as f:
            f.write(self.data)

    def get_title(self) -> str:
        """Return the ROM title."""
        # Currently only supports Game Boy title headers.
        return self.data[0x134:0x144].decode("ascii", errors="ignore").strip("\0")

    def get_version_byte(self) -> int:
        """Return the ROM version byte."""
        return self.data[0x14C]

    def get_header_checksum(self) -> int:
        """Return the ROM header checksum."""
        return self.data[0x14D]

    def get_global_checksum(self) -> int:
        """Return the ROM global checksum."""
        return (self.data[0x14E] << 8) | self.data[0x14F]

    def get_rom_code(self) -> str | None:
        """Return the ROM code if present and valid."""
        try:
            code = self.data[0xAC:0xB0].decode("ascii")
        except UnicodeDecodeError:
            return None

        if code.isprintable():
            return code

        return None

    def get_game_code(self) -> str | None:
        """Return the ROM game code."""
        rom_code = self.get_rom_code()

        if rom_code is None:
            return None

        return rom_code[:3]

    def get_language_code(self) -> str | None:
        """Return the ROM language code."""
        rom_code = self.get_rom_code()

        if rom_code is None:
            return None

        return rom_code[3]

    def get_metadata(self) -> ROMMetadata:
        """Build ROM metadata used for game detection.

        Returns:
            ROM metadata extracted from the ROM header.
        """
        rom_code = self.get_rom_code()

        return ROMMetadata(
            size=len(self.data),
            title=self.get_title(),
            game_code=rom_code[:3] if rom_code else None,
            language_code=rom_code[3] if rom_code else None,
            version_byte=self.get_version_byte(),
            header_checksum=self.get_header_checksum(),
            global_checksum=self.get_global_checksum(),
        )

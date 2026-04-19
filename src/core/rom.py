from src.games.base import ROMMetadata


class ROM:
    def __init__(self, data: bytearray, path: str = ""):
        self.data = data
        self.path = path

    @classmethod
    def load(cls, path: str) -> "ROM":
        with open(path, "rb") as f:
            return cls(bytearray(f.read()), path)

    def save(self, path: str) -> None:
        with open(path, "wb") as f:
            f.write(self.data)

    def get_title(self) -> str:
        return self.data[0x134:0x144].decode("ascii", errors="ignore").strip("\0")

    def get_version_byte(self) -> int:
        return self.data[0x14C]

    def get_header_checksum(self) -> int:
        return self.data[0x14D]

    def get_global_checksum(self) -> int:
        return (self.data[0x14E] << 8) | self.data[0x14F]

    def get_rom_code(self) -> str | None:
        try:
            code = self.data[0xAC:0xB0].decode("ascii")

            if code.isprintable():
                return code
        except:
            pass

        return None

    def get_game_code(self) -> str:
        return self.get_rom_code()[:3]

    def get_language_code(self) -> str:
        return self.get_rom_code()[3]

    def get_metadata(self) -> ROMMetadata:
        return ROMMetadata(
            size=len(self.data),
            title=self.get_title(),
            game_code=self.game_code() if self.get_rom_code() else None,
            language_code=self.get_language_code() if self.get_rom_code() else None,
            version_byte=self.get_version_byte(),
            header_checksum=self.get_header_checksum(),
            global_checksum=self.get_global_checksum(),
        )

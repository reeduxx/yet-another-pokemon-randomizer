from dataclasses import dataclass
from src.games.base import GameDefinition, ROMMetadata

POKEMON_INTERNAL_IDS = (
    0x99,  # BULBASAUR
    0x09,  # IVYSAUR
    0x9A,  # VENUSAUR
    0xB0,  # CHARMANDER
    0xB2,  # CHARMELEON
    0xB4,  # CHARIZARD
    0xB1,  # SQUIRTLE
    0xB3,  # WARTORTLE
    0x1C,  # BLASTOISE
    0x7B,  # CATERPIE
    0x7C,  # METAPOD
    0x7D,  # BUTTERFREE
    0x70,  # WEEDLE
    0x71,  # KAKUNA
    0x72,  # BEEDRILL
    0x24,  # PIDGEY
    0x96,  # PIDGEOTTO
    0x97,  # PIDGEOT
    0xA5,  # RATTATA
    0xA6,  # RATICATE
    0x05,  # SPEAROW
    0x23,  # FEAROW
    0x6C,  # EKANS
    0x2D,  # ARBOK
    0x54,  # PIKACHU
    0x55,  # RAICHU
    0x60,  # SANDSHREW
    0x61,  # SANDSLASH
    0x0F,  # NIDORAN♀
    0xA8,  # NIDORINA
    0x10,  # NIDOQUEEN
    0x03,  # NIDORAN♂
    0xA7,  # NIDORINO
    0x07,  # NIDOKING
    0x04,  # CLEFAIRY
    0x8E,  # CLEFABLE
    0x52,  # VULPIX
    0x53,  # NINETALES
    0x64,  # JIGGLYPUFF
    0x65,  # WIGGLYTUFF
    0x6B,  # ZUBAT
    0x82,  # GOLBAT
    0xB9,  # ODDISH
    0xBA,  # GLOOM
    0xBB,  # VILEPLUME
    0x6D,  # PARAS
    0x2E,  # PARASECT
    0x41,  # VENONAT
    0x77,  # VENOMOTH
    0x3B,  # DIGLETT
    0x76,  # DUGTRIO
    0x4D,  # MEOWTH
    0x90,  # PERSIAN
    0x2F,  # PSYDUCK
    0x80,  # GOLDUCK
    0x39,  # MANKEY
    0x75,  # PRIMEAPE
    0x21,  # GROWLITHE
    0x14,  # ARCANINE
    0x47,  # POLIWAG
    0x6E,  # POLIWHIRL
    0x6F,  # POLIWRATH
    0x94,  # ABRA
    0x26,  # KADABRA
    0x95,  # ALAKAZAM
    0x6A,  # MACHOP
    0x29,  # MACHOKE
    0x7E,  # MACHAMP
    0xBC,  # BELLSPROUT
    0xBD,  # WEEPINBELL
    0xBE,  # VICTREEBEL
    0x18,  # TENTACOOL
    0x9B,  # TENTACRUEL
    0xA9,  # GEODUDE
    0x27,  # GRAVELER
    0x31,  # GOLEM
    0xA3,  # PONYTA
    0xA4,  # RAPIDASH
    0x25,  # SLOWPOKE
    0x08,  # SLOWBRO
    0xAD,  # MAGNEMITE
    0x36,  # MAGNETON
    0x40,  # FARFETCH'D
    0x46,  # DODUO
    0x74,  # DODRIO
    0x3A,  # SEEL
    0x78,  # DEWGONG
    0x0D,  # GRIMER
    0x88,  # MUK
    0x17,  # SHELLDER
    0x8B,  # CLOYSTER
    0x19,  # GASTLY
    0x93,  # HAUNTER
    0x0E,  # GENGAR
    0x22,  # ONIX
    0x30,  # DROWZEE
    0x81,  # HYPNO
    0x4E,  # KRABBY
    0x8A,  # KINGLER
    0x06,  # VOLTORB
    0x8D,  # ELECTRODE
    0x0C,  # EXEGGCUTE
    0x0A,  # EXEGGUTOR
    0x11,  # CUBONE
    0x91,  # MAROWAK
    0x2B,  # HITMONLEE
    0x2C,  # HITMONCHAN
    0x0B,  # LICKITUNG
    0x37,  # KOFFING
    0x8F,  # WEEZING
    0x12,  # RHYHORN
    0x01,  # RHYDON
    0x28,  # CHANSEY
    0x1E,  # TANGELA
    0x02,  # KANGASKHAN
    0x5C,  # HORSEA
    0x5D,  # SEADRA
    0x9D,  # GOLDEEN
    0x9E,  # SEAKING
    0x1B,  # STARYU
    0x98,  # STARMIE
    0x2A,  # MR. MIME
    0x1A,  # SCYTHER
    0x48,  # JYNX
    0x35,  # ELECTABUZZ
    0x33,  # MAGMAR
    0x1D,  # PINSIR
    0x3C,  # TAUROS
    0x85,  # MAGIKARP
    0x16,  # GYARADOS
    0x13,  # LAPRAS
    0x4C,  # DITTO
    0x66,  # EEVEE
    0x69,  # VAPOREON
    0x68,  # JOLTEON
    0x67,  # FLAREON
    0xAA,  # PORYGON
    0x62,  # OMANYTE
    0x63,  # OMASTAR
    0x5A,  # KABUTO
    0x5B,  # KABUTOPS
    0xAB,  # AERODACTYL
    0x84,  # SNORLAX
    0x4A,  # ARTICUNO
    0x4B,  # ZAPDOS
    0x49,  # MOLTRES
    0x58,  # DRATINI
    0x59,  # DRAGONAIR
    0x42,  # DRAGONITE
    0x83,  # MEWTWO
    0x15,  # MEW
)

INTERNAL_ID_TO_DEX_NUM = {
    internal_id: dex_num
    for dex_num, internal_id in enumerate(POKEMON_INTERNAL_IDS, start=1)
}

DEX_NUM_TO_INTERNAL_ID = {
    dex_num: internal_id
    for dex_num, internal_id in enumerate(POKEMON_INTERNAL_IDS, start=1)
}


@dataclass(slots=True)
class Gen1GameDefinition(GameDefinition):
    version_byte: int | None = None
    header_checksum: int | None = None
    global_checksum: int | None = None
    species_info_table_offset = 0x383DE
    title_screen_first_mon_offset: int | None = None
    title_screen_mon_list_offset: int | None = None
    intro_mon_offset: int | None = None
    starting_money_wram_offset: int | None = None
    starting_money_routine_offset: int | None = None
    starting_money_middle_byte_offset: int | None = None
    starting_money_patch_offset: int | None = None
    starting_money_return_offset: int | None = None
    pokedex_owned_wram_offset: int | None = None
    show_pokedex_data_routine_offset: int | None = None
    starter_dex_preview_routine_offset: int | None = None
    starter_dex_preview_patch_offset: int | None = None

    def get_species_ids(self) -> list[int]:
        return POKEMON_INTERNAL_IDS

    def internal_id_to_dex_num(self, species_id: int) -> int:
        try:
            return INTERNAL_ID_TO_DEX_NUM[species_id]
        except KeyError as e:
            raise ValueError(
                f"Unknown Gen 1 internal species id: {species_id:#04x}"
            ) from e

    def dex_num_to_internal_id(self, dex_num: int) -> int:
        try:
            return DEX_NUM_TO_INTERNAL_ID[dex_num]
        except KeyError as e:
            raise ValueError(f"Unknown Gen 1 Pokédex number: {dex_num}") from e

    def matches(self, rom_metadata: ROMMetadata) -> bool:
        if rom_metadata.title is None:
            return False

        return (
            rom_metadata.title == self.internal_title
            and (
                self.version_byte is None
                or rom_metadata.version_byte == self.version_byte
            )
            and (
                self.header_checksum is None
                or rom_metadata.header_checksum == self.header_checksum
            )
            and (
                self.global_checksum is None
                or rom_metadata.global_checksum == self.global_checksum
            )
        )

from species.base import Species
from core.text import decode_gen1_text_fixed
from core.util import read_u8, read_bytes

SPECIES_INFO_OFFSETS = {
    "hp": 0x01,
    "attack": 0x02,
    "defense": 0x03,
    "speed": 0x04,
    "special": 0x05,
    "type1": 0x06,
    "type2": 0x07,
    "catch_rate": 0x08,
    "starting_move1": 0x0F,
    "starting_move2": 0x10,
    "starting_move3": 0x11,
    "starting_move4": 0x12,
    "tmhm_flags": 0x14,
}

SPECIES_INFO_ENTRY_SIZE = 0x1C
SPECIES_NAME_LENGTH_INT = 0xA
SPECIES_NAME_LENGTH_JAP = 0x5


def read_gen1_species_record(rom, game, internal_id: int) -> Species:
    info_offset = game.species_info_table_offset + (
        internal_id * SPECIES_INFO_ENTRY_SIZE
    )
    species_name_length = (
        SPECIES_NAME_LENGTH_JAP
        if game.language_code == "J"
        else SPECIES_NAME_LENGTH_INT
    )
    name_offset = game.species_name_table_offset + (internal_id * species_name_length)

    return Species(
        internal_id=internal_id,
        name=decode_gen1_text_fixed(rom.data, name_offset, species_name_length),
        hp=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["hp"]),
        attack=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["attack"]),
        defense=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["defense"]),
        speed=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["speed"]),
        type1=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["type1"]),
        type2=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["type2"]),
        catch_rate=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["catch_rate"]),
        info_offset=info_offset,
        name_offset=name_offset,
        special=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["special"]),
        starting_move1=read_u8(
            rom.data, info_offset + SPECIES_INFO_OFFSETS["starting_move1"]
        ),
        starting_move2=read_u8(
            rom.data, info_offset + SPECIES_INFO_OFFSETS["starting_move2"]
        ),
        starting_move3=read_u8(
            rom.data, info_offset + SPECIES_INFO_OFFSETS["starting_move3"]
        ),
        starting_move4=read_u8(
            rom.data, info_offset + SPECIES_INFO_OFFSETS["starting_move4"]
        ),
        tmhm_flags=read_bytes(
            rom.data, info_offset + SPECIES_INFO_OFFSETS["tmhm_flags"], 7
        ),
    )

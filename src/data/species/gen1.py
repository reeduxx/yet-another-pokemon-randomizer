from src.core.text import decode_gen1_text_fixed
from src.core.util import read_u8, read_bytes
from src.data.species.base import Species
from src.data.types import (
    BUG,
    DRAGON,
    ELECTRIC,
    FIGHTING,
    FIRE,
    FLYING,
    GHOST,
    GRASS,
    GROUND,
    ICE,
    NORMAL,
    POISON,
    PSYCHIC,
    ROCK,
    WATER,
)

GEN1_TYPE_TO_STANDARD_TYPE = {
    0: NORMAL,
    1: FIGHTING,
    2: FLYING,
    3: POISON,
    4: GROUND,
    5: ROCK,
    7: BUG,
    8: GHOST,
    20: FIRE,
    21: WATER,
    22: GRASS,
    23: ELECTRIC,
    24: PSYCHIC,
    25: ICE,
    26: DRAGON,
}

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
MEW_INTERNAL_ID = 0x15
MEW_INFO_OFFSET = 0x425B


def read_gen1_species_record(rom, game, internal_id: int) -> Species:
    species_index = internal_id - 1

    if internal_id == MEW_INTERNAL_ID:
        info_offset = MEW_INFO_OFFSET
    else:
        dex_index = game.internal_id_to_dex_num(internal_id) - 1
        info_offset = game.species_info_table_offset + (
            dex_index * SPECIES_INFO_ENTRY_SIZE
        )
    species_name_length = (
        SPECIES_NAME_LENGTH_JAP
        if game.language_code == "J"
        else SPECIES_NAME_LENGTH_INT
    )
    name_offset = game.species_name_table_offset + (species_index * species_name_length)

    return Species(
        internal_id=internal_id,
        name=decode_gen1_text_fixed(rom.data, name_offset, species_name_length),
        hp=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["hp"]),
        attack=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["attack"]),
        defense=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["defense"]),
        speed=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["speed"]),
        type1=normalize_gen1_type(
            read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["type1"])
        ),
        type2=normalize_gen1_type(
            read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["type2"])
        ),
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


def normalize_gen1_type(type_id: int) -> int:
    return GEN1_TYPE_TO_STANDARD_TYPE[type_id]

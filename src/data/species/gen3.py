from base import Species
from core.util import read_u8, read_u16_le

SPECIES_INFO_OFFSETS = {
    "hp": 0x00,
    "attack": 0x01,
    "defense": 0x02,
    "speed": 0x03,
    "special_attack": 0x04,
    "special_defense": 0x05,
    "type1": 0x06,
    "type2": 0x07,
    "catch_rate": 0x08,
    "item1": 0x0C,
    "item2": 0x0E,
    "ability1": 0x16,
    "ability2": 0x17,
}

SPECIES_INFO_ENTRY_SIZE = 0x1C
SPECIES_NAME_LENGTH = 0xA


def read_gen3_species_record(rom, game, internal_id: int) -> Species:
    info_offset = game.species_info_table_offset + (
        internal_id * SPECIES_INFO_ENTRY_SIZE
    )
    name_offset = game.species_name_table_offset + (internal_id * SPECIES_NAME_LENGTH)

    return Species(
        internal_id=internal_id,
        name=decode_gen3_text_fixed(rom.data, name_offset, SPECIES_NAME_LENGTH),
        hp=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["hp"]),
        attack=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["attack"]),
        defense=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["defense"]),
        speed=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["speed"]),
        type1=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["type1"]),
        type2=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["type2"]),
        catch_rate=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["catch_rate"]),
        info_offset=info_offset,
        name_offset=name_offset,
        special_attack=read_u8(
            rom.data, info_offset + SPECIES_INFO_OFFSETS["special_attack"]
        ),
        special_defense=read_u8(
            rom.data, info_offset + SPECIES_INFO_OFFSETS["special_defense"]
        ),
        item1=read_u16_le(rom.data, info_offset + SPECIES_INFO_OFFSETS["item1"]),
        item2=read_u16_le(rom.data, info_offset + SPECIES_INFO_OFFSETS["item2"]),
        ability1=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["ability1"]),
        ability2=read_u8(rom.data, info_offset + SPECIES_INFO_OFFSETS["ability2"]),
    )

from src.games.gen1.base import Gen1GameDefinition
from src.games.gen1.constants import (
    RG_JP_SPECIES_NAME_TABLE_OFFSET,
    RG_JP_TITLE_SCREEN_FIRST_MON_OFFSET,
    RG_JP_TITLE_SCREEN_MON_LIST_OFFSET,
    STARTER_DEX_PREVIEW_ROUTINE_OFFSET,
)

GREEN_JP_V10 = Gen1GameDefinition(
    name="ポケットモンスター 緑",
    internal_title="POKEMON GREEN",
    generation=1,
    language_code="J",
    revision="v1.0",
    version_byte=0x00,
    header_checksum=0x9C,
    global_checksum=0xDDD5,
    species_name_table_offset=RG_JP_SPECIES_NAME_TABLE_OFFSET,
    title_screen_first_mon_offset=RG_JP_TITLE_SCREEN_FIRST_MON_OFFSET,
    title_screen_mon_list_offset=RG_JP_TITLE_SCREEN_MON_LIST_OFFSET,
    intro_mon_offset=0x5FB2,
    starting_money_wram_offset=0xD2CB,
    starting_money_routine_offset=0xFBC3,
    starting_money_middle_byte_offset=0xFBCA,
    starting_money_patch_offset=0xFBC3,
    starting_pc_item_offset=0x5F79,
    player_starter_offsets=[0x1CBA7, 0x1CBB8, 0x1CBC9],
    rival_starter_offsets=[],
    pokedex_owned_wram_offset=0xD27B,
    show_pokedex_data_routine_offset=0x3E9D,
    starter_dex_preview_routine_offset=STARTER_DEX_PREVIEW_ROUTINE_OFFSET,
    starter_dex_preview_patch_offset=None,
)

GREEN_JP_V11 = Gen1GameDefinition(
    name="ポケットモンスター 緑",
    internal_title="POKEMON GREEN",
    generation=1,
    language_code="J",
    revision="v1.1",
    version_byte=0x01,
    header_checksum=0x9B,
    global_checksum=0xF547,
    species_name_table_offset=RG_JP_SPECIES_NAME_TABLE_OFFSET,
    title_screen_first_mon_offset=RG_JP_TITLE_SCREEN_FIRST_MON_OFFSET,
    title_screen_mon_list_offset=RG_JP_TITLE_SCREEN_MON_LIST_OFFSET,
    intro_mon_offset=0x5F57,
    starting_money_wram_offset=0xD2CB,
    starting_money_routine_offset=0xFBC3,
    starting_money_middle_byte_offset=0xFBCA,
    starting_money_patch_offset=0xFBC3,
    starting_pc_item_offset=0x5F1E,
    player_starter_offsets=[0x1CBA7, 0x1CBB8, 0x1CBC9],
    rival_starter_offsets=[],
    pokedex_owned_wram_offset=0xD27B,
    show_pokedex_data_routine_offset=0x3E8B,
    starter_dex_preview_routine_offset=STARTER_DEX_PREVIEW_ROUTINE_OFFSET,
    starter_dex_preview_patch_offset=None,
)

GREEN_VERSIONS = [
    GREEN_JP_V10,
    GREEN_JP_V11,
]

from games.base import GameDefinition

LEAFGREEN_EN = GameDefinition(
    name = "POKéMON LEAFGREEN",
    game_code = "BPG",
    language_code = "E",
    pokemon_sprite_table = 0x235088,
    pokemon_palette_table = 0x2372E8,
    starter_offsets = [0x169B91, 0x169D94, 0x169D5E],
    intro_pokemon_offsets = [0x12FB10, 0x130F24, 0x130F78],
    starting_pc_item_offset = None,
    starting_money_offset = None
)

LEAFGREEN_JP = GameDefinition(
    name = "ポケットモンスターリーフグリーン",
    game_code = "BPR",
    language_code = "J",
    pokemon_sprite_table = None,
    pokemon_palette_table = None,
    starter_offsets = [],
    intro_pokemon_offsets = [],
    starting_pc_item_offset = None,
    starting_money_offset = None
)
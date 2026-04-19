from games.base import GameDefinition

EMERALD_EN = GameDefinition(
    name = "POKéMON EMERALD",
    game_code = "BPE",
    language_code = "E",
    pokemon_sprite_table = None,
    pokemon_palette_table = None,
    starter_offsets = [0x5B1DF8, 0x5B1DFA, 0x5B1DFC],
    intro_pokemon_offsets = [0x30B0C, 0x31924, 0x130FA0],
    starting_pc_item_offset = None,
    starting_money_offset = None
)
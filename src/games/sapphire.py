from games.base import GameDefinition

SAPPHIRE_EN = GameDefinition(
    name = "POKéMON SAPPHIRE",
    game_code = "AXP",
    language_code = "E",
    pokemon_sprite_table = 0x1E82E4,
    pokemon_palette_table = 0x1EA544,
    starter_offsets = [0x3F771C, 0x3F771E, 0x3F7720],
    intro_pokemon_offsets = [0xB286, 0x12FB38, 0xA506, 0xB2B8, 0xB2C4],
    starting_pc_item_offset = None,
    starting_money_offset = None
)
from games.base import GameDefinition

RUBY_EN = GameDefinition(
    name = "POKéMON RUBY",
    game_code = "AXV",
    language_code = "E",
    pokemon_sprite_table = 0x1E8354,
    pokemon_palette_table = 0x1EA5B4,
    starter_offsets = [0x3F76C4, 0x3F76C6, 0x3F76C8],
    intro_pokemon_offsets = [0xB286, 0x12FB38, 0xA506, 0xB2B8, 0xB2C4],
    starting_pc_item_offset = None,
    starting_money_offset = None
)
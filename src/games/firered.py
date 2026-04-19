from games.base import Gen3Game

FIRERED_EN = Gen3Game(
    name = "POKéMON FIRERED",
    game_code = "BPR",
    language_code = "E",
    pokemon_sprite_table = 0x2350AC,
    pokemon_palette_table = 0x23730C,
    pokemon_name_table = 0x245EE0,
    starting_pc_item_offset = 0x402220,
    starting_money_offset = 0x54B60,
    intro_pokemon_offsets = [0x12FB38, 0x130F4C, 0x130FA0],
    starter_offsets = [0x169BB5, 0x169DB8, 0x169D82],
    starter_text_pointer_offsets = [0x169C16, 0x169C54, 0x169C35]
)
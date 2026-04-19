import random
from src.core.util import write_u8


def randomize_title_screen_mons(rom, game, all=False, seed=None) -> None:
    if game.title_screen_first_mon_offset is None:
        raise ValueError(
            f"{game.name} does not define a title screen first Pokémon offset"
        )
    if game.title_screen_mon_list_offset is None:
        raise ValueError(
            f"{game.name} does not define a title screen Pokémon list offset"
        )

    valid_ids = list(game.get_species_ids())
    list_length = 0x10

    if len(valid_ids) < list_length:
        raise ValueError(
            "Not enough valid species IDs to fill the title screen list without duplicates"
        )

    rng = random.Random(seed)
    first_mon = rng.choice(valid_ids)
    write_u8(rom.data, game.title_screen_first_mon_offset, first_mon)

    if all:
        remaining_choices = [
            species_id for species_id in valid_ids if species_id != first_mon
        ]
        other_mons = rng.sample(remaining_choices, list_length - 1)
        mon_list = [first_mon] + other_mons

        for i, species_id in enumerate(mon_list):
            write_u8(rom.data, game.title_screen_mon_list_offset + i, species_id)

"""Title screen Pokémon randomization utilities."""

import random
from src.core.rom import ROM
from src.core.util import write_u8
from src.games.base import GameDefinition


def randomize_title_screen_mons(
    rom: ROM, game: GameDefinition, randomize_all=False, seed=None
) -> None:
    """Randomize title screen Pokémon.

    Args:
        rom: Loaded ROM instance.
        game: Detected game definition.
        randomize_all: Whether to randomize the entire title screen list.
        seed: Optional RNG seed.

    Raises:
        ValueError: If required offsets are missing or insufficient species exist.
    """
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

    if randomize_all:
        remaining_choices = valid_ids.copy()
        remaining_choices.remove(first_mon)
        other_mons = rng.sample(remaining_choices, list_length - 1)
        mon_list = [first_mon] + other_mons

        for i, species_id in enumerate(mon_list):
            write_u8(rom.data, game.title_screen_mon_list_offset + i, species_id)
    else:
        write_u8(rom.data, game.title_screen_mon_list_offset, first_mon)

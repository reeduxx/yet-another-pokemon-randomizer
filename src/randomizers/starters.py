"""Starter Pokémon randomization utilities."""

import random
from src.core.rom import ROM
from src.core.util import read_u8, read_u16_le, write_u8, write_u16_le
from src.data.species.base import read_species_records
from src.games.base import GameDefinition
from src.randomizers.engine.starter_rules import (
    choose_random_type_trio,
    generate_starters_from_trio,
)
from src.randomizers.engine.type_trios import TYPE_TRIOS, TypeTrio


def read_starters(rom: ROM, game: GameDefinition) -> list[int]:
    """Read the current player starter Pokémon.

    Args:
        rom: Loaded ROM instance.
        game: Detected game definition.

    Returns:
        List of starter species IDs.
    """
    if game.generation == 1:
        return _read_gen1_starters(rom, game)

    return [read_u16_le(rom.data, offset) for offset in game.starter_offsets]


def randomize_starters(
    rom: ROM,
    game: GameDefinition,
    synchronize_rival_starter=False,
    correct_oak_starter_text=False,
    seed=None,
    use_type_trio=False,
    type_trio: TypeTrio | None = None,
    min_bst: int | None = None,
    max_bst: int | None = None,
) -> list[int]:
    """Randomize player starter Pokémon.

    Args:
        rom: Loaded ROM instance.
        game: Detected game definition.
        synchronize_rival_starter: Whether rival starters should match the randomized choices.
        correct_oak_starter_text: Whether to update starter selection text.
        seed: Optional RNG seed.
        use_type_trio: Whether to use a valid type trio.
        type_trio: The type trio to use.
        min_bst: The minimum base stat total (BST).
        max_bst: The maximum BST.

    Returns:
        Randomized starter species IDs.
    """
    rng = random.Random(seed)

    if use_type_trio:
        species_records = read_species_records(rom, game)

        if type_trio is None:
            type_trio = choose_random_type_trio(TYPE_TRIOS, rng)

        starter_species = generate_starters_from_trio(
            species_records.values(),
            type_trio,
            rng,
            min_bst=min_bst,
            max_bst=max_bst,
        )

        starters = [mon.internal_id for mon in starter_species]
    else:
        species_ids = list(game.get_species_ids())
        starters = rng.sample(species_ids, 3)

    if game.generation in [1, 2]:
        _write_gen1_starters(rom, game, starters, synchronize_rival_starter)
        return starters

    for offset, species_id in zip(game.starter_offsets, starters):
        write_u16_le(rom.data, offset, species_id)

    if correct_oak_starter_text:
        update_starter_choice_texts(rom, game, starters)

    return starters


""" TODO: Fix implementation
def update_starter_choice_texts(
    rom: ROM, game: GameDefinition, starter_species_ids: list[int]
) -> None:
    for i, species_id in enumerate(starter_species_ids):
        species = read_species_record(species_id)
        text = build_starter_choice_text(
            species_name=species.name.upper(),
            species_type=species.type.upper(),
            starter=i,
        )

        encoded = encode_gen3_text(text)
        write_gen3_text_smart(rom, game.starter_text_pointer_offsets[i], encoded)


def build_starter_choice_text(
    species_name: str, species_type: str, starter: int
) -> str:
    if starter == 0:
        return f"I see! {species_name} is your choice.{{NL}}It’s very easy to raise.{{PAGE}}So, {{PLAYER}}, you want to go with{{NL}}the {species_type} POKéMON {species_name}?"
    if starter == 1:
        return f"Ah! {species_name} is your choice.{{NL}}You should raise it patiently.{{PAGE}}So, {{PLAYER}}, you’re claiming the{{NL}}{species_type} POKéMON {species_name}?"
    if starter == 2:
        return f"Hm! {species_name} is your choice.{{NL}}It’s one worth raising.{{PAGE}}So, {{PLAYER}}, you’ve decided on the{{NL}}{species_type} POKéMON {species_name}?"
    raise ValueError(f"Invalid starter index: {starter}")
"""


def _read_gen1_starters(rom: ROM, game: GameDefinition) -> list[int]:
    """Read Gen 1 player starter species IDs."""
    if getattr(game, "player_starter_offsets", None) is None:
        raise ValueError(f"{game.name} does not define starter_offsets.")

    return [read_u8(rom.data, offset) for offset in game.player_starter_offsets]


def _write_gen1_starters(
    rom: ROM, game: GameDefinition, starters: list[int], synchronize_rival_starter=False
) -> None:
    """Write Gen 1 player and rival starter species IDs."""
    if len(starters) != 3:
        raise ValueError("Gen 1 starter randomization requires exactly 3 starters.")

    if getattr(game, "player_starter_offsets", None) is None:
        raise ValueError(f"{game.name} does not define starter_offsets.")

    for offset, species_id in zip(game.player_starter_offsets, starters):
        write_u8(rom.data, offset, species_id)

    if synchronize_rival_starter:
        rival_starters = [starters[1], starters[2], starters[0]]

        # Rival starters are stored 10 bytes before player starter.
        #
        # Ex. XX EA 3D CD 3E 03 EA 3E CD 3E YY 06 02 18 20 08 3E
        #
        # XX = Rival starter
        # YY = Player starter
        for offset, species_id in zip(game.player_starter_offsets, rival_starters):
            write_u8(rom.data, offset - 10, species_id)

        for offset, species_id in zip(game.rival_starter_offsets, rival_starters):
            write_u8(rom.data, offset, species_id)

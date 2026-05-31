import random
from collections.abc import Iterable
from src.data.species.base import Species
from src.randomizers.engine.species_filters import (
    exclude_species_ids,
    filter_by_bst,
    filter_by_type,
)
from src.randomizers.engine.type_trios import TypeTrio


def generate_starters_from_trio(
    species: Iterable[Species],
    trio: TypeTrio,
    rng: random.Random,
    min_bst: int | None = None,
    max_bst: int | None = None,
) -> tuple[Species, Species, Species]:
    """Generate starter Pokémon from the given type trio."""
    species_list = list(species)
    selected_starters: list[Species] = []

    for type_id in trio.types:
        pool = _build_starter_pool(species_list, type_id, min_bst, max_bst)
        pool = exclude_species_ids(
            pool,
            {mon.internal_id for mon in selected_starters},
        )

        if not pool:
            raise ValueError(
                f"No valid starter candidates found for type ID {type_id} in trio {trio.display_name}."
            )

        selected_starters.append(rng.choice(pool))

    rng.shuffle(selected_starters)

    if len(selected_starters) != 3:
        raise ValueError("Starter generation must produce exactly 3 starters.")

    return selected_starters[0], selected_starters[1], selected_starters[2]


def choose_random_type_trio(
    trios: Iterable[TypeTrio],
    rng: random.Random,
) -> TypeTrio:
    """Return a randomly selected type trio."""
    trio_list = list(trios)

    if not trio_list:
        raise ValueError("No type trios were provided.")

    return rng.choice(trio_list)


def _build_starter_pool(
    species: Iterable[Species],
    type_id: int,
    min_bst: int | None = None,
    max_bst: int | None = None,
) -> list[Species]:
    """Build a starter candidate pool for a given type."""
    candidates = filter_by_type(species, type_id)
    candidates = filter_by_bst(candidates, min_bst, max_bst)

    return candidates

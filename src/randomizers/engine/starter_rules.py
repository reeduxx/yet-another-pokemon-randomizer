import random
from collections.abc import Iterable
from src.data.species.base import Species
from src.data.types import (
    FIGHTING,
    FLYING,
    POISON,
    GROUND,
    ROCK,
    BUG,
    STEEL,
    FIRE,
    WATER,
    GRASS,
    ELECTRIC,
    PSYCHIC,
    ICE,
    DARK,
)
from src.randomizers.engine.species_filters import (
    exclude_species_ids,
    filter_by_bst,
    filter_by_type,
)


def generate_type_trio_starters(
    species: Iterable[Species],
    rng: random.Random,
    min_bst: int | None = None,
    max_bst: int | None = None,
) -> tuple[Species, Species, Species]:
    species_list = list(species)
    grass_pool = _build_starter_pool(species_list, GRASS, min_bst, max_bst)
    fire_pool = _build_starter_pool(species_list, FIRE, min_bst, max_bst)
    water_pool = _build_starter_pool(species_list, WATER, min_bst, max_bst)

    if not grass_pool:
        raise ValueError("No valid Grass-type starter candidates found.")
    if not fire_pool:
        raise ValueError("No valid Fire-type starter candidates found.")
    if not water_pool:
        raise ValueError("No valid Water-type starter candidates found.")

    grass_starter = rng.choice(grass_pool)
    fire_pool = exclude_species_ids(fire_pool, {grass_starter.internal_id})

    if not fire_pool:
        raise ValueError("No valid Fire-type starter candidates found.")

    fire_starter = rng.choice(fire_pool)

    water_pool = exclude_species_ids(
        water_pool,
        {grass_starter.internal_id, fire_starter.internal_id},
    )

    if not water_pool:
        raise ValueError("No valid Water-type starter candidates found.")

    water_starter = rng.choice(water_pool)

    return grass_starter, fire_starter, water_starter


def _build_starter_pool(
    species: Iterable[Species],
    type_id: int,
    min_bst: int | None = None,
    max_bst: int | None = None,
) -> list[Species]:
    candidates = filter_by_type(species, type_id)
    candidates = filter_by_bst(candidates, min_bst, max_bst)

    return candidates

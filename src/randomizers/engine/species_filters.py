from collections.abc import Iterable
from src.data.species.base import Species


def filter_by_bst(
    species: Iterable[Species],
    min_bst: int | None = None,
    max_bst: int | None = None,
) -> list[Species]:
    """Return species whose BST falls within the specified range."""
    result: list[Species] = []

    for mon in species:
        if min_bst is not None and mon.bst < min_bst:
            continue
        if max_bst is not None and mon.bst > max_bst:
            continue

        result.append(mon)

    return result


def filter_by_type(species: Iterable[Species], type_id: int) -> list[Species]:
    """Return species that possess the specified type."""
    result: list[Species] = []

    for mon in species:
        if type_id in mon.types:
            result.append(mon)

    return result


def exclude_species_ids(
    species: Iterable[Species], excluded_ids: set[int]
) -> list[Species]:
    """Return species whose internal IDs are not excluded."""
    result: list[Species] = []

    for mon in species:
        if mon.internal_id in excluded_ids:
            continue

        result.append(mon)

    return result

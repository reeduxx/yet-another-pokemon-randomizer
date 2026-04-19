from src.data.items.items_gen1 import ITEMS_BY_ID as GEN1_ITEMS_BY_ID
from src.data.items.items_gen2 import ITEMS_BY_ID as GEN2_ITEMS_BY_ID
from src.data.items.items_gen3 import ITEMS_BY_ID as GEN3_ITEMS_BY_ID

ITEMS_BY_GEN = {
    1: GEN1_ITEMS_BY_ID,
    2: GEN2_ITEMS_BY_ID,
    3: GEN3_ITEMS_BY_ID,
}

ID_BY_ITEM_BY_GEN = {
    gen: {name: item_id for item_id, name in table.items()}
    for gen, table in ITEMS_BY_GEN.items()
}


def get_item_table(gen: int) -> dict[int, str]:
    try:
        return ITEMS_BY_GEN[gen]
    except KeyError as e:
        raise ValueError(f"Unsupported generation: {gen}") from e


def get_item_name(item_id: int, gen: int) -> str:
    table = get_item_table(gen)

    return table.get(item_id, f"UNKNOWN_{item_id}")


def get_item_id(item_name: str, gen: int) -> int | None:
    try:
        return ID_BY_ITEM_BY_GEN[gen][item_name]
    except KeyError:
        return None


def is_valid_item(item_id: int, gen: int) -> bool:
    return item_id in get_item_table(gen)

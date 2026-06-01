from dataclasses import dataclass
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
    TYPES_BY_ID,
)


@dataclass(frozen=True)
class TypeTrio:
    types: tuple[int, int, int]
    name: str = ""

    def __post_init__(self) -> None:
        if len(self.types) != 3:
            raise ValueError("Type trios must contain exactly 3 types.")
        if len(set(self.types)) != 3:
            raise ValueError("Type trios must contain unique types.")

    @property
    def type_names(self) -> tuple[str, ...]:
        """Return the names of the types in this trio."""
        return tuple(TYPES_BY_ID[type_id] for type_id in self.types)

    @property
    def display_name(self) -> str:
        """Return the display name for this trio."""
        if self.name:
            return self.name

        return " / ".join(self.type_names)


STANDARD_TRIO = TypeTrio(
    name="Classic",
    types=(GRASS, FIRE, WATER),
)

TYPE_TRIOS = (
    STANDARD_TRIO,
    TypeTrio(types=(FIGHTING, FLYING, ROCK)),
    TypeTrio(types=(FIRE, ROCK, STEEL)),
    TypeTrio(types=(GRASS, ICE, ROCK)),
    TypeTrio(types=(GRASS, POISON, GROUND)),
    TypeTrio(types=(FIRE, GRASS, GROUND)),
    TypeTrio(types=(FIRE, GRASS, ROCK)),
    TypeTrio(types=(FIRE, ICE, GROUND)),
    TypeTrio(types=(ICE, GROUND, ROCK)),
    TypeTrio(types=(ICE, GROUND, STEEL)),
    TypeTrio(types=(WATER, ELECTRIC, GROUND)),
    TypeTrio(types=(GRASS, FLYING, ROCK)),
    TypeTrio(types=(GRASS, BUG, ROCK)),
    TypeTrio(types=(ICE, FIGHTING, FLYING)),
    TypeTrio(types=(FIGHTING, PSYCHIC, DARK)),
)

TYPE_TRIOS_BY_NAME = {trio.display_name: trio for trio in TYPE_TRIOS}

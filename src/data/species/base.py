from dataclasses import dataclass


@dataclass(slots=True)
class Species:
    # General species info
    internal_id: int
    name: str

    # Core species data
    hp: int
    attack: int
    defense: int
    speed: int
    type1: int
    type2: int
    catch_rate: int
    info_offset: int
    name_offset: int

    # Gens 1/2 unify the special stats, Gen 3+ split them between sp.atk/def
    special: int | None = None
    special_attack: int | None = None
    special_defense: int | None = None

    # Gen 2 introduces items
    item1: int | None = None
    item2: int | None = None

    # Gen 3 introduces abilities, 5+ include hidden abilities
    ability1: int | None = None
    ability2: int | None = None
    ability3: int | None = None

    # Gen 1 stores level 1 moves in the species data
    starting_move1: int | None = None
    starting_move2: int | None = None
    starting_move3: int | None = None
    starting_move4: int | None = None
    # Gens 1/2 store TM/HM learns in the species data
    tmhm_flags: bytes | None = None

    @property
    def bst(self) -> int:
        """Return the base stat total for this species."""
        if self.special is not None:
            return self.hp + self.attack + self.defense + self.speed + self.special

        return (
            self.hp
            + self.attack
            + self.defense
            + self.speed
            + (self.special_attack or 0)
            + (self.special_defense or 0)
        )

    @property
    def types(self) -> tuple[int, int]:
        """Return the species' type IDs."""
        return self.type1, self.type2


def read_species_record(rom, game, internal_id: int) -> Species:
    if game.generation == 1:
        from gen1 import read_gen1_species_record

        return read_gen1_species_record(rom, game, internal_id)

    raise NotImplementedError(
        f"Species reading not implemented for generation {game.generation}"
    )


def read_species_records(rom, game) -> dict[int, Species]:
    species: dict[int, Species] = {}

    for internal_id in game.get_internal_ids():
        species[internal_id] = read_species_record(rom, game, internal_id)

    return species

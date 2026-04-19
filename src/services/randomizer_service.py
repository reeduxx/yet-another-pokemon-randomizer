from dataclasses import dataclass
from pathlib import Path
from src.games.registry import detect_game
from src.core.rom import ROM
from src.randomizers.intro import (
    randomize_intro_mon,
    randomize_starting_pc_item,
    randomize_starting_money,
)
from src.randomizers.starters import randomize_starters
from src.randomizers.titlescreen import randomize_title_screen_mons


@dataclass
class RandomizerSettings:
    randomize_title_screen_mon: bool | None = None
    randomize_title_screen_mon_mode: str | None = None
    randomize_intro_mon: bool | None = None
    randomize_starting_pc_item: bool | None = None
    randomize_starting_money: bool | None = None
    starting_money_min: int | None = None
    starting_money_max: int | None = None
    randomize_starters: bool | None = None
    synchronize_rival_starter: bool | None = None
    correct_oak_starter_text: bool | None = None
    seed: int | None = None


@dataclass
class GameCapabilities:
    randomize_title_screen_mon: bool = False
    randomize_title_screen_mon_mode: bool = False
    randomize_intro_mon: bool = False
    randomize_starting_pc_item: bool = False
    randomize_starting_money: bool = False
    randomize_starters: bool = False
    correct_oak_starter_text: bool = False


@dataclass
class DetectionResult:
    game_name: str
    rom_identifier: str
    language: str
    capabilities: GameCapabilities


def detect_rom_file(rom_path: str) -> DetectionResult:
    rom = ROM.load(rom_path)
    game = detect_game(rom)

    if game is None:
        raise ValueError(f"Unsupported or unrecognized ROM (title: {rom.get_title()})")

    return DetectionResult(
        game_name=game.name,
        rom_identifier=getattr(game, "rom_code", None) or game.internal_title,
        language=game.language_name,
        capabilities=build_game_capabilities(game),
    )


def build_output_path(input_path: str) -> str:
    path = Path(input_path)

    return str(path.with_stem(path.stem + " (Randomized)"))


def randomize_rom_file(
    input_path: str, settings: RandomizerSettings, output_path: str | None = None
) -> str:
    rom = ROM.load(input_path)
    game = detect_game(rom)

    if game is None:
        raise ValueError(f"Unsupported or unrecognized ROM (title: {rom.get_title()})")

    if settings.randomize_title_screen_mon:
        randomize_title_screen_mons(
            rom,
            game,
            settings.randomize_title_screen_mon_mode == "All Pokémon",
            settings.seed,
        )

    if settings.randomize_intro_mon:
        randomize_intro_mon(rom, game, settings.seed)

    if settings.randomize_starting_pc_item:
        randomize_starting_pc_item(rom, game, settings.seed)

    if settings.randomize_starting_money:
        randomize_starting_money(rom, game, settings)

    if settings.randomize_starters:
        randomize_starters(
            rom,
            game,
            settings.synchronize_rival_starter,
            settings.correct_oak_starter_text,
            settings.seed,
        )

    final_output = output_path or build_output_path(input_path)
    rom.save(final_output)

    return final_output


def build_game_capabilities(game) -> GameCapabilities:
    return GameCapabilities(
        randomize_title_screen_mon=getattr(game, "title_screen_first_mon_offset", None)
        is not None,
        randomize_title_screen_mon_mode=getattr(
            game, "title_screen_mon_list_offset", None
        )
        is not None,
        randomize_intro_mon=getattr(game, "intro_mon_offset", None) is not None,
        randomize_starting_pc_item=getattr(game, "starting_pc_item_offset", None)
        is not None,
        randomize_starting_money=(
            getattr(game, "starting_money_middle_byte_offset", None) is not None
            or getattr(game, "starting_money_patch_offset", None) is not None
        ),
        randomize_starters=True,
        correct_oak_starter_text=getattr(game, "starter_text_pointer_offsets", None)
        is not None,
    )

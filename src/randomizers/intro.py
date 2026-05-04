import random
from src.data.items.items import get_item_table
from src.core.util import (
    write_u8,
    write_u16_le,
    write_u32_le,
    write_pointer,
    resolve_range,
    int_to_bcd_3bytes,
    rom_offset_to_gb_address,
)


def randomize_intro_mon(rom, game, seed=None) -> None:
    if game.generation == 1:
        randomize_gen1_intro_mon(rom, game, seed)
    elif game.game_code in ["AXP", "AXV", "BPE"]:
        return
    elif game.game_code in ["BPG", "BPR"]:
        randomize_frlg_intro_mon(rom, game, seed)


def randomize_gen1_intro_mon(rom, game, seed=None) -> None:
    rng = random.Random(seed)

    if getattr(game, "intro_mon_offset", None) is None:
        raise ValueError(f"{game.name} does not define intro_mon_offset.")

    intro_mon = rng.choice(game.get_species_ids())
    write_u8(rom.data, game.intro_mon_offset, intro_mon)


def randomize_frlg_intro_mon(rom, game, seed=None) -> None:
    rng = random.Random(seed)
    mon = rng.randint(1, 250)
    write_u8(rom.data, game.intro_pokemon_offsets[0], mon)
    write_u8(rom.data, game.intro_pokemon_offsets[1], mon)
    write_pointer(
        rom.data, game.intro_pokemon_offsets[2], game.pokemon_sprite_table + (mon * 8)
    )
    write_pointer(
        rom.data,
        game.intro_pokemon_offsets[2] + 4,
        game.pokemon_palette_table + (mon * 8),
    )


def randomize_starting_pc_item(rom, game, seed=None) -> None:
    rng = random.Random(seed)
    item = rng.choice(list(get_item_table(game.generation).keys()))

    if game.generation == 1:
        write_u8(rom.data, game.starting_pc_item_offset, item)
    else:
        write_u16_le(rom.data, game.starting_pc_item_offset, item)


def randomize_starting_money(rom, game, settings) -> None:
    rng = random.Random(settings.seed)
    default_max = (
        9900
        if game.generation == 1 and not settings.patch_starting_money_limit
        else 999999
    )
    min_money, max_money = resolve_range(
        default_min=0,
        default_max=default_max,
        user_min=settings.starting_money_min,
        user_max=settings.starting_money_max,
    )
    money = rng.randrange(min_money, max_money + 1, 100)

    if game.generation == 1:
        randomize_gen1_starting_money(
            rom, game, money, patch=settings.patch_starting_money_limit
        )
        return
    if getattr(game, "starting_money_offset", None) is None:
        return

    write_u32_le(rom.data, game.starting_money_offset, money)


def randomize_gen1_starting_money(rom, game, money: int, patch: bool = False) -> None:
    if money < 0 or money > 999999:
        raise ValueError("Starting money must be between 0 and 999999.")
    if not patch and money > 9900:
        raise ValueError(
            "Gen 1 starting money is limited to 9900 unless the expanded money patch is enabled."
        )
    if (
        money <= 9900
        and money % 100 == 0
        and getattr(game, "starting_money_middle_byte_offset", None) is not None
    ):
        middle_bcd_byte = int_to_bcd_3bytes(money)[1]
        write_u8(rom.data, game.starting_money_middle_byte_offset, middle_bcd_byte)
        return
    if not patch:
        raise ValueError("This starting money value requires the expanded money patch.")
    if getattr(game, "starting_money_patch_offset", None) is None:
        raise ValueError(
            f"{game.name} requires a full starting money patch for {money}, "
            "but no starting_money_patch_offset is defined."
        )

    patch_gen1_starting_money_full(rom, game, money)


def patch_gen1_starting_money_full(rom, game, money: int) -> None:
    if getattr(game, "starting_money_wram_offset", None) is None:
        raise ValueError(f"{game.name} does not define starting_money_wram_offset.")
    if getattr(game, "starting_money_patch_offset", None) is None:
        raise ValueError(f"{game.name} does not define starting_money_patch_offset.")

    bcd1, bcd2, bcd3 = int_to_bcd_3bytes(money)

    # Patch in-place
    # starting_money_return_offset = None means patch in-place
    if getattr(game, "starting_money_return_offset", None) is None:
        patch = bytes(
            [
                0x21,
                game.starting_money_wram_offset & 0xFF,
                (game.starting_money_wram_offset >> 8) & 0xFF,  # ld hl, wPlayerMoney
                0x36,
                bcd1,  # ld [hl], byte1
                0x23,  # inc hl
                0x36,
                bcd2,  # ld [hl], byte2
                0x23,  # inc hl
                0x36,
                bcd3,  # ld [hl], byte3
            ]
        )
        rom.data[
            game.starting_money_patch_offset : game.starting_money_patch_offset
            + len(patch)
        ] = patch
        return

    if getattr(game, "starting_money_routine_offset", None) is None:
        raise ValueError(f"{game.name} does not define starting_money_routine_offset.")

    # Overwrite original routine with jp to custom patch routine
    write_u8(rom.data, game.starting_money_routine_offset, 0xC3)  # jp
    write_u16_le(
        rom.data,
        game.starting_money_routine_offset + 1,
        rom_offset_to_gb_address(game.starting_money_patch_offset),
    )

    # Overwrite leftover original routine with nop
    for i in range(3, 10):
        write_u8(rom.data, game.starting_money_routine_offset + i, 0x00)  # nop

    return_addr = rom_offset_to_gb_address(game.starting_money_return_offset)
    patch = bytes(
        [
            0x21,
            game.starting_money_wram_offset & 0xFF,
            (game.starting_money_wram_offset >> 8) & 0xFF,  # ld hl, wPlayerMoney
            0x36,
            bcd1,  # ld [hl], byte1
            0x23,  # inc hl
            0x36,
            bcd2,  # ld [hl], byte2
            0x23,  # inc hl
            0x36,
            bcd3,  # ld [hl], byte3
            0xAF,  # XOR A
            0xC3,
            return_addr & 0xFF,
            (return_addr >> 8) & 0xFF,  # jp return_offset
        ]
    )
    rom.data[
        game.starting_money_patch_offset : game.starting_money_patch_offset + len(patch)
    ] = patch


def patch_starter_dex_preview(rom, game, owned_bytes: list[int]) -> None:
    write_u8(rom.data, game.starter_dex_preview_routine_offset, 0xC3)  # jp
    write_u16_le(
        rom.data,
        game.starter_dex_preview_routine_offset + 1,
        rom_offset_to_gb_address(game.starter_dex_preview_patch_offset),
    )

    for i in range(3, 15):
        write_u8(rom.data, game.starter_dex_preview_routine_offset + i, 0x00)  # nop

    if not owned_bytes:
        owned_bytes = [0]

    patch = bytearray()
    base_addr = game.pokedex_owned_wram_offset

    for i, value in enumerate(owned_bytes):
        addr = base_addr + i
        patch.extend(
            [
                0x3E,
                value,  # ld a, imm8
                0xEA,
                addr & 0xFF,
                addr >> 8,  # ld [addr], a
            ]
        )

    patch.extend(
        [
            0x3E,
            0x3D,  # ld a, $3D
            0xCD,
            game.show_pokedex_data_routine_offset & 0xFF,
            (game.show_pokedex_data_routine_offset >> 8) & 0xFF,  # call predef
            0xAF,  # xor a
        ]
    )

    for i in range(len(owned_bytes)):
        addr = base_addr + i
        patch.extend(
            [
                0xEA,
                addr & 0xFF,
                addr >> 8,  # ld [addr], a
            ]
        )

    patch.append(0xC9)  # ret
    rom.data[
        game.starter_dex_preview_patch_offset : game.starter_dex_preview_patch_offset
        + len(patch)
    ] = patch

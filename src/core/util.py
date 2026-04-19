def read_u8(data: bytearray, offset: int) -> int:
    return data[offset]


def write_u8(data: bytearray, offset: int, value: int) -> None:
    data[offset] = value & 0xFF


def read_u16_le(data: bytearray, offset: int) -> int:
    return data[offset] | (data[offset + 1] << 8)


def write_u16_le(data: bytearray, offset: int, value: int) -> None:
    data[offset] = value & 0xFF
    data[offset + 1] = (value >> 8) & 0xFF


def read_u32_le(data: bytearray, offset: int) -> int:
    return (
        data[offset]
        | (data[offset + 1] << 8)
        | (data[offset + 2] << 16)
        | (data[offset + 3] << 24)
    )


def write_u32_le(data: bytearray, offset: int, value: int) -> None:
    data[offset] = value & 0xFF
    data[offset + 1] = (value >> 8) & 0xFF
    data[offset + 2] = (value >> 16) & 0xFF
    data[offset + 3] = (value >> 24) & 0xFF


def read_bytes(data: bytearray, offset: int, length: int) -> bytes:
    return bytes(data[offset : offset + length])


def write_bytes(data: bytearray, offset: int, values: bytes) -> None:
    data[offset : offset + len(values)] = values


def read_pointer(data: bytearray, offset: int) -> int:
    value = read_u32_le(data, offset)

    return value - 0x08000000 if value >= 0x08000000 else value


def write_pointer(data: bytearray, offset: int, value: int) -> None:
    write_u32_le(data, offset, value + 0x08000000)


def write_bytes_padded(
    data: bytearray, offset: int, values: bytes, total_length: int, pad_byte: int = 0xFF
) -> None:
    if len(values) > total_length:
        raise ValueError("Encoded text is longer than available space.")

    data[offset : offset + len(values)] = values
    remaining = total_length - len(values)

    if remaining > 0:
        data[offset + len(values) : offset + total_length] = bytes(
            [pad_byte] * remaining
        )


def find_free_space(
    data: bytearray, length: int, start_offset: int = 0x700000, fill_byte: int = 0xFF
) -> int:
    run_start = -1
    run_length = 0

    for i in range(start_offset, len(data)):
        if data[i] == fill_byte:
            if run_start == -1:
                run_start = i
            run_length += 1

            if run_length >= length:
                return run_start
        else:
            run_start = -1
            run_length = 0

    raise ValueError(
        f"Could not find {length} bytes of free space starting at 0x{start_offset:X}"
    )


def copy_bytes(data: bytearray, src: int, dst: int, length: int) -> None:
    data[dst : dst + length] = data[src : src + length]


def resolve_range(
    default_min: int,
    default_max: int,
    user_min: int | None,
    user_max: int | None,
) -> tuple[int, int]:
    min_value = default_min if user_min is None else user_min
    max_value = default_max if user_max is None else user_max

    if min_value < default_min:
        min_value = default_min

    if max_value > default_max:
        max_value = default_max

    if min_value > max_value:
        raise ValueError(
            f"Invalid range: minimum ({min_value}) cannot be greater than maximum ({max_value})."
        )

    return min_value, max_value


def int_to_bcd_3bytes(value: int) -> bytes:
    if not 0 <= value <= 999_999:
        raise ValueError("Value must be between 0 and 999999.")

    digits = f"{value:06d}"

    return bytes((int(digits[i]) << 4) | int(digits[i + 1]) for i in range(0, 6, 2))


def rom_offset_to_gb_address(offset: int) -> int:
    bank = offset // 0x4000
    bank_offset = offset % 0x4000

    if bank == 0:
        return bank_offset

    return 0x4000 + bank_offset

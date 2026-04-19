from core.util import read_pointer, write_pointer, write_bytes_padded, find_free_space

GEN1_ENG_ENCODE_MAP = {
    "‘": 0x70,
    "’": 0x71,
    "“": 0x72,
    "”": 0x73,
    "…": 0x75,
    " ": 0x7F,
    "A": 0x80,
    "B": 0x81,
    "C": 0x82,
    "D": 0x83,
    "E": 0x84,
    "F": 0x85,
    "G": 0x86,
    "H": 0x87,
    "I": 0x88,
    "J": 0x89,
    "K": 0x8A,
    "L": 0x8B,
    "M": 0x8C,
    "N": 0x8D,
    "O": 0x8E,
    "P": 0x8F,
    "Q": 0x90,
    "R": 0x91,
    "S": 0x92,
    "T": 0x93,
    "U": 0x94,
    "V": 0x95,
    "W": 0x96,
    "X": 0x97,
    "Y": 0x98,
    "Z": 0x99,
    "(": 0x9A,
    ")": 0x9B,
    ":": 0x9C,
    ";": 0x9D,
    "[": 0x9E,
    "]": 0x9F,
    "a": 0xA0,
    "b": 0xA1,
    "c": 0xA2,
    "d": 0xA3,
    "e": 0xA4,
    "f": 0xA5,
    "g": 0xA6,
    "h": 0xA7,
    "i": 0xA8,
    "j": 0xA9,
    "k": 0xAA,
    "l": 0xAB,
    "m": 0xAC,
    "n": 0xAD,
    "o": 0xAE,
    "p": 0xAF,
    "q": 0xB0,
    "r": 0xB1,
    "s": 0xB2,
    "t": 0xB3,
    "u": 0xB4,
    "v": 0xB5,
    "w": 0xB6,
    "x": 0xB7,
    "y": 0xB8,
    "z": 0xB9,
    "'": 0xE0,
    "-": 0xE3,
    "?": 0xE6,
    "!": 0xE7,
    "♂": 0xEF,
    ".": 0xF2,
    "/": 0xF3,
    ",": 0xF4,
    "♀": 0xF5,
}

GEN3_ENCODE_MAP = {
    " ": 0x00,
    "é": 0x1B,
    "&": 0x2D,
    "(": 0x5C,
    ")": 0x5D,
    "0": 0xA1,
    "1": 0xA2,
    "2": 0xA3,
    "3": 0xA4,
    "4": 0xA5,
    "5": 0xA6,
    "6": 0xA7,
    "7": 0xA8,
    "8": 0xA9,
    "9": 0xAA,
    "!": 0xAB,
    "?": 0xAC,
    ".": 0xAD,
    "-": 0xAE,
    "…": 0xB0,
    "“": 0xB1,
    "”": 0xB2,
    "‘": 0xB3,
    "’": 0xB4,
    "♂": 0xB5,
    "♀": 0xB6,
    "$": 0xB7,
    ",": 0xB8,
    "×": 0xB9,
    "/": 0xBA,
    "A": 0xBB,
    "B": 0xBC,
    "C": 0xBD,
    "D": 0xBE,
    "E": 0xBF,
    "F": 0xC0,
    "G": 0xC1,
    "H": 0xC2,
    "I": 0xC3,
    "J": 0xC4,
    "K": 0xC5,
    "L": 0xC6,
    "M": 0xC7,
    "N": 0xC8,
    "O": 0xC9,
    "P": 0xCA,
    "Q": 0xCB,
    "R": 0xCC,
    "S": 0xCD,
    "T": 0xCE,
    "U": 0xCF,
    "V": 0xD0,
    "W": 0xD1,
    "X": 0xD2,
    "Y": 0xD3,
    "Z": 0xD4,
    "a": 0xD5,
    "b": 0xD6,
    "c": 0xD7,
    "d": 0xD8,
    "e": 0xD9,
    "f": 0xDA,
    "g": 0xDB,
    "h": 0xDC,
    "i": 0xDD,
    "j": 0xDE,
    "k": 0xDF,
    "l": 0xE0,
    "m": 0xE1,
    "n": 0xE2,
    "o": 0xE3,
    "p": 0xE4,
    "q": 0xE5,
    "r": 0xE6,
    "s": 0xE7,
    "t": 0xE8,
    "u": 0xE9,
    "v": 0xEA,
    "w": 0xEB,
    "x": 0xEC,
    "y": 0xED,
    "z": 0xEE,
    ":": 0xF0,
}

GEN1_TOKEN_MAP = {
    "{NULL}": 0x00,
    "{NL}": 0x4F,
    "{PLAYER}": 0x52,
    "{POKE}": 0x54,
    "{CONT}": 0x55,
    "{DONE}": 0x57,
}

GEN3_TOKEN_MAP = {
    "{PLAYER}": [0xFD, 0x01],
    "{UP}": [0x79],
    "{DOWN}": [0x7A],
    "{LEFT}": [0x7B],
    "{RIGHT}": [0x7C],
    "{SCROLL}": [0xFA],
    "{PAGE}": [0xFB],
    "{NL}": [0xFE],
}

GEN1_EOS = 0x50
GEN3_EOS = 0xFF

GEN1_DECODE_MAP = {value: key for key, value in GEN1_ENG_ENCODE_MAP.items()}
GEN1_TOKEN_DECODE_MAP = {value: key for key, value in GEN1_TOKEN_MAP.items()}
GEN3_DECODE_MAP = {value: key for key, value in GEN3_ENCODE_MAP.items()}
GEN3_TOKEN_DECODE_MAP = {}

for token, values in GEN3_TOKEN_MAP.items():
    if len(values) == 1:
        GEN3_TOKEN_DECODE_MAP[values[0]] = token


def decode_text_fixed(
    data: bytearray,
    offset: int,
    length: int,
    decode_map: dict[int, str],
    eos: int,
    token_decode_map: dict[int, str] | None = None,
) -> str:
    chars: list[str] = []
    token_decode_map = {} if token_decode_map is None else token_decode_map

    for i in range(length):
        value = data[offset + i]

        if value == eos:
            break

        if value in token_decode_map:
            chars.append(token_decode_map[value])
        else:
            chars.append(decode_map.get(value, "?"))

    return "".join(chars)


def decode_gen1_text_fixed(data: bytearray, offset: int, length: int) -> str:
    return decode_text_fixed(
        data=data,
        offset=offset,
        length=length,
        decode_map=GEN1_DECODE_MAP,
        eos=GEN1_EOS,
        token_decode_map=GEN1_TOKEN_DECODE_MAP,
    )


def encode_gen1_text(text: str, append_eos: bool = True) -> bytes:
    result: list[int] = []
    i = 0
    tokens = sorted(GEN1_TOKEN_MAP.items(), key=lambda item: len(item[0]), reverse=True)

    while i < len(text):
        matched = False

        for token, value in tokens:
            if text.startswith(token, i):
                result.append(value)
                i += len(token)
                matched = True
                break

        if matched:
            continue

        char = text[i]

        if char not in GEN1_ENG_CHAR_MAP:
            raise ValueError(f"Unsupported Gen 1 character: {char!r}")

        result.append(GEN1_ENG_CHAR_MAP[char])
        i += 1

    if append_eos:
        result.append(GEN1_EOS)

    return bytes(result)


def decode_gen3_text_fixed(data: bytearray, offset: int, length: int) -> str:
    return decode_text_fixed(
        data=data,
        offset=offset,
        length=length,
        decode_map=GEN3_DECODE_MAP,
        eos=GEN3_EOS,
        token_decode_map=GEN3_TOKEN_DECODE_MAP,
    )


def encode_gen3_text(text: str, append_eos: bool = True) -> bytes:
    result: list[int] = []
    i = 0
    tokens = sorted(GEN3_TOKEN_MAP.items(), key=lambda item: len(item[0]), reverse=True)

    while i < len(text):
        matched = False

        for token, values in tokens:
            if text.startswith(token, i):
                result.extend(values)
                i += len(token)
                matched = True
                break

        if matched:
            continue

        char = text[i]

        if char not in GEN3_CHAR_MAP:
            raise ValueError(f"Unsupported Gen 3 character: {char!r}")

        result.append(GEN3_CHAR_MAP[char])
        i += 1

    if append_eos:
        result.append(GEN3_EOS)

    return bytes(result)


def read_gen1_string_length(data: bytearray, offset: int) -> int:
    i = offset

    while i < len(data):
        if data[i] == GEN1_EOS:
            return (i - offset) + 1

        i += 1

    raise ValueError(f"Unterminated Gen 1 string at offset 0x{offset:X}")


def read_gen3_string_length(data: bytearray, offset: int) -> int:
    i = offset

    while i < len(data):
        if data[i] == 0xFF:
            return (i - offset) + 1

        i += 1

    raise ValueError(f"Unterminated Gen 3 string at offset 0x{offset:X}")


def write_gen3_text_smart(rom, pointer_offset: int, encoded_text: bytes) -> int:
    original_text_offset = read_pointer(rom.data, pointer_offset)
    original_length = read_gen3_string_length(rom.data, original_text_offset)

    if len(encoded_text) <= original_length:
        write_bytes_padded(
            rom.data, original_text_offset, encoded_text, original_length
        )
        return original_text_offset

    new_text_offset = write_text_to_free_space(rom, encoded_text)
    write_pointer(rom.data, pointer_offset, new_text_offset)
    return new_text_offset


def write_text_to_free_space(
    rom, encoded_text: bytes, start_offset: int = 0x700000, fill_byte: int = 0xFF
) -> int:
    offset = find_free_space(
        rom.data,
        length=len(encoded_text),
        start_offset=start_offset,
        fill_byte=fill_byte,
    )

    rom.data[offset : offset + len(encoded_text)] = encoded_text

    return offset

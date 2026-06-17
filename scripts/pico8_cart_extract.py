#!/usr/bin/env python3
"""Extract Lua and API usage from a PICO-8 .p8.png cart."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
import urllib.request

from PIL import Image


API_NAMES = [
    "_init",
    "_update",
    "_update60",
    "_draw",
    "btn",
    "btnp",
    "cls",
    "spr",
    "sspr",
    "map",
    "mget",
    "mset",
    "pget",
    "pset",
    "line",
    "rect",
    "rectfill",
    "circ",
    "circfill",
    "print",
    "pal",
    "palt",
    "camera",
    "clip",
    "sfx",
    "music",
    "fget",
    "fset",
    "cartdata",
    "dset",
    "dget",
    "rnd",
    "flr",
    "mid",
    "sin",
    "cos",
]


class BitReader:
    def __init__(self, data: list[int]) -> None:
        self.data = data
        self.byte_pos = 0
        self.bit_pos = 0
        self.exhausted = False

    def read_bits(self, count: int) -> int:
        result = 0
        for index in range(count):
            if self.byte_pos >= len(self.data):
                self.exhausted = True
                return result
            bit = (self.data[self.byte_pos] >> self.bit_pos) & 1
            result |= bit << index
            self.bit_pos += 1
            if self.bit_pos >= 8:
                self.bit_pos = 0
                self.byte_pos += 1
        return result

    def read_bit(self) -> int:
        return self.read_bits(1)


def read_cart_bytes(path: Path) -> list[int]:
    image = Image.open(path).convert("RGBA")
    bytes_out: list[int] = []
    for _x, _y, (r, g, b, a) in iter_pixels(image):
        bytes_out.append(((a & 0x03) << 6) | ((r & 0x03) << 4) | ((g & 0x03) << 2) | (b & 0x03))
    return bytes_out


def iter_pixels(image: Image.Image):
    width, height = image.size
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            yield x, y, pixels[x, y]


def decompress_pxa(code_bytes: list[int]) -> str:
    unc_size = code_bytes[4] | (code_bytes[5] << 8)
    com_size = code_bytes[6] | (code_bytes[7] << 8)
    reader = BitReader(code_bytes[8 : 8 + com_size])
    mtf = list(range(256))
    output: list[int] = []
    iterations = 0
    max_iterations = unc_size * 10

    while len(output) < unc_size and not reader.exhausted and iterations < max_iterations:
        iterations += 1
        if reader.read_bit() == 1:
            extra = 0
            while reader.read_bit() == 1 and extra < 8 and not reader.exhausted:
                extra += 1
            if reader.exhausted:
                break
            index = reader.read_bits(4 + extra)
            if extra > 0:
                index += (1 << 4) * ((1 << extra) - 1)
            if index >= len(mtf):
                break
            value = mtf[index]
            output.append(value)
            del mtf[index]
            mtf.insert(0, value)
        else:
            if reader.read_bit() == 0:
                off_bits = 15
            elif reader.read_bit() == 0:
                off_bits = 10
            else:
                off_bits = 5
            offset = reader.read_bits(off_bits) + 1
            if offset == 1 and off_bits != 5:
                literal_count = 0
                while literal_count < unc_size and not reader.exhausted:
                    value = reader.read_bits(8)
                    if value == 0:
                        break
                    output.append(value)
                    literal_count += 1
                    if value in mtf:
                        index = mtf.index(value)
                        del mtf[index]
                        mtf.insert(0, value)
            else:
                count = 3
                guard = 0
                while guard < 100 and not reader.exhausted:
                    part = reader.read_bits(3)
                    count += part
                    guard += 1
                    if part != 7:
                        break
                start = len(output) - offset
                for index in range(count):
                    src = start + index
                    if 0 <= src < len(output):
                        output.append(output[src])

    return bytes(output).decode("latin-1")


def decompress_old(code_bytes: list[int]) -> str:
    pico8_chars = "\n 0123456789abcdefghijklmnopqrstuvwxyz!#%(){}[]<>+=/*:;.,~_"
    result = []
    index = 8 if code_bytes[:2] == [0x00, 0x70] else 0
    while index < len(code_bytes):
        byte = code_bytes[index]
        if byte == 0:
            break
        if byte < 0x3C:
            if byte < len(pico8_chars):
                result.append(pico8_chars[byte])
        elif byte < 0x80:
            index += 1
            next_byte = code_bytes[index] if index < len(code_bytes) else 0
            char_code = ((byte - 0x3C) << 4) | (next_byte & 0x0F)
            if 0x20 <= char_code < 0x7F:
                result.append(chr(char_code))
        else:
            index += 1
            next_byte = code_bytes[index] if index < len(code_bytes) else 0
            offset = ((byte & 0x3F) << 8) | next_byte
            length = (byte >> 6) + 2
            start = len(result) - offset
            for copy_index in range(length):
                src = start + copy_index
                if 0 <= src < len(result):
                    result.append(result[src])
        index += 1
    return "".join(result)


def extract_lua(path: Path) -> str:
    bytes_out = read_cart_bytes(path)
    code_bytes = bytes_out[0x4300:]
    if code_bytes[:4] == [0x00, 0x70, 0x78, 0x61]:
        return decompress_pxa(code_bytes)
    if code_bytes[:4] == [0x3A, 0x63, 0x3A, 0x00]:
        return decompress_old(code_bytes[4:])
    if code_bytes[:4] == [0x00, 0x70, 0x69, 0x63]:
        return decompress_old(code_bytes)
    chars = []
    for value in code_bytes:
        if value == 0:
            break
        chars.append(chr(value))
    return "".join(chars)


def api_surface(code: str) -> list[str]:
    found = []
    for name in API_NAMES:
        if re.search(rf"(?<![\w.]){re.escape(name)}\s*\(", code):
            found.append(name)
    return found


def resolve_input(value: str) -> Path:
    if value.startswith("http://") or value.startswith("https://"):
        target = Path(".tmp") / "pico8-carts" / Path(value).name
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            urllib.request.urlretrieve(value, target)
        return target
    return Path(value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cart", help="local .p8.png path or URL")
    parser.add_argument("--out", type=Path, help="write extracted Lua to this path")
    parser.add_argument("--api", action="store_true", help="print detected API surface")
    args = parser.parse_args()

    cart = resolve_input(args.cart)
    code = extract_lua(cart)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(code, encoding="utf-8")
    else:
        sys.stdout.write(code)
        if code and not code.endswith("\n"):
            sys.stdout.write("\n")
    if args.api:
        print("API:", ", ".join(api_surface(code)), file=sys.stderr)
        print(f"Chars: {len(code)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""To a Starling — PyxelPico port.

Adapted from the PICO-8 cart by Peteksi and Gruber (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=45958
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from toastarling_core import ToAStarlingCore  # noqa: E402


SCREEN = 240
TILE_COLORS = {
    "#": 5,
    "B": 13,
    "D": 4,
    "^": 8,
    "b": 14,
    "k": 10,
    "s": 12,
    "c": 11,
    "G": 7,
}


class ToAStarling:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="To a Starling", fps=30)
        self.core = ToAStarlingCore()
        self.mode = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c4e4", "p", "6", "n", 6)
        pyxel.sound(1).set("g4c5", "s", "7", "f", 8)
        pyxel.sound(2).set("c3", "n", "7", "f", 10)
        pyxel.sound(3).set("e4g4b4", "t", "5", "n", 10)

    def reset(self) -> None:
        self.core.reset()
        self.mode = "play"
        self.flash = 0

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.mode == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            return
        if self.mode == "cleared":
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            elif ih.btnp_b() or ih.btnp_select():
                self.mode = "title"
            return

        old_berries = self.core.berries
        old_keys = self.core.keys
        old_deaths = self.core.deaths
        self.core.tick(left=ih.btn_left(), right=ih.btn_right(), jump=ih.btnp_a(), glide=ih.btn_b() or ih.btn_down())
        if self.core.deaths > old_deaths:
            pyxel.play(3, 2)
            self.flash = 5
        elif self.core.berries > old_berries or self.core.keys > old_keys:
            pyxel.play(3, 3)
        elif self.core.message in {"jump", "glide"} and pyxel.frame_count % 5 == 0:
            pyxel.play(3, 0)
        if self.core.cleared:
            pyxel.play(3, 1)
            self.mode = "cleared"

    def draw(self) -> None:
        pyxel.cls(1 if self.flash == 0 else 2)
        if self.mode == "title":
            self._draw_title()
            return
        cam_x = max(0, min(self.core.player.x - 104, self.core.width * self.core.tile - SCREEN))
        cam_y = max(0, min(self.core.player.y - 116, self.core.height * self.core.tile - SCREEN + 32))
        self._draw_sky()
        self._draw_room(cam_x, cam_y)
        self._draw_player(cam_x, cam_y)
        self._draw_hud()
        if self.mode == "cleared":
            self._panel("to a starling", "A again  B title")

    def _draw_title(self) -> None:
        self._draw_sky()
        self._center("to a starling", 48, 7)
        self._center("peteksi + gruber", 62, 6)
        self._draw_big_bird(120, 114)
        self._center("d-pad move  A jump", 178, 7)
        self._center("hold B/down to glide", 192, 7)
        if pyxel.frame_count % 30 < 22:
            self._center("press A", 214, 10)

    def _draw_sky(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 12)
        pyxel.rect(0, 126, SCREEN, 114, 3)
        for x in range(-20, SCREEN, 48):
            pyxel.circ(x + (pyxel.frame_count // 4) % 48, 42, 10, 7)
            pyxel.circ(x + 12 + (pyxel.frame_count // 4) % 48, 40, 8, 7)
        for x in range(0, SCREEN, 24):
            pyxel.line(x, 154, x + 18, 142, 11)

    def _draw_room(self, cam_x: float, cam_y: float) -> None:
        tile = self.core.tile
        for y, row in enumerate(self.core.tiles):
            for x, char in enumerate(row):
                if char == ".":
                    continue
                sx = int(x * tile - cam_x)
                sy = int(y * tile - cam_y + 24)
                if sx < -tile or sy < -tile or sx > SCREEN or sy > SCREEN:
                    continue
                self._draw_tile(char, sx, sy, tile)

    def _draw_tile(self, char: str, x: int, y: int, size: int) -> None:
        color = TILE_COLORS.get(char, 6)
        if char == "#":
            pyxel.rect(x, y, size, size, color)
            pyxel.rectb(x, y, size, size, 1)
        elif char == "^":
            pyxel.tri(x, y + size, x + size // 2, y + 2, x + size, y + size, color)
        elif char == "b":
            pyxel.circ(x + size // 2, y + size // 2, 4, color)
            pyxel.pset(x + size // 2 + 3, y + 3, 3)
        elif char == "k":
            pyxel.circ(x + 4, y + 6, 3, color)
            pyxel.line(x + 7, y + 6, x + 11, y + 6, color)
        elif char == "s":
            pyxel.rect(x + 3, y + 3, 6, 6, color)
            pyxel.line(x + 4, y + 8, x + 8, y + 4, 0)
        elif char == "c":
            pyxel.rect(x + 4, y + 1, 3, 10, color)
            pyxel.tri(x + 7, y + 1, x + 12, y + 4, x + 7, y + 7, 10)
        elif char == "G":
            pyxel.circ(x + 6, y + 6, 5, 7)
            pyxel.line(x + 2, y + 6, x - 6, y + 2, 7)
            pyxel.line(x + 10, y + 6, x + 18, y + 2, 7)
        else:
            pyxel.rect(x, y, size, size, color)
            pyxel.rectb(x, y, size, size, 0)

    def _draw_player(self, cam_x: float, cam_y: float) -> None:
        p = self.core.player
        x = int(p.x - cam_x + 2)
        y = int(p.y - cam_y + 28)
        wing = 2 if ih.btn_b() or p.dy < 0 else 0
        color = 10 if p.on_ground else 7
        pyxel.elli(x, y + 2, 9, 7, color)
        pyxel.tri(x + (2 if p.facing > 0 else -2), y + 3, x + p.facing * 10, y + 5, x + (2 if p.facing > 0 else -2), y + 7, 9)
        pyxel.line(x - 2, y + 4, x - 10, y + wing, 7)
        pyxel.line(x + 2, y + 4, x + 10, y + wing, 7)
        pyxel.pset(x + p.facing * 3, y + 3, 0)

    def _draw_big_bird(self, x: int, y: int) -> None:
        pyxel.elli(x - 18, y - 10, 36, 26, 10)
        pyxel.tri(x + 12, y - 2, x + 32, y + 4, x + 12, y + 10, 9)
        pyxel.line(x - 8, y, x - 54, y - 24, 7)
        pyxel.line(x + 4, y, x + 50, y - 24, 7)
        pyxel.pset(x + 8, y - 4, 0)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 24, 0)
        pyxel.text(8, 6, f"berries {self.core.berries}", 7)
        pyxel.text(78, 6, f"keys {self.core.keys}", 7)
        pyxel.text(132, 6, f"falls {self.core.deaths}", 7)
        pyxel.text(8, 16, self.core.message[:34], 6)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 92, 192, 54, 0)
        pyxel.rectb(24, 92, 192, 54, 7)
        self._center(title, 108, 11)
        self._center(subtitle, 128, 6)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    ToAStarling()

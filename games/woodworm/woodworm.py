"""Woodworm — PyxelPico port.

Adapted from the PICO-8 cart by spratt (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=142717
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from woodworm_core import WoodwormCore  # noqa: E402


SCREEN = 240
TILE = 14
OX = 64
OY = 72


class Woodworm:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Woodworm", fps=30)
        self.core = WoodwormCore()
        self.mode = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c4", "t", "6", "n", 4)
        pyxel.sound(1).set("e3g3", "s", "6", "f", 8)
        pyxel.sound(2).set("c3", "n", "7", "f", 10)
        pyxel.sound(3).set("c4e4g4", "p", "7", "n", 12)

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

        direction = None
        if ih.btnp_left(8, 5):
            direction = "left"
        elif ih.btnp_right(8, 5):
            direction = "right"
        elif ih.btnp_up(8, 5):
            direction = "up"
        elif ih.btnp_down(8, 5):
            direction = "down"
        if direction:
            old_eaten = self.core.wood_eaten
            old_score = self.core.score
            if self.core.move(direction):
                pyxel.play(3, 1 if self.core.wood_eaten > old_eaten else 0)
            else:
                pyxel.play(3, 2)
                self.flash = 4
            if self.core.score > old_score and self.core.cleared:
                pyxel.play(3, 3)
                self.mode = "cleared"
        elif ih.btnp_b():
            if self.core.undo():
                pyxel.play(3, 0)
        elif ih.btnp_select():
            self.core.reset()
            pyxel.play(3, 2)

    def draw(self) -> None:
        pyxel.cls(0 if self.flash == 0 else 2)
        if self.mode == "title":
            self._draw_title()
            return
        self._draw_table()
        self._draw_level()
        self._draw_worm()
        self._draw_hud()
        if self.mode == "cleared":
            self._panel("clever worm", "A next try  B title")

    def _draw_title(self) -> None:
        self._draw_table()
        self._center("woodworm", 48, 11)
        self._center("spratt", 62, 6)
        for i, (x, y) in enumerate(((96, 120), (110, 120), (124, 120), (138, 120))):
            self._draw_segment(x, y, 11 if i == 0 else 3, head=i == 0)
        pyxel.rect(84, 146, 70, 14, 4)
        pyxel.text(98, 150, "munch", 7)
        self._center("d-pad move  B undo", 184, 7)
        self._center("select reset", 198, 7)
        if pyxel.frame_count % 30 < 22:
            self._center("press A", 216, 10)

    def _draw_table(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        pyxel.rect(18, 42, 204, 164, 4)
        pyxel.rectb(18, 42, 204, 164, 5)
        for y in range(54, 196, 14):
            pyxel.line(28, y, 212, y, 5)

    def _draw_level(self) -> None:
        for y, row in enumerate(self.core.tiles):
            for x, char in enumerate(row):
                px, py = OX + x * TILE, OY + y * TILE
                if char == "#":
                    pyxel.rect(px, py, TILE, TILE, 5)
                    pyxel.rectb(px, py, TILE, TILE, 1)
                elif char == "w":
                    pyxel.rect(px + 1, py + 1, TILE - 2, TILE - 2, 4)
                    pyxel.line(px + 3, py + 4, px + TILE - 3, py + 4, 9)
                    pyxel.line(px + 3, py + 9, px + TILE - 3, py + 9, 9)
                elif char == "b":
                    pyxel.rect(px + 1, py + 1, TILE - 2, TILE - 2, 13)
                    pyxel.rectb(px + 1, py + 1, TILE - 2, TILE - 2, 6)
                elif char == "G":
                    pyxel.circ(px + TILE // 2, py + TILE // 2, 6, 10)
                    pyxel.text(px + 3, py + 4, "G", 0)

    def _draw_worm(self) -> None:
        for i, (x, y) in enumerate(reversed(self.core.worm)):
            px, py = OX + x * TILE + TILE // 2, OY + y * TILE + TILE // 2
            self._draw_segment(px, py, 11 if i == len(self.core.worm) - 1 else 3, head=i == len(self.core.worm) - 1)

    def _draw_segment(self, x: int, y: int, color: int, *, head: bool) -> None:
        pyxel.circ(x, y, 6, color)
        pyxel.circb(x, y, 6, 0)
        if head:
            pyxel.pset(x - 2, y - 2, 0)
            pyxel.pset(x + 2, y - 2, 0)
            pyxel.line(x - 3, y + 3, x + 3, y + 3, 0)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 30, 0)
        pyxel.text(8, 6, f"moves {self.core.moves}", 7)
        pyxel.text(72, 6, f"wood {self.core.wood_eaten}", 7)
        pyxel.text(136, 6, f"score {self.core.score}", 7)
        pyxel.text(8, 18, self.core.message[:34], 6)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 92, 192, 54, 0)
        pyxel.rectb(24, 92, 192, 54, 7)
        self._center(title, 108, 11)
        self._center(subtitle, 128, 6)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    Woodworm()

"""P.Craft - PyxelPico port.

Adapted from the PICO-8 cart by NuSan (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=3200
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from pcraft_core import PCraftCore  # noqa: E402


SCREEN = 240
TILE = 16
OX = 24
OY = 42


class PCraft:
    recipes = ("axe", "sword", "boat")

    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="P.Craft", fps=30)
        self.core = PCraftCore()
        self.screen = "title"
        self.craft_index = 0
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3e3g3", "t", "5", "n", 8)
        pyxel.sound(1).set("g4c5", "s", "6", "f", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 10)
        pyxel.sound(3).set("e4g4b4", "p", "5", "n", 10)

    def reset(self) -> None:
        self.core.restart()
        self.screen = "play"
        self.craft_index = 0
        self.flash = 0

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 0)
            return
        if self.core.escaped:
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            elif ih.btnp_select():
                self.screen = "title"
            return

        old_message = self.core.message
        self.core.tick(
            left=ih.btnp_left(hold=8, repeat=6),
            right=ih.btnp_right(hold=8, repeat=6),
            up=ih.btnp_up(hold=8, repeat=6),
            down=ih.btnp_down(hold=8, repeat=6),
            use=ih.btnp_a(),
        )
        if ih.btnp_b():
            self.core.craft(self.recipes[self.craft_index])
        if ih.btnp_select():
            self.craft_index = (self.craft_index + 1) % len(self.recipes)
            self.core.message = f"recipe {self.recipes[self.craft_index]}"
        if ih.btnp_start():
            self.reset()
        if self.core.message != old_message:
            if "crafted" in self.core.message or "escaped" in self.core.message:
                pyxel.play(3, 3)
                self.flash = 6
            elif "gathered" in self.core.message or "crystal" in self.core.message:
                pyxel.play(3, 1)
            elif "need" in self.core.message:
                pyxel.play(3, 2)

    def draw(self) -> None:
        pyxel.cls(11 if self.flash else 1)
        if self.screen == "title":
            self._draw_title()
            return
        self._draw_world()
        self._draw_player()
        self._draw_hud()
        if self.core.escaped:
            self._panel("escaped the island", "A replay   Select title")

    def _draw_title(self) -> None:
        self._draw_sea()
        self._draw_tree(72, 134)
        self._draw_rock(166, 146)
        pyxel.rect(78, 168, 84, 24, 4)
        pyxel.rectb(78, 168, 84, 24, 9)
        self._center("P.Craft", 62, 7)
        self._center("NuSan", 82, 6)
        self._center("A start", 210, 10 if pyxel.frame_count % 30 < 22 else 6)

    def _draw_world(self) -> None:
        self._draw_sea()
        for y, row in enumerate(self.core.tiles):
            for x, tile in enumerate(row):
                sx = OX + x * TILE
                sy = OY + y * TILE
                self._draw_tile(tile, sx, sy)

    def _draw_sea(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 12)
        for y in range(0, SCREEN, 18):
            pyxel.line(0, (y + pyxel.frame_count // 3) % SCREEN, SCREEN, (y + pyxel.frame_count // 3) % SCREEN, 5)

    def _draw_tile(self, tile: str, x: int, y: int) -> None:
        colors = {
            "water": 12,
            "grass": 3,
            "tree": 3,
            "stone": 3,
            "fiber": 3,
            "workbench": 4,
            "cave": 5,
            "shore": 10,
        }
        pyxel.rect(x, y, TILE, TILE, colors[tile])
        pyxel.rectb(x, y, TILE, TILE, 11 if tile != "water" else 5)
        if tile == "tree":
            self._draw_tree(x + 8, y + 14)
        elif tile == "stone":
            self._draw_rock(x + 8, y + 11)
        elif tile == "fiber":
            pyxel.line(x + 6, y + 13, x + 8, y + 5, 11)
            pyxel.line(x + 10, y + 13, x + 8, y + 5, 11)
        elif tile == "workbench":
            pyxel.rect(x + 3, y + 6, 10, 7, 9)
            pyxel.line(x + 4, y + 14, x + 4, y + 16, 0)
            pyxel.line(x + 12, y + 14, x + 12, y + 16, 0)
        elif tile == "cave":
            pyxel.circ(x + 8, y + 11, 6, 0)
            pyxel.rect(x + 3, y + 11, 11, 5, 0)
        elif tile == "shore":
            pyxel.text(x + 3, y + 5, "S", 4)

    def _draw_tree(self, x: int, y: int) -> None:
        pyxel.rect(x - 2, y - 7, 4, 7, 4)
        pyxel.circ(x, y - 10, 6, 11)

    def _draw_rock(self, x: int, y: int) -> None:
        pyxel.circ(x, y, 5, 6)
        pyxel.circb(x, y, 5, 13)

    def _draw_player(self) -> None:
        x = OX + self.core.x * TILE + 8
        y = OY + self.core.y * TILE + 12
        pyxel.circ(x, y - 10, 4, 7)
        pyxel.rect(x - 4, y - 7, 8, 9, 8)
        pyxel.line(x - 3, y + 2, x - 6, y + 7, 7)
        pyxel.line(x + 3, y + 2, x + 6, y + 7, 7)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 36, 0)
        inv = self.core.inventory
        pyxel.text(6, 6, f"wood {inv['wood']} stone {inv['stone']} fiber {inv['fiber']} crystal {inv['crystal']}", 7)
        pyxel.text(6, 17, f"tools {','.join(sorted(self.core.tools - {'hands'})) or 'hands'}", 10)
        pyxel.text(132, 17, f"B craft {self.recipes[self.craft_index]}", 6)
        pyxel.text(6, 28, self.core.message[:54], 13)
        pyxel.text(42, 222, "D-pad move  A use  B craft  Select recipe", 7)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(22, 91, 196, 58, 0)
        pyxel.rectb(22, 91, 196, 58, 7)
        self._center(title, 110, 10)
        self._center(subtitle, 130, 7)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    PCraft()

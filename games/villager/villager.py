"""Villager - PyxelPico port.

Adapted from the PICO-8 cart by partnano (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=38905
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from villager_core import BUILD_COSTS, VillagerCore  # noqa: E402


SCREEN = 240
TILE = 12
OX = 24
OY = 48


class Villager:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Villager", fps=30)
        self.core = VillagerCore()
        self.screen = "title"
        self.plan = "house"
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c4e4", "t", "54", "n", 8)
        pyxel.sound(1).set("g3c4", "p", "65", "n", 10)
        pyxel.sound(2).set("c3", "s", "5", "n", 8)
        pyxel.sound(3).set("c4e4g4", "s", "567", "n", 16)

    def update(self) -> None:
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if ih.btnp_select():
            self.core = VillagerCore(self.core.seed + 1)
            return
        dx = int(ih.btnp_right(hold=8, repeat=6)) - int(ih.btnp_left(hold=8, repeat=6))
        dy = int(ih.btnp_down(hold=8, repeat=6)) - int(ih.btnp_up(hold=8, repeat=6))
        if dx or dy:
            self.core.move_cursor(dx, dy)
        if ih.btnp_a():
            if self.core.gather():
                pyxel.play(3, 0)
        if ih.btnp_b():
            if self.core.build(self.plan):
                pyxel.play(3, 3)
            else:
                self.plan = self.core.cycle_building(self.plan, 1)
                pyxel.play(3, 1)
        if ih.btnp_start():
            self.plan = self.core.cycle_building(self.plan, 1)
        self.core.tick()

    def draw(self) -> None:
        pyxel.cls(12)
        if self.screen == "title":
            self._draw_world()
            self._draw_title()
            return
        self._draw_world()
        self._draw_hud()

    def _draw_world(self) -> None:
        pyxel.rect(OX - 4, OY - 4, self.core.width * TILE + 8, self.core.height * TILE + 8, 4)
        for y in range(self.core.height):
            for x in range(self.core.width):
                tile = self.core.world[(x, y)]
                sx, sy = OX + x * TILE, OY + y * TILE
                pyxel.rect(sx, sy, TILE, TILE, 11)
                if tile == "tree":
                    pyxel.circ(sx + 6, sy + 5, 4, 3)
                    pyxel.rect(sx + 5, sy + 7, 2, 5, 4)
                elif tile == "boulder":
                    pyxel.circ(sx + 6, sy + 7, 4, 5)
                elif tile == "berry":
                    pyxel.circ(sx + 5, sy + 6, 2, 8)
                    pyxel.circ(sx + 8, sy + 7, 2, 8)
                elif tile == "mushroom":
                    pyxel.rect(sx + 5, sy + 6, 3, 5, 7)
                    pyxel.circ(sx + 6, sy + 5, 4, 14)
        for (x, y), kind in self.core.buildings.items():
            self._draw_building(OX + x * TILE, OY + y * TILE, kind)
        cx, cy = self.core.cursor
        pyxel.rectb(OX + cx * TILE - 1, OY + cy * TILE - 1, TILE + 2, TILE + 2, 10)

    def _draw_building(self, x: int, y: int, kind: str) -> None:
        color = {"house": 9, "farm": 3, "workshop": 13, "tavern": 8}[kind]
        pyxel.rect(x + 1, y + 4, 10, 7, color)
        pyxel.tri(x, y + 5, x + 6, y, x + 12, y + 5, 4)
        pyxel.pset(x + 5, y + 8, 0)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 40, 0)
        r = self.core.resources
        pyxel.text(5, 5, f"wood {r['wood']} stone {r['stone']} food {r['food']} pop {self.core.population}", 7)
        pyxel.text(5, 16, f"happy {self.core.happiness} plan {self.plan}  {self.core.message[:24]}", 10)
        costs = BUILD_COSTS[self.plan]
        pyxel.text(5, 28, "cost " + " ".join(f"{k}:{v}" for k, v in costs.items()), 6)
        pyxel.text(5, 228, "D-pad cursor  A gather  B build/cycle  Start plan  Select new island", 6)

    def _draw_title(self) -> None:
        pyxel.rect(24, 46, 192, 74, 0)
        pyxel.rectb(24, 46, 192, 74, 7)
        self._center("VILLAGER", 62, 7)
        self._center("partnano", 80, 6)
        self._center("relaxing city builder", 98, 10)
        self._center("A start", 220, 10 if pyxel.frame_count % 40 < 28 else 5)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    Villager()

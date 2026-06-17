"""Porklike — PyxelPico port.

Adapted from the PICO-8 cart by Krystman (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=37045
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from porklike_core import PorklikeCore, Tile  # noqa: E402


SCREEN = 240
TILE = 12
OX = 30
OY = 38


class Porklike:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Porklike", fps=30)
        self.core = PorklikeCore()
        self.mode = "title"
        self.bump_flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3", "t", "5", "n", 5)
        pyxel.sound(1).set("g2c3", "s", "6", "f", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 12)

    def reset(self) -> None:
        self.core.reset()
        self.mode = "play"
        self.bump_flash = 0

    def update(self) -> None:
        if self.bump_flash > 0:
            self.bump_flash -= 1
        if self.mode == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            return
        if self.mode in {"won", "lost"}:
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            elif ih.btnp_b() or ih.btnp_select():
                self.mode = "title"
            return

        dx = int(ih.btnp_right(8, 6)) - int(ih.btnp_left(8, 6))
        dy = int(ih.btnp_down(8, 6)) - int(ih.btnp_up(8, 6))
        if dx and dy:
            dy = 0
        if dx or dy or ih.btnp_a():
            prev_hp = self.core.player_hp
            result = self.core.move_player(dx, dy)
            if result.value == "blocked":
                pyxel.play(3, 2)
                self.bump_flash = 4
            elif result.value == "attacked":
                pyxel.play(3, 1)
            elif self.core.player_hp < prev_hp:
                pyxel.play(3, 2)
            else:
                pyxel.play(3, 0)
        if self.core.won:
            self.mode = "won"
        elif self.core.lost:
            self.mode = "lost"

    def draw(self) -> None:
        pyxel.cls(1 if self.bump_flash == 0 else 2)
        if self.mode == "title":
            self._draw_title()
            return
        self._draw_map()
        self._draw_items()
        self._draw_enemies()
        self._draw_player()
        self._draw_hud()
        if self.mode == "won":
            self._panel("escaped", "A retry  B title")
        elif self.mode == "lost":
            self._panel("pork chopped", "A retry  B title")

    def _draw_title(self) -> None:
        self._draw_dungeon_backdrop()
        self._center("porklike", 50, 10)
        self._center("krystman", 64, 6)
        self._draw_pig(120, 112, 12)
        self._draw_enemy_shape(87, 130, 8)
        self._draw_enemy_shape(153, 130, 8)
        self._center("d-pad move", 180, 7)
        self._center("bump enemies, find stairs", 194, 7)
        if pyxel.frame_count % 30 < 22:
            self._center("press A", 214, 11)

    def _draw_map(self) -> None:
        self._draw_dungeon_backdrop()
        for y, row in enumerate(self.core.tiles):
            for x, tile in enumerate(row):
                px = OX + x * TILE
                py = OY + y * TILE
                if tile is Tile.WALL:
                    pyxel.rect(px, py, TILE, TILE, 5)
                    pyxel.rectb(px, py, TILE, TILE, 1)
                else:
                    pyxel.rect(px, py, TILE, TILE, 0)
                    pyxel.pset(px + 2, py + 2, 13)
                    if tile is Tile.EXIT:
                        pyxel.rect(px + 3, py + 3, 6, 6, 10)
                        pyxel.text(px + 4, py + 3, ">", 0)

    def _draw_dungeon_backdrop(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        for y in range(24, SCREEN, 24):
            pyxel.line(0, y, SCREEN, y, 13)
        for x in range(0, SCREEN, 24):
            pyxel.line(x, 0, x, SCREEN, 13)

    def _draw_items(self) -> None:
        for item in self.core.items:
            x = OX + item.x * TILE + TILE // 2
            y = OY + item.y * TILE + TILE // 2
            pyxel.circ(x, y, 3, 11)
            pyxel.pset(x + 2, y - 3, 3)

    def _draw_enemies(self) -> None:
        for enemy in self.core.enemies:
            self._draw_enemy_shape(OX + enemy.x * TILE + 6, OY + enemy.y * TILE + 6, 8)

    def _draw_player(self) -> None:
        self._draw_pig(OX + self.core.player_x * TILE + 6, OY + self.core.player_y * TILE + 6, 12)

    def _draw_pig(self, x: int, y: int, color: int) -> None:
        pyxel.circ(x, y, 6, color)
        pyxel.rect(x - 4, y - 8, 3, 4, color)
        pyxel.rect(x + 2, y - 8, 3, 4, color)
        pyxel.rect(x - 3, y, 6, 4, 14)
        pyxel.pset(x - 2, y + 2, 0)
        pyxel.pset(x + 2, y + 2, 0)
        pyxel.pset(x - 2, y - 2, 0)
        pyxel.pset(x + 2, y - 2, 0)

    def _draw_enemy_shape(self, x: int, y: int, color: int) -> None:
        pyxel.rect(x - 5, y - 5, 10, 10, color)
        pyxel.rectb(x - 5, y - 5, 10, 10, 0)
        pyxel.pset(x - 2, y - 1, 0)
        pyxel.pset(x + 2, y - 1, 0)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 28, 0)
        pyxel.text(8, 6, f"floor {self.core.level}", 7)
        pyxel.text(72, 6, f"hp {self.core.player_hp}/{self.core.max_hp}", 7)
        pyxel.text(142, 6, f"score {self.core.score}", 7)
        pyxel.text(8, 18, self.core.message[:28], 6)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(28, 92, 184, 54, 0)
        pyxel.rectb(28, 92, 184, 54, 7)
        self._center(title, 108, 11)
        self._center(subtitle, 128, 6)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    Porklike()

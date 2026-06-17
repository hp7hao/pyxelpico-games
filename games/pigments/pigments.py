"""pigments - PyxelPico port.

Adapted from the PICO-8 cart by benjamin_soule (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=40490
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from pigments_core import PigmentsCore  # noqa: E402


SCREEN = 240
TILE = 20
BOARD_X = 30
BOARD_Y = 34


class Pigments:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="pigments", fps=30)
        self.core = PigmentsCore()
        self.screen = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3e3g3", "t", "5", "n", 8)
        pyxel.sound(1).set("c4f4a4", "p", "6", "n", 8)
        pyxel.sound(2).set("f2c2", "n", "7", "f", 10)
        pyxel.sound(3).set("c4e4g4c5", "s", "5", "n", 14)

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if ih.btnp_start() or ih.btnp_b() or ih.btnp_select():
            self.core.restart()
            self.flash = 4
            return
        if self.core.game_over or self.core.level_clear:
            if ih.btnp_a():
                self.core.restart()
                self.flash = 4
            return

        before_score = self.core.score
        before_over = self.core.game_over
        moved = False
        if ih.btnp_left():
            moved = self.core.move(-1, 0)
        elif ih.btnp_right():
            moved = self.core.move(1, 0)
        elif ih.btnp_up():
            moved = self.core.move(0, -1)
        elif ih.btnp_down():
            moved = self.core.move(0, 1)
        elif ih.btnp_a():
            self.core.wait()
            moved = True
        if moved and self.core.score > before_score:
            pyxel.play(3, 1)
        elif moved:
            pyxel.play(3, 0)
        if not before_over and self.core.game_over:
            self.flash = 12
            pyxel.play(3, 2)
        if self.core.level_clear:
            pyxel.play(3, 3)

    def draw(self) -> None:
        pyxel.cls(8 if self.flash else 0)
        if self.screen == "title":
            self._draw_title()
            return
        self._draw_board()
        self._draw_actors()
        self._draw_hud()
        if self.core.game_over:
            self._panel("sliced", "A retry")
        elif self.core.level_clear:
            self._panel("fully painted", "A replay")

    def _draw_title(self) -> None:
        self._draw_paint_background()
        self._center("pigments", 54, 7)
        self._center("paint all tiles", 76, 12)
        self._center("dodge razor discs", 90, 8)
        for i, color in enumerate([10, 11, 12, 9, 14]):
            pyxel.circ(64 + i * 28, 130 + (i % 2) * 8, 10, color)
            pyxel.circb(64 + i * 28, 130 + (i % 2) * 8, 11, 7)
        self._center("A start", 210, 7 if pyxel.frame_count % 30 < 22 else 5)

    def _draw_paint_background(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        for i in range(18):
            color = [2, 3, 4, 5, 13][i % 5]
            pyxel.line(i * 16 - 40, SCREEN, i * 16 + 60, 0, color)

    def _draw_board(self) -> None:
        pyxel.rect(BOARD_X - 4, BOARD_Y - 4, TILE * self.core.width + 8, TILE * self.core.height + 8, 5)
        for y in range(self.core.height):
            for x in range(self.core.width):
                tile = (x, y)
                sx, sy = self._tile_screen(tile)
                color = 13 if tile in self.core.painted else 1
                if tile in self.core.walls:
                    color = 0
                elif tile in self.core.grass:
                    color = 3 if tile in self.core.painted else 11
                elif tile in self.core.water:
                    color = 12 if tile in self.core.painted else 5
                elif tile in self.core.triggers:
                    color = 10 if tile in self.core.painted else 4
                pyxel.rect(sx, sy, TILE - 1, TILE - 1, color)
                if tile in self.core.safe_tiles and tile not in self.core.painted:
                    pyxel.pset(sx + TILE // 2, sy + TILE // 2, 5)
                if tile in self.core.triggers:
                    pyxel.tri(sx + 5, sy + 15, sx + 10, sy + 4, sx + 15, sy + 15, 8)

    def _draw_actors(self) -> None:
        for droplet in self.core.droplets:
            sx, sy = self._tile_screen(droplet)
            pyxel.circ(sx + 10, sy + 10, 5, 14)
            pyxel.pset(sx + 8, sy + 8, 7)
        for disc in self.core.discs:
            sx, sy = self._tile_screen(disc)
            cx, cy = sx + 10, sy + 10
            pyxel.circ(cx, cy, 8, 6)
            pyxel.line(cx - 9, cy, cx + 9, cy, 7)
            pyxel.line(cx, cy - 9, cx, cy + 9, 7)
            pyxel.circ(cx, cy, 3, 0)
        px, py = self._tile_screen(self.core.player)
        color = 7 if self.core.player not in self.core.water else 12
        pyxel.circ(px + 10, py + 10, 7, color)
        pyxel.circb(px + 10, py + 10, 8, 0)
        pyxel.pset(px + 8, py + 8, 0)
        pyxel.pset(px + 12, py + 8, 0)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 26, 0)
        pyxel.text(6, 5, f"paint {int(self.core.painted_ratio * 100):3d}%", 7)
        pyxel.text(84, 5, f"pigment {self.core.pigment:02d}", 14)
        pyxel.text(170, 5, f"score {self.core.score:02d}", 10)
        pyxel.text(6, 16, self.core.message[:50], 13)
        pyxel.rect(0, 222, SCREEN, 18, 0)
        pyxel.text(28, 228, "D-pad paint  A wait  B/Start restart", 7)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(22, 90, 196, 58, 0)
        pyxel.rectb(22, 90, 196, 58, 7)
        self._center(title, 109, 10)
        self._center(subtitle, 130, 7)

    @staticmethod
    def _tile_screen(tile: tuple[int, int]) -> tuple[int, int]:
        return BOARD_X + tile[0] * TILE, BOARD_Y + tile[1] * TILE

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    Pigments()

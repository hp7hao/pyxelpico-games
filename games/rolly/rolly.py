"""Rolly - PyxelPico port.

Adapted from the PICO-8 cart by Davbo and Rory (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=31526
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from rolly_core import RollyCore, TILE  # noqa: E402


SCREEN = 240


class Rolly:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Rolly", fps=30)
        self.core = RollyCore()
        self.screen = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3e3g3", "t", "5", "n", 8)
        pyxel.sound(1).set("g3c4", "p", "6", "f", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 8)
        pyxel.sound(3).set("c4e4g4c5", "s", "5", "n", 12)

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if self.core.level_clear:
            if ih.btnp_a() or ih.btnp_start():
                self.core.restart()
            elif ih.btnp_select():
                self.screen = "title"
            return

        before_deaths = self.core.deaths
        if ih.btnp_a():
            if self.core.jump():
                pyxel.play(3, 0)
        if ih.btnp_b():
            direction = -1 if ih.btn_left() else 1 if ih.btn_right() else self.core.facing
            if self.core.roll(direction=direction):
                pyxel.play(3, 1)
        if ih.btnp_start():
            self.core.restart()
        self.core.tick(left=ih.btn_left(), right=ih.btn_right())
        if self.core.deaths > before_deaths:
            self.flash = 8
            pyxel.play(3, 2)
        if self.core.level_clear:
            pyxel.play(3, 3)

    def draw(self) -> None:
        pyxel.cls(8 if self.flash else 1)
        if self.screen == "title":
            self._draw_title()
            return
        self._draw_level()
        self._draw_player()
        self._draw_hud()
        if self.core.level_clear:
            self._panel("friends rescued", "A replay   Select title")

    def _draw_title(self) -> None:
        self._draw_cave_background()
        self._draw_ball(120, 122, 8, 10)
        self._center("ROLLY", 58, 7)
        self._center("jump roll hop dive", 82, 10)
        self._center("Davbo and Rory", 100, 13)
        self._center("A start", 210, 7 if pyxel.frame_count % 30 < 22 else 5)

    def _draw_level(self) -> None:
        self._draw_cave_background()
        for tile in self.core.solid:
            if tile == self.core.exit and self.core.exit_open:
                continue
            self._draw_tile(tile, 5)
        for tile in self.core.breakable:
            self._draw_tile(tile, 4)
        for tile in self.core.bouncy:
            self._draw_tile(tile, 11)
        for x, y in self.core.spikes:
            sx, sy = self._screen_tile(x, y)
            pyxel.tri(sx, sy + TILE, sx + TILE // 2, sy + 2, sx + TILE, sy + TILE, 8)
        for x, y in self.core.orbs:
            sx, sy = self._screen_tile(x, y)
            pyxel.circ(sx + 8, sy + 8, 5, 12)
            pyxel.circb(sx + 8, sy + 8, 6, 7)
        for x, y in self.core.friends:
            sx, sy = self._screen_tile(x, y)
            self._draw_ball(sx + 8, sy + 8, 5, 14)
        sx, sy = self._screen_tile(*self.core.exit)
        pyxel.rect(sx + 2, sy + 2, 12, 12, 3 if self.core.exit_open else 0)
        pyxel.rectb(sx + 2, sy + 2, 12, 12, 7)

    def _draw_cave_background(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        for y in range(32, SCREEN, 28):
            pyxel.line(0, y, SCREEN, y - 18, 13)

    def _draw_tile(self, tile: tuple[int, int], color: int) -> None:
        sx, sy = self._screen_tile(*tile)
        pyxel.rect(sx, sy, TILE, TILE, color)
        pyxel.rectb(sx, sy, TILE, TILE, 0)

    def _draw_player(self) -> None:
        self._draw_ball(int(self.core.x), int(self.core.y), 7, 10 if self.core.can_hop else 6)
        if abs(self.core.vx) > 2.5:
            pyxel.circb(int(self.core.x), int(self.core.y), 10, 7)

    def _draw_ball(self, x: int, y: int, radius: int, color: int) -> None:
        pyxel.circ(x, y, radius, color)
        pyxel.circb(x, y, radius, 0)
        pyxel.pset(x - 2, y - 2, 7)
        pyxel.pset(x + 2, y - 2, 7)
        pyxel.line(x - 3, y + 3, x + 3, y + 3, 0)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 24, 0)
        pyxel.text(6, 5, f"deaths {self.core.deaths} friends {self.core.friends_rescued}", 7)
        pyxel.text(148, 5, "hop ready" if self.core.can_hop else "need orb", 10)
        pyxel.text(6, 15, self.core.message[:48], 13)
        pyxel.rect(0, 222, SCREEN, 18, 0)
        pyxel.text(36, 228, "D-pad move  A jump  B roll/hop  Start retry", 7)

    @staticmethod
    def _screen_tile(x: int, y: int) -> tuple[int, int]:
        return x * TILE, y * TILE + 24

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 92, 192, 56, 0)
        pyxel.rectb(24, 92, 192, 56, 7)
        self._center(title, 111, 10)
        self._center(subtitle, 130, 7)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    Rolly()

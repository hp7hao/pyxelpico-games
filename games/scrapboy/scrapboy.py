"""Scrap Boy - PyxelPico port.

Adapted from the PICO-8 cart by BoneVolt (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=39800
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from scrapboy_core import ScrapBoyCore, TILE  # noqa: E402


SCREEN = 240


class ScrapBoy:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Scrap Boy", fps=30)
        self.core = ScrapBoyCore()
        self.screen = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3f3", "t", "5", "n", 6)
        pyxel.sound(1).set("g3c4e4", "p", "6", "f", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 10)
        pyxel.sound(3).set("c4e4g4c5", "s", "5", "n", 12)

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if self.core.level_clear or self.core.game_over:
            if ih.btnp_a() or ih.btnp_start():
                self.core.restart()
                self.flash = 4
            return
        if ih.btnp_a():
            if self.core.jump():
                pyxel.play(3, 0)
        if ih.btnp_b():
            dx = -1 if ih.btn_left() else 1 if ih.btn_right() else self.core.facing
            dy = -1 if ih.btn_up() else 1 if ih.btn_down() else 0
            if self.core.shoot(dx, dy):
                pyxel.play(3, 1)
        if ih.btnp_select():
            weapons = ["laser", "bomb", "magnet"]
            self.core.weapon = weapons[(weapons.index(self.core.weapon) + 1) % len(weapons)]
        if ih.btnp_start():
            self.core.restart()
        before_hp = self.core.hp
        self.core.tick(left=ih.btn_left(), right=ih.btn_right(), jump_held=ih.btn_a())
        if self.core.hp < before_hp:
            self.flash = 8
            pyxel.play(3, 2)

    def draw(self) -> None:
        pyxel.cls(8 if self.flash else 1)
        if self.screen == "title":
            self._draw_title()
            return
        self._draw_level()
        self._draw_player()
        self._draw_hud()
        if self.core.game_over:
            self._panel("scrapped", "A retry")
        elif self.core.level_clear:
            self._panel("scrap recovered", "A replay")

    def _draw_title(self) -> None:
        self._draw_factory_bg()
        self._center("SCRAP BOY", 58, 10)
        self._center("3 forms demo", 84, 7)
        self._draw_robot(120, 140)
        self._center("A start", 210, 7 if pyxel.frame_count % 30 < 22 else 5)

    def _draw_level(self) -> None:
        self._draw_factory_bg()
        for tile in self.core.solid:
            self._draw_tile(tile, 5)
        for tile in self.core.platforms:
            self._draw_tile(tile, 13)
        for tile in self.core.doors:
            self._draw_tile(tile, 4)
        for tile in self.core.spikes:
            sx, sy = self._tile_screen(tile)
            pyxel.tri(sx, sy + TILE, sx + TILE // 2, sy + 2, sx + TILE, sy + TILE, 8)
        for tile in self.core.scraps:
            sx, sy = self._tile_screen(tile)
            pyxel.circ(sx + 8, sy + 8, 4, 10)
            pyxel.circb(sx + 8, sy + 8, 5, 7)
        for tile, weapon in self.core.powerups.items():
            sx, sy = self._tile_screen(tile)
            pyxel.rect(sx + 3, sy + 3, 10, 10, {"laser": 12, "bomb": 9, "magnet": 14}.get(weapon, 7))
            pyxel.rectb(sx + 3, sy + 3, 10, 10, 0)
        for tile, hp in self.core.enemies.items():
            sx, sy = self._tile_screen(tile)
            pyxel.rect(sx + 3, sy + 4, 10, 10, 11 if hp == 1 else 2)
            pyxel.pset(sx + 6, sy + 7, 0)
            pyxel.pset(sx + 10, sy + 7, 0)
        self._draw_tile(self.core.exit, 3)

    def _draw_factory_bg(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        for x in range(0, SCREEN, 24):
            pyxel.line(x, 0, x - 30, SCREEN, 13)

    def _draw_tile(self, tile: tuple[int, int], color: int) -> None:
        sx, sy = self._tile_screen(tile)
        pyxel.rect(sx, sy, TILE, TILE, color)
        pyxel.rectb(sx, sy, TILE, TILE, 0)

    def _draw_player(self) -> None:
        self._draw_robot(int(self.core.x), int(self.core.y))

    def _draw_robot(self, x: int, y: int) -> None:
        color = {"laser": 12, "bomb": 9, "magnet": 14}.get(self.core.weapon, 7)
        pyxel.rect(x - 6, y - 12, 12, 20, color)
        pyxel.rect(x - 5, y - 18, 10, 8, 6)
        pyxel.pset(x - 2, y - 15, 7)
        pyxel.pset(x + 2, y - 15, 7)
        pyxel.line(x - 7, y - 4, x - 12, y + 2, color)
        pyxel.line(x + 7, y - 4, x + 12, y + 2, color)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 25, 0)
        pyxel.text(5, 5, f"hp {self.core.hp} scrap {self.core.scrap}", 7)
        pyxel.text(92, 5, f"weapon {self.core.weapon}", 10)
        pyxel.text(5, 16, self.core.message[:50], 13)
        pyxel.rect(0, 222, SCREEN, 18, 0)
        pyxel.text(20, 228, "D-pad move  A jump  B fire  Select form", 7)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 92, 192, 56, 0)
        pyxel.rectb(24, 92, 192, 56, 7)
        self._center(title, 111, 10)
        self._center(subtitle, 130, 7)

    @staticmethod
    def _tile_screen(tile: tuple[int, int]) -> tuple[int, int]:
        return tile[0] * TILE, tile[1] * TILE + 28

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    ScrapBoy()

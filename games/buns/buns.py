"""Buns: Bunny Survivor — PyxelPico port.

Adapted from the PICO-8 cart by unikotoast (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=48032
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from buns_core import BunsCore, Upgrade  # noqa: E402


SCREEN = 240
UPGRADES = (Upgrade.DAMAGE, Upgrade.HASTE, Upgrade.HEART)


class Buns:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Buns", fps=30)
        self.core = BunsCore()
        self.mode = "title"
        self.upgrade_index = 0
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3g3", "t", "6", "n", 8)
        pyxel.sound(1).set("e3a3c4", "p", "7", "n", 10)
        pyxel.sound(2).set("c2", "n", "7", "f", 16)

    def reset(self) -> None:
        self.core.reset()
        self.mode = "play"
        self.upgrade_index = 0
        self.flash = 0

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
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
        if self.core.awaiting_upgrade:
            if ih.btnp_left():
                self.upgrade_index = max(0, self.upgrade_index - 1)
                pyxel.play(3, 0)
            elif ih.btnp_right():
                self.upgrade_index = min(len(UPGRADES) - 1, self.upgrade_index + 1)
                pyxel.play(3, 0)
            elif ih.btnp_a() or ih.btnp_start():
                self.core.apply_upgrade(UPGRADES[self.upgrade_index])
                pyxel.play(3, 1)
            return

        dx = int(ih.btn_right()) - int(ih.btn_left())
        dy = int(ih.btn_down()) - int(ih.btn_up())
        self.core.move_player(dx, dy)
        prev_hp = self.core.player_hp
        prev_level = self.core.level
        prev_kills = self.core.kills
        self.core.tick()
        if self.core.player_hp < prev_hp:
            pyxel.play(3, 2)
            self.flash = 8
        elif self.core.level > prev_level:
            pyxel.play(3, 1)
        elif self.core.kills > prev_kills:
            pyxel.play(3, 0)
        if self.core.won:
            self.mode = "won"
        elif self.core.lost:
            self.mode = "lost"

    def draw(self) -> None:
        pyxel.cls(3 if self.flash == 0 else 8)
        if self.mode == "title":
            self._draw_title()
            return
        self._draw_field()
        for gem in self.core.gems:
            pyxel.dither(0.5)
            pyxel.circ(int(gem.x), int(gem.y), 4, 11)
            pyxel.dither(1)
        for bullet in self.core.bullets:
            pyxel.circ(int(bullet.x), int(bullet.y), 2, 10)
        for enemy in self.core.enemies:
            self._draw_enemy(enemy)
        self._draw_player()
        self._draw_hud()
        if self.core.awaiting_upgrade:
            self._draw_upgrade_panel()
        if self.mode == "won":
            self._panel("boss cleared", "A retry  B title")
        elif self.mode == "lost":
            self._panel("bunny down", "A retry  B title")

    def _draw_title(self) -> None:
        self._draw_field()
        self._draw_player_at(120, 103, 12)
        for x, y in ((80, 126), (154, 128), (126, 158)):
            self._draw_enemy_shape(x, y, 8, False)
        self._center("buns", 42, 10)
        self._center("bunny survivor", 56, 7)
        self._center("unikotoast", 68, 6)
        self._center("d-pad move", 182, 7)
        self._center("auto carrots, collect gems", 194, 7)
        if pyxel.frame_count % 30 < 22:
            self._center("press A", 214, 11)

    def _draw_field(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 3)
        for y in range(20, SCREEN, 20):
            pyxel.line(0, y, SCREEN, y, 11 if y % 40 else 5)
        for x in range(0, SCREEN, 20):
            pyxel.line(x, 20, x, SCREEN, 11 if x % 40 else 5)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 18, 0)
        pyxel.text(6, 5, f"time {self.core.timer // 30:03d}", 7)
        pyxel.text(72, 5, f"lvl {self.core.level}", 7)
        pyxel.text(120, 5, f"ko {self.core.kills}", 7)
        pyxel.text(174, 5, f"hp {self.core.player_hp}/{self.core.max_hp}", 7)
        pyxel.rect(6, 20, 70, 5, 5)
        pyxel.rect(7, 21, int(68 * self.core.exp / self.core.exp_needed), 3, 11)

    def _draw_player(self) -> None:
        color = 12 if not (self.core.iframes > 0 and pyxel.frame_count % 6 < 3) else 7
        self._draw_player_at(int(self.core.player_x), int(self.core.player_y), color)

    def _draw_player_at(self, x: int, y: int, color: int) -> None:
        pyxel.circ(x, y, 7, color)
        pyxel.elli(x - 5, y - 14, 4, 9, color)
        pyxel.elli(x + 5, y - 14, 4, 9, color)
        pyxel.pset(x - 2, y - 2, 0)
        pyxel.pset(x + 2, y - 2, 0)

    def _draw_enemy(self, enemy) -> None:
        self._draw_enemy_shape(int(enemy.x), int(enemy.y), 8 if not enemy.boss else 2, enemy.boss)

    def _draw_enemy_shape(self, x: int, y: int, color: int, boss: bool) -> None:
        radius = 18 if boss else 7
        pyxel.circ(x, y, radius, color)
        pyxel.pset(x - radius // 3, y - 2, 0)
        pyxel.pset(x + radius // 3, y - 2, 0)
        pyxel.line(x - radius, y + radius, x + radius, y + radius, 0)

    def _draw_upgrade_panel(self) -> None:
        pyxel.rect(18, 80, 204, 82, 0)
        pyxel.rectb(18, 80, 204, 82, 7)
        self._center("level up", 92, 11)
        labels = ["damage", "haste", "heart"]
        for index, label in enumerate(labels):
            x = 37 + index * 58
            color = 10 if index == self.upgrade_index else 6
            pyxel.rectb(x, 116, 48, 22, color)
            pyxel.text(x + 6, 124, label, color)
        self._center("left/right choose  A pick", 150, 6)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(28, 92, 184, 54, 0)
        pyxel.rectb(28, 92, 184, 54, 7)
        self._center(title, 108, 11)
        self._center(subtitle, 128, 6)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    Buns()

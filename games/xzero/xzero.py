"""X-Zero — PyxelPico port.

Adapted from the PICO-8 cart by paranoidcactus (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=36053
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from xzero_core import XZeroCore  # noqa: E402


SCREEN = 240


class XZero:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="X-Zero", fps=30)
        self.core = XZeroCore()
        self.mode = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c4", "t", "6", "n", 4)
        pyxel.sound(1).set("g3c4", "s", "7", "f", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 12)

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
        if self.mode in {"won", "lost"}:
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            elif ih.btnp_b() or ih.btnp_select():
                self.mode = "title"
            return

        direction = int(ih.btn_right()) - int(ih.btn_left())
        self.core.move(direction)
        self.core.aim_y = int(ih.btn_down()) - int(ih.btn_up())
        if ih.btnp_b():
            self.core.jump()
            pyxel.play(3, 0)
        if ih.btnp_a():
            self.core.shoot()
            pyxel.play(3, 1)
        hp = self.core.player_hp
        self.core.tick()
        if self.core.player_hp < hp:
            self.flash = 8
            pyxel.play(3, 2)
        if self.core.won:
            self.mode = "won"
        elif self.core.lost:
            self.mode = "lost"

    def draw(self) -> None:
        pyxel.cls(0 if self.flash == 0 else 8)
        if self.mode == "title":
            self._draw_title()
            return
        self._draw_world()
        self._draw_hud()
        if self.mode == "won":
            self._panel("x-zero clear", "A retry  B title")
        elif self.mode == "lost":
            self._panel("signal lost", "A retry  B title")

    def _draw_title(self) -> None:
        self._draw_backdrop()
        self._draw_player(120, 132)
        self._center("x-zero", 52, 10)
        self._center("platform shooter", 68, 6)
        self._center("d-pad move/aim", 184, 7)
        self._center("A shoot  B jump", 198, 7)
        self._center("press A", 216, 11)

    def _draw_world(self) -> None:
        self._draw_backdrop()
        pyxel.rect(0, int(self.core.ground_y) + 12, SCREEN, 44, 5)
        pyxel.line(0, int(self.core.ground_y) + 12, SCREEN, int(self.core.ground_y) + 12, 13)
        pyxel.rect(int(self.core.exit_x) - 5, int(self.core.ground_y) - 36, 10, 48, 10)
        pyxel.text(int(self.core.exit_x) - 7, int(self.core.ground_y) - 48, "exit", 10)
        for x, y in self.core.pickups:
            pyxel.circ(int(x), int(y) - 7, 4, 11)
        for shot in self.core.shots:
            pyxel.rect(int(shot.x) - 2, int(shot.y) - 1, 5, 3, 12)
        for enemy in self.core.enemies:
            if not enemy.dead:
                self._draw_enemy(int(enemy.x), int(enemy.y))
        self._draw_player(int(self.core.player_x), int(self.core.player_y))

    def _draw_backdrop(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 0)
        for y in range(28, 170, 18):
            pyxel.line(0, y, SCREEN, y, 1)
        for x in range(0, SCREEN, 24):
            pyxel.line(x, 28, x + 20, 170, 1)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 24, 0)
        pyxel.text(8, 6, f"zone {self.core.zone}", 7)
        pyxel.text(82, 6, f"score {self.core.score}", 7)
        pyxel.text(160, 6, "hp " + "*" * self.core.player_hp, 8 if self.core.player_hp <= 1 else 7)

    def _draw_player(self, x: int, y: int) -> None:
        pyxel.rect(x - 5, y - 20, 10, 20, 12)
        pyxel.rect(x - 7, y - 14, 14, 8, 1)
        pyxel.rect(x - 3, y - 27, 6, 8, 10)
        pyxel.line(x + self.core.facing * 5, y - 13, x + self.core.facing * 13, y - 13 - self.core.aim_y * 5, 10)

    def _draw_enemy(self, x: int, y: int) -> None:
        pyxel.rect(x - 8, y - 18, 16, 18, 8)
        pyxel.rectb(x - 8, y - 18, 16, 18, 2)
        pyxel.pset(x - 3, y - 12, 0)
        pyxel.pset(x + 3, y - 12, 0)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(28, 92, 184, 54, 0)
        pyxel.rectb(28, 92, 184, 54, 7)
        self._center(title, 108, 11)
        self._center(subtitle, 128, 6)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    XZero()

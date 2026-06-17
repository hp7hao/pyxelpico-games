"""Little Dragon Adventure - PyxelPico port.

Adapted from the PICO-8 cart by Mush (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=31469
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from littledragon_core import LittleDragonCore  # noqa: E402


SCREEN = 240
SCALE_X = 1.0
GROUND = 168


class LittleDragonAdventure:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Little Dragon Adventure", fps=30)
        self.core = LittleDragonCore()
        self.screen = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c4e4g4", "t", "5", "n", 8)
        pyxel.sound(1).set("g4c5", "s", "6", "f", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 10)
        pyxel.sound(3).set("e4g4c5e5", "p", "5", "n", 12)

    def reset(self) -> None:
        self.core.restart()
        self.screen = "play"
        self.flash = 0

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 0)
            return
        if self.core.cleared:
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            elif ih.btnp_select():
                self.screen = "title"
            return
        old_deaths = self.core.deaths
        old_eggs = self.core.eggs
        self.core.tick(
            left=ih.btn_left(),
            right=ih.btn_right(),
            jump=ih.btnp_a(),
            fire=ih.btn_b() or ih.btnp_b(),
        )
        if self.core.deaths > old_deaths:
            self.flash = 5
            pyxel.play(3, 2)
        elif self.core.eggs > old_eggs:
            pyxel.play(3, 3)
        elif ih.btnp_a() or ih.btnp_b():
            pyxel.play(3, 1)
        if ih.btnp_select():
            self.reset()

    def draw(self) -> None:
        pyxel.cls(8 if self.flash else 12)
        if self.screen == "title":
            self._draw_title()
            return
        self._draw_world()
        self._draw_entities()
        self._draw_hud()
        if self.core.cleared:
            self._panel("eggs saved", "A replay   Select title")

    def _draw_title(self) -> None:
        self._draw_background()
        self._draw_dragon(118, 148, 1)
        self._center("little dragon", 48, 7)
        self._center("adventure", 64, 10)
        self._center("Mush", 82, 6)
        self._center("A start", 210, 10 if pyxel.frame_count % 30 < 22 else 6)

    def _draw_world(self) -> None:
        self._draw_background()
        pyxel.rect(0, GROUND, SCREEN, 72, 3)
        for x in range(0, SCREEN, 16):
            pyxel.rect(x, GROUND, 14, 8, 11)
        pyxel.rect(self.core.checkpoint_x - 5, GROUND - 32, 10, 32, 6)
        pyxel.tri(self.core.checkpoint_x, GROUND - 44, self.core.checkpoint_x - 12, GROUND - 28, self.core.checkpoint_x + 12, GROUND - 28, 10)
        for hx, _ in self.core.hazards:
            pyxel.tri(int(hx - 6), GROUND, int(hx), GROUND - 16, int(hx + 6), GROUND, 8)
        pyxel.rect(int(self.core.boss.x - 10), GROUND - 42, 20, 42, 5)
        pyxel.text(int(self.core.boss.x - 14), GROUND - 54, "boss", 7)

    def _draw_background(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 12)
        for i in range(7):
            x = (i * 47 - pyxel.frame_count // 4) % 280 - 30
            y = 30 + (i * 23) % 90
            pyxel.circ(x, y, 9, 7)
            pyxel.circ(x + 10, y + 2, 7, 7)
            pyxel.rect(x - 8, y + 4, 28, 5, 7)

    def _draw_entities(self) -> None:
        self._draw_dragon(int(self.core.player.x), self._screen_y(self.core.player.y), self.core.player.facing)
        for ball in self.core.fireballs:
            pyxel.circ(int(ball.x), self._screen_y(ball.y), 3, 10)
        for enemy in self.core.enemies:
            if enemy.alive:
                self._draw_enemy(int(enemy.x), self._screen_y(enemy.y), enemy.kind)
        if not self.core.cleared:
            self._draw_enemy(int(self.core.boss.x), self._screen_y(self.core.boss.y) - 8, "boss")

    def _draw_dragon(self, x: int, y: int, facing: int) -> None:
        pyxel.circ(x, y - 12, 5, 11)
        pyxel.rect(x - 7, y - 8, 14, 10, 3)
        pyxel.tri(x - 6 * facing, y - 8, x - 22 * facing, y - 16, x - 10 * facing, y - 2, 10)
        pyxel.tri(x + 7 * facing, y - 13, x + 17 * facing, y - 10, x + 7 * facing, y - 7, 11)
        pyxel.line(x - 4, y + 2, x - 9, y + 8, 5)
        pyxel.line(x + 4, y + 2, x + 9, y + 8, 5)

    def _draw_enemy(self, x: int, y: int, kind: str) -> None:
        color = 2 if kind == "boss" else 13 if kind == "jelly" else 7
        pyxel.circ(x, y - 12, 7 if kind == "boss" else 5, color)
        pyxel.rect(x - 6, y - 8, 12, 10, color)
        if kind == "boss":
            pyxel.rect(x - 12, y - 22, 24, 5, 8)
        else:
            pyxel.line(x - 4, y + 2, x - 8, y + 8, 0)
            pyxel.line(x + 4, y + 2, x + 8, y + 8, 0)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 28, 0)
        pyxel.text(8, 6, f"eggs {self.core.eggs}/{self.core.total_eggs}", 10)
        pyxel.text(82, 6, f"deaths {self.core.deaths}", 7)
        pyxel.text(154, 6, f"boss {max(0, self.core.boss.hp)}", 8)
        pyxel.text(8, 18, self.core.message[:48], 13)
        pyxel.text(26, 224, "D-pad move  A jump/double  B fire  Select restart", 7)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(26, 90, 188, 58, 0)
        pyxel.rectb(26, 90, 188, 58, 7)
        self._center(title, 108, 10)
        self._center(subtitle, 128, 7)

    @staticmethod
    def _screen_y(world_y: float) -> int:
        return int(GROUND - (LittleDragonCore.floor_y - world_y))

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    LittleDragonAdventure()

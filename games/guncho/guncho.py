"""Guncho - PyxelPico port.

Adapted from the PICO-8 cart by spoike (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=48452
"""

from __future__ import annotations

import math
import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from guncho_core import GunchoCore  # noqa: E402


SCREEN = 240
HEX = 20
CX = 120
CY = 102
ACTIONS = ("move", "shoot", "punch", "hail", "wait")


class Guncho:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Guncho", fps=30)
        self.core = GunchoCore()
        self.screen = "title"
        self.action = 0
        self.direction = 0
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3e3g3", "t", "5", "n", 7)
        pyxel.sound(1).set("c2", "n", "7", "f", 8)
        pyxel.sound(2).set("g2c3", "s", "6", "f", 10)
        pyxel.sound(3).set("c4e4g4c5", "p", "5", "n", 12)

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if self.core.player_killed or self.core.won:
            if ih.btnp_a() or ih.btnp_start():
                self.core.restart()
                self.screen = "play"
                self.action = 0
                self.direction = 0
            elif ih.btnp_select():
                self.screen = "title"
            return

        if ih.btnp_left(hold=10, repeat=6):
            self.direction = (self.direction - 1) % 6
            self.core.aim = self.direction
        elif ih.btnp_right(hold=10, repeat=6):
            self.direction = (self.direction + 1) % 6
            self.core.aim = self.direction
        if ih.btnp_up(hold=10, repeat=8):
            self.action = (self.action - 1) % len(ACTIONS)
        elif ih.btnp_down(hold=10, repeat=8):
            self.action = (self.action + 1) % len(ACTIONS)
        if ih.btnp_a():
            self._perform_action()
        if ih.btnp_b():
            self.action = (self.action + 1) % len(ACTIONS)
        if ih.btnp_start():
            self.core.restart()

    def _perform_action(self) -> None:
        before_kills = self.core.bandits_killed
        action = ACTIONS[self.action]
        if action == "move":
            ok = self.core.move(self.direction)
        elif action == "shoot":
            ok = self.core.shoot(self.direction)
        elif action == "punch":
            ok = self.core.punch(self.direction)
        elif action == "hail":
            ok = self.core.bullet_hail()
        else:
            self.core.enemy_turn_pending = True
            self.core.message = "wait"
            ok = True
        if not ok:
            pyxel.play(3, 2)
            return
        pyxel.play(3, 1 if self.core.bandits_killed > before_kills else 0)
        self.flash = 4
        if self.core.enemy_turn_pending:
            self.core.perform_enemy_turn()
        if self.core.check_level_clear():
            if self.core.won:
                pyxel.play(3, 3)
            else:
                self.core.advance_level()
                pyxel.play(3, 3)

    def draw(self) -> None:
        pyxel.cls(9 if self.flash else 4)
        if self.screen == "title":
            self._draw_title()
            return
        self._draw_board()
        self._draw_hud()
        if self.core.player_killed:
            self._panel("shot down", "A retry   Select title")
        elif self.core.won:
            self._panel("bounty claimed", "A replay   Select title")

    def _draw_title(self) -> None:
        self._draw_sun(120, 72)
        self._draw_cowboy(120, 127, 7)
        self._center("GUNCHO", 46, 0)
        self._center("wild west roguelike", 70, 7)
        self._center("spoike", 90, 13)
        self._center("A start", 210, 0 if pyxel.frame_count % 30 < 22 else 5)

    def _draw_board(self) -> None:
        for cell in sorted(self.core.cells):
            x, y = self._cell_xy(cell)
            color = 10 if cell == self._target_cell() else 4
            pyxel.circ(x, y, 11, color)
            pyxel.circb(x, y, 11, 5)
        for dynamite in self.core.dynamites:
            if not dynamite.exploded:
                x, y = self._cell_xy(dynamite.pos)
                pyxel.rect(x - 5, y - 6, 10, 12, 8)
                pyxel.text(x - 2, y - 3, str(dynamite.timer), 7)
        for enemy in self.core.enemies:
            if not enemy.killed:
                x, y = self._cell_xy(enemy.pos)
                color = 2 if enemy.kind == "boss" else 8 if enemy.kind == "gun" else 12 if enemy.kind == "tnt" else 1
                self._draw_cowboy(x, y, color)
                if enemy.stun:
                    pyxel.text(x - 6, y - 18, "stun", 7)
        px, py = self._cell_xy(self.core.player)
        self._draw_cowboy(px, py, 7)
        tx, ty = self._cell_xy(self._target_cell())
        pyxel.line(px, py, tx, ty, 0)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 28, 0)
        pyxel.text(6, 5, f"camp {self.core.level}/5  bandits {self.core.bandits_killed}", 7)
        pyxel.text(6, 16, self.core.message[:36], 10)
        pyxel.text(128, 5, "bullets " + "".join("*" if b else "." for b in self.core.bullets), 7)
        pyxel.rect(0, 210, SCREEN, 30, 0)
        for i, name in enumerate(ACTIONS):
            color = 10 if i == self.action else 6
            pyxel.text(8 + i * 42, 216, name, color)
        pyxel.text(20, 228, "Left/Right aim  Up/Down action  A use  B next", 7)

    def _draw_sun(self, x: int, y: int) -> None:
        pyxel.circ(x, y, 36, 10)
        pyxel.circb(x, y, 38, 9)
        for yy in range(112, 180, 12):
            pyxel.line(0, yy, SCREEN, yy - 16, 5)

    def _draw_cowboy(self, x: int, y: int, color: int) -> None:
        pyxel.rect(x - 7, y - 8, 14, 5, color)
        pyxel.rect(x - 4, y - 13, 8, 5, color)
        pyxel.circ(x, y - 4, 5, 15)
        pyxel.rect(x - 5, y + 1, 10, 9, color)
        pyxel.line(x + 5, y + 3, x + 12, y + 1, 0)
        pyxel.pset(x - 2, y - 5, 0)
        pyxel.pset(x + 2, y - 5, 0)

    def _target_cell(self) -> tuple[int, int]:
        return self.core.neighbor(self.core.player, self.direction)

    @staticmethod
    def _cell_xy(cell: tuple[int, int]) -> tuple[int, int]:
        q, r = cell
        x = CX + int((q + r / 2) * HEX * 1.35)
        y = CY + int(r * HEX * 1.15)
        return x, y

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 92, 192, 56, 0)
        pyxel.rectb(24, 92, 192, 56, 7)
        self._center(title, 111, 10)
        self._center(subtitle, 130, 7)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    Guncho()

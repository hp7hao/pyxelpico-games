"""Shadows of Dunwich 2.0 - PyxelPico port.

Adapted from the PICO-8 cart by paranoidcactus (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=34047
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from shadowsofdunwich_core import Enemy, ShadowsOfDunwichCore, Soldier  # noqa: E402


SCREEN = 240
TILE = 22
OX = 10
OY = 34
ACTIONS = ("move", "shoot", "grenade", "watch")


class ShadowsOfDunwich:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Shadows of Dunwich", fps=30)
        self.core = ShadowsOfDunwichCore()
        self.screen = "title"
        self.cursor = self.core.soldiers[0].pos
        self.soldier_index = 0
        self.action_index = 0
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c2g2", "s", "5", "f", 8)
        pyxel.sound(1).set("c3d#3g3", "t", "6", "n", 9)
        pyxel.sound(2).set("g1c2", "n", "7", "f", 12)
        pyxel.sound(3).set("c2f2g#2c3", "p", "4", "n", 18)

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if self.core.victory or self.core.defeat:
            if ih.btnp_a() or ih.btnp_start():
                self.core.restart()
                self.cursor = self.core.soldiers[0].pos
                self.soldier_index = 0
                self.action_index = 0
                self.screen = "play"
            elif ih.btnp_select():
                self.screen = "title"
            return

        self._move_cursor()
        if ih.btnp_b():
            self._next_soldier()
        if ih.btnp_select():
            self.action_index = (self.action_index + 1) % len(ACTIONS)
        if ih.btnp_a():
            self._perform_action()
        if ih.btnp_start():
            if self.core.living_enemies():
                self.core.enemy_turn()
                pyxel.play(3, 2)
            else:
                self.core.complete_battle()
                pyxel.play(3, 3)

    def _move_cursor(self) -> None:
        x, y = self.cursor
        if ih.btnp_left(hold=10, repeat=4):
            x -= 1
        elif ih.btnp_right(hold=10, repeat=4):
            x += 1
        if ih.btnp_up(hold=10, repeat=4):
            y -= 1
        elif ih.btnp_down(hold=10, repeat=4):
            y += 1
        self.cursor = (max(0, min(self.core.width - 1, x)), max(0, min(self.core.height - 1, y)))

    def _next_soldier(self) -> None:
        for offset in range(1, len(self.core.soldiers) + 1):
            index = (self.soldier_index + offset) % len(self.core.soldiers)
            if self.core.soldiers[index].alive:
                self.soldier_index = index
                self.cursor = self.core.soldiers[index].pos
                self.core.selected = index
                return

    def _perform_action(self) -> None:
        before = sum(enemy.dead for enemy in self.core.enemies)
        action = ACTIONS[self.action_index]
        if action == "move":
            ok = self.core.move_soldier(self.soldier_index, self.cursor)
        elif action == "shoot":
            ok = self.core.shoot(self.soldier_index, self.cursor)
        elif action == "grenade":
            ok = self.core.grenade(self.soldier_index, self.cursor)
        else:
            ok = self.core.overwatch(self.soldier_index)
        if ok:
            self.flash = 3
            pyxel.play(3, 1 if sum(enemy.dead for enemy in self.core.enemies) > before else 0)
            if not self.core.living_enemies():
                self.core.complete_battle()
        else:
            pyxel.play(3, 2)

    def draw(self) -> None:
        pyxel.cls(1 if self.flash else 0)
        if self.screen == "title":
            self._draw_title()
            return
        self._draw_map()
        self._draw_units()
        self._draw_hud()
        if self.core.victory:
            self._panel("dunwich sealed", "A replay   Select title")
        elif self.core.defeat:
            self._panel("squad lost", "A retry   Select title")

    def _draw_title(self) -> None:
        for y in range(0, SCREEN, 16):
            pyxel.line(0, y, SCREEN, y + 34, 5)
        pyxel.circ(122, 86, 35, 13)
        pyxel.circb(122, 86, 38, 7)
        self._center("SHADOWS", 54, 7)
        self._center("OF DUNWICH", 68, 10)
        self._center("turn-based squad tactics", 112, 6)
        self._center("paranoidcactus", 128, 13)
        self._center("A start", 210, 7 if pyxel.frame_count % 40 < 28 else 5)

    def _draw_map(self) -> None:
        for y in range(self.core.height):
            for x in range(self.core.width):
                sx, sy = self._cell_xy((x, y))
                color = 5 if (x, y) in self.core.walls else 3 if (x + y) % 2 else 4
                pyxel.rect(sx, sy, TILE - 1, TILE - 1, color)
                pyxel.rectb(sx, sy, TILE - 1, TILE - 1, 0)
        cx, cy = self._cell_xy(self.cursor)
        pyxel.rectb(cx - 1, cy - 1, TILE + 1, TILE + 1, 10)

    def _draw_units(self) -> None:
        for enemy in self.core.enemies:
            if not enemy.dead:
                self._draw_enemy(enemy)
        for index, soldier in enumerate(self.core.soldiers):
            if soldier.alive:
                self._draw_soldier(soldier, index == self.soldier_index)

    def _draw_soldier(self, soldier: Soldier, selected: bool) -> None:
        x, y = self._cell_center(soldier.pos)
        color = 12 if selected else 6
        pyxel.circ(x, y - 4, 5, 15)
        pyxel.rect(x - 6, y, 12, 10, color)
        pyxel.line(x + 4, y + 3, x + 12, y, 7)
        pyxel.text(x - 7, y + 12, soldier.name[0], 7)

    def _draw_enemy(self, enemy: Enemy) -> None:
        x, y = self._cell_center(enemy.pos)
        color = 8 if enemy.kind == "cultist" else 2 if enemy.kind == "splitter" else 13 if enemy.kind == "seer" else 9
        pyxel.tri(x, y - 9, x - 8, y + 8, x + 8, y + 8, color)
        pyxel.rect(x - 3, y - 1, 6, 4, 0)
        if enemy.kind == "spawn":
            pyxel.circ(x, y, 4, 2)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 30, 0)
        pyxel.text(5, 5, f"battle {self.core.battle}  level {self.core.campaign_level}/16", 7)
        pyxel.text(5, 17, self.core.message[:42], 10)
        soldier = self.core.soldiers[self.soldier_index]
        pyxel.rect(0, 212, SCREEN, 28, 0)
        pyxel.text(5, 216, f"{soldier.name} hp {soldier.hp} ap {soldier.ap} lv {soldier.level}", 7)
        for index, action in enumerate(ACTIONS):
            color = 10 if index == self.action_index else 6
            pyxel.text(5 + index * 56, 228, action, color)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 94, 192, 52, 0)
        pyxel.rectb(24, 94, 192, 52, 7)
        self._center(title, 112, 10)
        self._center(subtitle, 130, 7)

    @staticmethod
    def _cell_xy(pos: tuple[int, int]) -> tuple[int, int]:
        return OX + pos[0] * TILE, OY + pos[1] * TILE

    @staticmethod
    def _cell_center(pos: tuple[int, int]) -> tuple[int, int]:
        x, y = ShadowsOfDunwich._cell_xy(pos)
        return x + TILE // 2, y + TILE // 2

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    ShadowsOfDunwich()

"""Freezing Knights - PyxelPico port.

Adapted from the PICO-8 multicart RPG by tinyevilwizard (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=50683
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from freezingknights_core import Enemy, FreezingKnightsCore  # noqa: E402


SCREEN = 240


class FreezingKnights:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Freezing Knights", fps=30)
        self.core = FreezingKnightsCore()
        self.screen = "title"
        self.path_cursor = 0
        self.knight_cursor = 0
        self.enemy_cursor = 0
        self.guard_meter = 0.0
        self.guard_dir = 1
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3e3g3c4", "t", "5", "n", 12)
        pyxel.sound(1).set("g4c5", "s", "6", "f", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 10)
        pyxel.sound(3).set("e4g4b4", "p", "5", "n", 8)

    def reset(self) -> None:
        self.core.restart()
        self.screen = "map"
        self.path_cursor = 0
        self.knight_cursor = 0
        self.enemy_cursor = 0
        self.guard_meter = 0.0

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "map"
                pyxel.play(3, 0)
            return
        if self.core.mode == "clear":
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            elif ih.btnp_select():
                self.screen = "title"
            return
        if self.core.mode == "rest":
            self._update_rest()
        elif self.core.mode == "battle":
            self._update_battle()
        else:
            self._update_map()

    def _update_map(self) -> None:
        paths = self.core.available_paths()
        if ih.btnp_up() or ih.btnp_left():
            self.path_cursor = max(0, self.path_cursor - 1)
        if ih.btnp_down() or ih.btnp_right():
            self.path_cursor = min(max(0, len(paths) - 1), self.path_cursor + 1)
        if ih.btnp_a() and paths:
            self.core.choose_path(self.path_cursor)
            self.path_cursor = 0
            self.enemy_cursor = 0
            pyxel.play(3, 3 if self.core.mode == "battle" else 0)

    def _update_rest(self) -> None:
        if ih.btnp_left() or ih.btnp_right():
            self.knight_cursor = 1 - self.knight_cursor
        if ih.btnp_up():
            self.core.buy_upgrade(self.knight_cursor, "attack")
            pyxel.play(3, 1)
        if ih.btnp_down():
            self.core.buy_upgrade(self.knight_cursor, "hp")
            pyxel.play(3, 1)
        if ih.btnp_a() or ih.btnp_start():
            self.core.rest()
            self.path_cursor = 0
            pyxel.play(3, 0)

    def _update_battle(self) -> None:
        self.guard_meter += 0.035 * self.guard_dir
        if self.guard_meter >= 1.0 or self.guard_meter <= 0.0:
            self.guard_meter = max(0.0, min(1.0, self.guard_meter))
            self.guard_dir *= -1
        living = [index for index, enemy in enumerate(self.core.enemies) if enemy.alive]
        if living:
            if ih.btnp_left():
                self.enemy_cursor = max(0, self.enemy_cursor - 1)
            if ih.btnp_right():
                self.enemy_cursor = min(len(living) - 1, self.enemy_cursor + 1)
        if ih.btnp_up() or ih.btnp_down():
            self.knight_cursor = 1 - self.knight_cursor
        if ih.btnp_a():
            target = living[min(self.enemy_cursor, max(0, len(living) - 1))] if living else 0
            before_mode = self.core.mode
            self.core.knight_action(self.knight_cursor, "strike", target)
            pyxel.play(3, 1)
            if before_mode == "battle" and self.core.mode == "battle":
                self.core.enemy_turn(self.guard_meter)
                self.flash = 3
        if ih.btnp_b():
            self.core.use_potion(self.knight_cursor)
            pyxel.play(3, 0)
        if ih.btnp_select():
            self.core.enemy_turn(self.guard_meter)
            self.flash = 3

    def draw(self) -> None:
        pyxel.cls(5 if self.flash else 1)
        self._draw_snow()
        if self.screen == "title":
            self._draw_title()
        elif self.core.mode == "rest":
            self._draw_rest()
        elif self.core.mode == "battle":
            self._draw_battle()
        elif self.core.mode == "clear":
            self._draw_clear()
        else:
            self._draw_map()

    def _draw_title(self) -> None:
        self._draw_mountain(0)
        self._center("freezing knights", 54, 7)
        self._center("tinyevilwizard", 70, 12)
        self._draw_knight(86, 150, 12, 6)
        self._draw_knight(154, 150, 10, 8)
        self._center("A start", 210, 10 if pyxel.frame_count % 30 < 22 else 6)

    def _draw_map(self) -> None:
        self._draw_mountain(self.core.current_node_index)
        self._draw_party_status(8, 8)
        self._center(self.core.current_node.name, 58, 7)
        paths = self.core.available_paths()
        for row, node_index in enumerate(paths):
            node = self.core.nodes[node_index]
            y = 92 + row * 28
            color = 10 if row == self.path_cursor else 6
            pyxel.rect(34, y - 5, 172, 20, 0)
            pyxel.rectb(34, y - 5, 172, 20, color)
            pyxel.text(44, y, f"{node.kind}: {node.name}", color)
        pyxel.text(42, 202, "D-pad choose   A travel", 7)
        pyxel.text(8, 224, self.core.message[:48], 13)

    def _draw_rest(self) -> None:
        self._draw_mountain(self.core.current_node_index)
        self._center(self.core.current_node.name, 42, 10)
        self._draw_party_status(8, 76)
        for index, knight in enumerate(self.core.party):
            x = 72 + index * 92
            self._draw_knight(x, 142, 12 if index == 0 else 10, 6 if index == 0 else 8)
            if index == self.knight_cursor:
                pyxel.rectb(x - 18, 112, 36, 48, 10)
        pyxel.text(38, 184, f"gold {self.core.gold}  upgrade {self.core.upgrade_cost}g", 7)
        pyxel.text(36, 198, "Up attack  Down hp  A rest", 6)
        pyxel.text(8, 224, self.core.message[:48], 13)

    def _draw_battle(self) -> None:
        self._draw_party_status(8, 8)
        for index, knight in enumerate(self.core.party):
            self._draw_knight(54 + index * 52, 154, 12 if index == 0 else 10, 6 if index == 0 else 8)
            self._draw_hp_bar(32 + index * 58, 164, 42, knight.hp, knight.max_hp, 8)
            if index == self.knight_cursor:
                pyxel.tri(48 + index * 52, 174, 60 + index * 52, 174, 54 + index * 52, 166, 10)
        living = [enemy for enemy in self.core.enemies if enemy.alive]
        for index, enemy in enumerate(living):
            x = 138 + index * 42
            self._draw_enemy(enemy, x, 116)
            self._draw_hp_bar(x - 16, 130, 34, enemy.hp, enemy.max_hp, 11)
            if index == self.enemy_cursor:
                pyxel.rectb(x - 21, 84, 42, 52, 10)
        pyxel.rect(36, 194, 168, 8, 0)
        pyxel.rectb(36, 194, 168, 8, 7)
        pyxel.rect(38, 196, int(164 * self.guard_meter), 4, 10)
        pyxel.text(40, 207, "A strike  B potion  Select defend", 7)
        pyxel.text(8, 224, self.core.message[:48], 13)

    def _draw_clear(self) -> None:
        self._draw_mountain(6)
        self._center("summit saved", 76, 10)
        self._center("A replay   Select title", 104, 7)
        self._draw_knight(96, 156, 12, 6)
        self._draw_knight(144, 156, 10, 8)

    def _draw_party_status(self, x: int, y: int) -> None:
        pyxel.rect(x - 2, y - 2, 142, 34, 0)
        for index, knight in enumerate(self.core.party):
            ky = y + index * 13
            pyxel.text(x, ky, f"{knight.name[:5]} {knight.hp}/{knight.max_hp} st{knight.stamina}", 7)
        pyxel.text(x + 82, y, f"pot {self.core.potions}", 10)
        pyxel.text(x + 82, y + 13, f"gold {self.core.gold}", 6)

    def _draw_mountain(self, node_index: int) -> None:
        pyxel.tri(20, 196, 118, 34, 220, 196, 6)
        pyxel.tri(75, 104, 118, 34, 160, 104, 7)
        for index, node in enumerate(self.core.nodes):
            x = 44 + (index * 31) % 152
            y = 184 - index * 21
            color = 10 if index == node_index else 13 if node.kind == "rest" else 7
            pyxel.circ(x, y, 4, color)
            if index > 0:
                px = 44 + ((index - 1) * 31) % 152
                py = 184 - (index - 1) * 21
                pyxel.line(px, py, x, y, 13)

    def _draw_snow(self) -> None:
        for i in range(34):
            x = (i * 37 + pyxel.frame_count // 2) % 250 - 5
            y = (i * 19 + pyxel.frame_count) % 240
            pyxel.pset(x, y, 7)

    def _draw_knight(self, x: int, y: int, cloak: int, armor: int) -> None:
        pyxel.circ(x, y - 18, 5, 15)
        pyxel.rect(x - 6, y - 13, 12, 16, cloak)
        pyxel.rect(x - 4, y - 10, 8, 9, armor)
        pyxel.line(x + 6, y - 9, x + 15, y - 15, 7)
        pyxel.line(x - 3, y + 3, x - 7, y + 9, 0)
        pyxel.line(x + 3, y + 3, x + 7, y + 9, 0)

    def _draw_enemy(self, enemy: Enemy, x: int, y: int) -> None:
        pyxel.circ(x, y - 14, 8, 13)
        pyxel.rect(x - 10, y - 8, 20, 20, 5)
        pyxel.text(x - min(20, len(enemy.name) * 2), y + 16, enemy.name[:10], 7)

    @staticmethod
    def _draw_hp_bar(x: int, y: int, w: int, hp: int, max_hp: int, color: int) -> None:
        pyxel.rect(x, y, w, 5, 0)
        pyxel.rect(x, y, max(1, int(w * hp / max_hp)), 5, color)
        pyxel.rectb(x, y, w, 5, 7)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    FreezingKnights()

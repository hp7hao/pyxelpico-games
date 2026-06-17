"""Trial of the Sorcerer - PyxelPico port.

Adapted from the PICO-8 cart by Mot (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=43833
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from trialsorcerer_core import DIRS, TrialSorcererCore  # noqa: E402


SCREEN = 240
VIEW_TOP = 34
VIEW_H = 142
TILE = 9


class TrialSorcerer:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Trial of the Sorcerer", fps=30)
        self.core = TrialSorcererCore()
        self.screen = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3g3c4", "t", "6", "n", 9)
        pyxel.sound(1).set("g4c5", "s", "6", "f", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 10)
        pyxel.sound(3).set("e3g3b3e4", "p", "5", "n", 12)

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

        old_message = self.core.message
        old_hp = self.core.hp
        self.core.tick(
            forward=ih.btnp_up(hold=7, repeat=5),
            backward=ih.btnp_down(hold=7, repeat=5),
            turn_left=ih.btnp_left(hold=7, repeat=5),
            turn_right=ih.btnp_right(hold=7, repeat=5),
            strafe=ih.btn_b(),
            shoot=ih.btnp_a(),
        )
        if self.core.hp < old_hp:
            self.flash = 5
            pyxel.play(3, 2)
        elif self.core.message != old_message:
            if "banished" in self.core.message or "defeated" in self.core.message:
                pyxel.play(3, 1)
            elif "key" in self.core.message or "power" in self.core.message:
                pyxel.play(3, 3)
        if ih.btnp_select():
            self.reset()

    def draw(self) -> None:
        pyxel.cls(2 if self.flash else 0)
        if self.screen == "title":
            self._draw_title()
            return
        self._draw_view()
        self._draw_weapon()
        self._draw_minimap()
        self._draw_hud()
        if self.core.cleared:
            self._panel("bahmott defeated", "A replay   Select title")

    def _draw_title(self) -> None:
        self._draw_stone_backdrop()
        pyxel.circ(120, 112, 26, 5)
        pyxel.circb(120, 112, 28, 8)
        pyxel.line(120, 74, 120, 148, 10)
        pyxel.circ(120, 70, 5, 11)
        self._center("trial of the", 50, 7)
        self._center("sorcerer", 66, 10)
        self._center("Mot", 86, 6)
        self._center("A start", 208, 10 if pyxel.frame_count % 30 < 22 else 6)

    def _draw_stone_backdrop(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        for y in range(0, SCREEN, 20):
            for x in range((-y // 2) % 24 - 24, SCREEN, 24):
                pyxel.rectb(x, y, 24, 20, 5)

    def _draw_view(self) -> None:
        pyxel.rect(0, VIEW_TOP, SCREEN, VIEW_H, 1)
        pyxel.rect(0, VIEW_TOP, SCREEN, VIEW_H // 2, 5)
        pyxel.rect(0, VIEW_TOP + VIEW_H // 2, SCREEN, VIEW_H // 2, 3)
        for index, offset in enumerate((-1, 0, 1)):
            dist, tile = self.core.visible_ray(offset)
            width = max(20, 124 - dist * 17)
            height = max(22, 118 - dist * 15)
            cx = 120 + (index - 1) * (40 + dist * 4)
            y = VIEW_TOP + (VIEW_H - height) // 2
            color = 4 if tile == "D" else 13 if dist <= 2 else 5
            pyxel.rect(cx - width // 2, y, width, height, color)
            pyxel.rectb(cx - width // 2, y, width, height, 0)
            if tile == "D":
                pyxel.circ(cx + width // 5, y + height // 2, 3, 10)
        self._draw_visible_sprites()

    def _draw_visible_sprites(self) -> None:
        dx, dy = DIRS[self.core.facing]
        for monster in self.core.monsters:
            if not monster.alive:
                continue
            relx = monster.x - self.core.x
            rely = monster.y - self.core.y
            ahead = relx * dx + rely * dy
            side = relx * -dy + rely * dx
            if ahead <= 0 or ahead > 5 or abs(side) > 2:
                continue
            size = max(10, 46 - ahead * 6)
            x = 120 + side * 34 - size // 2
            y = VIEW_TOP + 96 - size
            self._draw_monster(x, y, size, monster.kind)
        for (x, y), kind in self.core.pickups.items():
            relx = x - self.core.x
            rely = y - self.core.y
            ahead = relx * dx + rely * dy
            side = relx * -dy + rely * dx
            if 0 < ahead <= 4 and abs(side) <= 1:
                sx = 120 + side * 40
                sy = VIEW_TOP + 104 - ahead * 7
                self._draw_pickup(sx, sy, kind)

    def _draw_monster(self, x: int, y: int, size: int, kind: str) -> None:
        color = 8 if kind == "bahmott" else 2 if kind == "spider" else 13
        pyxel.circ(x + size // 2, y + size // 3, size // 3, color)
        pyxel.rect(x + size // 4, y + size // 2, size // 2, size // 3, color)
        pyxel.circ(x + size // 2 - 5, y + size // 3, 2, 10)
        pyxel.circ(x + size // 2 + 5, y + size // 3, 2, 10)

    def _draw_pickup(self, x: int, y: int, kind: str) -> None:
        color = {"key": 10, "crystal": 12, "potion": 8}[kind]
        pyxel.circ(x, y, 5, color)
        pyxel.circb(x, y, 6, 7)

    def _draw_weapon(self) -> None:
        pyxel.line(120, 156, 132, 210, 4)
        pyxel.line(123, 156, 135, 210, 10)
        pyxel.circ(120, 152, 5 + self.core.staff_power, 12)
        if pyxel.frame_count % 20 < 10:
            pyxel.circb(120, 152, 9 + self.core.staff_power, 10)

    def _draw_minimap(self) -> None:
        ox, oy = 9, 184
        for y, row in enumerate(self.core.grid):
            for x, tile in enumerate(row):
                color = 5 if tile == "#" else 4 if tile == "D" else 10 if tile == "E" else 1
                pyxel.rect(ox + x * TILE, oy + y * TILE, TILE - 1, TILE - 1, color)
        px = ox + self.core.x * TILE + 4
        py = oy + self.core.y * TILE + 4
        pyxel.circ(px, py, 3, 11)
        dx, dy = DIRS[self.core.facing]
        pyxel.line(px, py, px + dx * 5, py + dy * 5, 7)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 30, 0)
        pyxel.text(8, 6, f"lv {self.core.level}/{self.core.final_level}", 7)
        pyxel.text(58, 6, f"hp {self.core.hp}/{self.core.max_hp}", 8)
        pyxel.text(116, 6, f"key {self.core.keys}", 10)
        pyxel.text(164, 6, f"staff {self.core.staff_power}", 12)
        pyxel.text(8, 18, self.core.message[:52], 13)
        pyxel.text(114, 190, "Up/Down move", 7)
        pyxel.text(114, 202, "Left/Right turn", 7)
        pyxel.text(114, 214, "Hold B strafe", 6)
        pyxel.text(114, 226, "A staff  Select restart", 10)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 91, 192, 58, 0)
        pyxel.rectb(24, 91, 192, 58, 7)
        self._center(title, 110, 10)
        self._center(subtitle, 130, 7)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    TrialSorcerer()

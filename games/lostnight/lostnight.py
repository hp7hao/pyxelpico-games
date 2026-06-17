"""The Lost Night - PyxelPico port.

Adapted from the PICO-8 cart by arlefreak (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=41791
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from lostnight_core import LostNightCore  # noqa: E402


SCREEN = 240
SCALE = 2
OX = 24
OY = 34


class LostNight:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="The Lost Night", fps=30)
        self.core = LostNightCore()
        self.screen = "title"
        self.shop_cursor = 0
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3g3c4", "t", "5", "n", 12)
        pyxel.sound(1).set("c4e4g4", "p", "6", "f", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 10)
        pyxel.sound(3).set("g4f4d4c4", "s", "5", "n", 10)

    def reset(self) -> None:
        self.core.restart()
        self.screen = "overworld"
        self.shop_cursor = 0
        self.flash = 0

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "overworld"
                pyxel.play(3, 0)
            return
        if self.core.mode == "clear":
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            elif ih.btnp_select():
                self.screen = "title"
            return
        if self.screen == "shop":
            self._update_shop()
            return
        if self.core.mode == "battle":
            self._update_battle()
        else:
            self._update_overworld()

    def _update_overworld(self) -> None:
        old_mode = self.core.mode
        self.core.tick_overworld(
            left=ih.btn_left(),
            right=ih.btn_right(),
            up=ih.btn_up(),
            down=ih.btn_down(),
        )
        if old_mode != self.core.mode:
            pyxel.play(3, 3)
        if ih.btnp_b():
            self.core.drink_tea()
            pyxel.play(3, 0)
        if ih.btnp_select():
            self.screen = "shop"

    def _update_battle(self) -> None:
        old_hp = self.core.hp
        self.core.tick_battle(
            left=ih.btn_left(),
            right=ih.btn_right(),
            up=ih.btn_up(),
            down=ih.btn_down(),
        )
        if ih.btnp_a():
            self.core.fire()
            pyxel.play(3, 1)
        if ih.btnp_b():
            self.core.drink_tea()
            pyxel.play(3, 0)
        if self.core.hp < old_hp:
            self.flash = 4
            pyxel.play(3, 2)
        if self.core.mode != "battle":
            pyxel.play(3, 3)

    def _update_shop(self) -> None:
        items = ("power", "speed", "rate", "hp")
        if ih.btnp_up():
            self.shop_cursor = (self.shop_cursor - 1) % len(items)
        if ih.btnp_down():
            self.shop_cursor = (self.shop_cursor + 1) % len(items)
        if ih.btnp_a():
            self.core.buy_upgrade(items[self.shop_cursor])
            pyxel.play(3, 1)
        if ih.btnp_b() or ih.btnp_select() or ih.btnp_start():
            self.screen = "overworld"

    def draw(self) -> None:
        pyxel.cls(8 if self.flash else 0)
        if self.screen == "title":
            self._draw_title()
        elif self.core.mode == "clear":
            self._draw_clear()
        elif self.screen == "shop":
            self._draw_shop()
        elif self.core.mode == "battle":
            self._draw_battle()
        else:
            self._draw_overworld()

    def _draw_title(self) -> None:
        self._draw_stars()
        self._center("the lost night", 58, 7)
        self._center("arlefreak", 74, 13)
        pyxel.rect(82, 138, 76, 16, 5)
        self._draw_player(120, 144)
        self._center("A start", 210, 10 if pyxel.frame_count % 30 < 22 else 6)

    def _draw_overworld(self) -> None:
        self._draw_room()
        self._draw_player(OX + int(self.core.player.x * SCALE), OY + int(self.core.player.y * SCALE))
        for room in self.core.encounter_rooms:
            if room not in self.core.cleared_rooms:
                x = OX + room[0] * 40 + 22
                y = OY + room[1] * 44 + 22
                pyxel.circ(x, y, 4, 8 if pyxel.frame_count % 20 < 10 else 2)
        self._draw_hud()
        pyxel.text(14, 214, "D-pad move  B tea  Select shop", 7)

    def _draw_battle(self) -> None:
        self._draw_stars()
        pyxel.rect(28, 70, 184, 102, 1)
        pyxel.rectb(28, 70, 184, 102, 7)
        self._draw_enemy(120, 96)
        self._draw_player(28 + int(self.core.player.x * 1.9), 70 + int(self.core.player.y * 1.35))
        for bullet in self.core.enemy_bullets:
            pyxel.circ(28 + int(bullet.x * 1.9), 70 + int(bullet.y * 1.35), 3, 10)
        for bullet in self.core.player_bullets:
            pyxel.circ(28 + int(bullet.x * 1.9), 70 + int(bullet.y * 1.35), 2, 11)
        self._draw_hud()
        pyxel.text(26, 190, f"{self.core.enemy.name} hp {self.core.enemy.hp}", 13)
        pyxel.text(26, 204, "A fire  B tea  dodge sparks", 7)
        pyxel.text(8, 224, self.core.message[:48], 10)

    def _draw_shop(self) -> None:
        self._draw_stars()
        pyxel.rect(34, 44, 172, 150, 1)
        pyxel.rectb(34, 44, 172, 150, 7)
        self._center("candy shop", 58, 10)
        stats = {
            "power": self.core.power_level,
            "speed": self.core.speed_level,
            "rate": self.core.rate_level,
            "hp": self.core.max_hp,
        }
        for index, item in enumerate(("power", "speed", "rate", "hp")):
            y = 86 + index * 22
            color = 10 if index == self.shop_cursor else 7
            pyxel.text(62, y, f"{item:<5} {stats[item]}   4 candy", color)
        pyxel.text(62, 178, f"candy {self.core.candy}", 6)
        pyxel.text(44, 210, "A buy  B/Select back", 7)
        pyxel.text(8, 224, self.core.message[:48], 10)

    def _draw_clear(self) -> None:
        pyxel.cls(12)
        pyxel.circ(120, 84, 38, 10)
        pyxel.rect(0, 120, SCREEN, 120, 3)
        self._center("dawn returns", 62, 0)
        self._center("A replay   Select title", 196, 7)
        self._draw_player(120, 150)

    def _draw_room(self) -> None:
        pyxel.rect(OX, OY, self.core.room_w * SCALE, self.core.room_h * SCALE, 1)
        pyxel.rectb(OX, OY, self.core.room_w * SCALE, self.core.room_h * SCALE, 7)
        rx, ry = self.core.room
        pyxel.text(OX + 6, OY + 6, f"room {rx},{ry}", 6)
        for i in range(12):
            x = OX + (i * 19 + rx * 13) % (self.core.room_w * SCALE)
            y = OY + (i * 29 + ry * 17) % (self.core.room_h * SCALE)
            pyxel.pset(x, y, 13)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 28, 0)
        pyxel.text(8, 6, f"hp {self.core.hp}/{self.core.max_hp}", 7)
        pyxel.text(72, 6, f"tea {self.core.tea}", 10)
        pyxel.text(124, 6, f"candy {self.core.candy}", 6)
        pyxel.text(8, 18, self.core.message[:48], 13)

    def _draw_stars(self) -> None:
        for i in range(60):
            x = (i * 43 + pyxel.frame_count // 2) % 240
            y = (i * 31 + pyxel.frame_count // 3) % 240
            pyxel.pset(x, y, 7 if i % 3 else 13)

    @staticmethod
    def _draw_player(x: int, y: int) -> None:
        pyxel.circ(x, y - 10, 4, 15)
        pyxel.rect(x - 4, y - 6, 8, 12, 11)
        pyxel.line(x - 3, y + 6, x - 7, y + 12, 5)
        pyxel.line(x + 3, y + 6, x + 7, y + 12, 5)

    @staticmethod
    def _draw_enemy(x: int, y: int) -> None:
        pyxel.circ(x, y, 17, 2)
        pyxel.circ(x - 6, y - 4, 2, 10)
        pyxel.circ(x + 6, y - 4, 2, 10)
        pyxel.rect(x - 7, y + 7, 14, 3, 8)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    LostNight()

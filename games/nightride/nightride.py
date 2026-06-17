"""Night Ride - PyxelPico port.

Adapted from the PICO-8 cart by vladcom (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=39650
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from nightride_core import NightRideCore  # noqa: E402


SCREEN = 240
LANE_X = [76, 120, 164]


class NightRide:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Night Ride", fps=30)
        self.core = NightRideCore()
        self.screen = "title"
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3", "n", "6", "f", 5)
        pyxel.sound(1).set("c4g3", "t", "5", "n", 7)
        pyxel.sound(2).set("c2", "s", "7", "f", 12)
        pyxel.sound(3).set("c3d#3g3c4", "p", "4", "n", 14)

    def update(self) -> None:
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if self.core.game_over or self.core.victory:
            if ih.btnp_a() or ih.btnp_start():
                self.core.restart()
            elif ih.btnp_select():
                self.screen = "title"
            return
        if ih.btnp_select():
            self.core.restart()
        turn = 0
        if ih.btnp_left(hold=8, repeat=8):
            turn = -1
        elif ih.btnp_right(hold=8, repeat=8):
            turn = 1
        if ih.btnp_a() or ih.btnp_b():
            if self.core.shoot():
                pyxel.play(3, 1)
        self.core.tick(turn=turn)

    def draw(self) -> None:
        pyxel.cls(0)
        if self.screen == "title":
            self._draw_title()
            return
        self._draw_road()
        self._draw_actors()
        self._draw_hud()
        if self.core.game_over:
            self._panel("wrecked", "A retry   Select title")
        elif self.core.victory:
            self._panel("sunrise", "A ride again")

    def _draw_title(self) -> None:
        self._draw_road()
        self._draw_player(120, 170)
        self._center("NIGHT RIDE", 58, 7)
        self._center("vladcom", 80, 6)
        self._center("D-pad dodge   A shoot", 204, 7)
        self._center("A start", 220, 10 if pyxel.frame_count % 40 < 28 else 5)

    def _draw_road(self) -> None:
        pyxel.rect(48, 0, 144, SCREEN, 1)
        for y in range(-20, SCREEN, 24):
            yy = (y + pyxel.frame_count * 3) % (SCREEN + 24) - 24
            pyxel.rect(118, yy, 4, 12, 7)
            pyxel.rect(74, yy + 12, 3, 10, 5)
            pyxel.rect(163, yy + 12, 3, 10, 5)
        pyxel.rect(0, 0, 48, SCREEN, 0)
        pyxel.rect(192, 0, 48, SCREEN, 0)
        for i in range(20):
            x = (i * 47 + pyxel.frame_count) % SCREEN
            y = (i * 31 + pyxel.frame_count * 2) % SCREEN
            pyxel.pset(x, y, 6)

    def _draw_actors(self) -> None:
        for car in self.core.traffic:
            x = LANE_X[int(car["lane"])]
            y = int(float(car["y"]) * SCREEN)
            color = 8 if car["kind"] == "bike" else 12
            self._draw_enemy_car(x, y, color)
        for bullet in self.core.bullets:
            x = LANE_X[int(bullet["lane"])]
            y = int(float(bullet["y"]) * SCREEN)
            pyxel.rect(x - 2, y - 5, 4, 10, 10)
        if self.core.boss_hp > 0:
            pyxel.rect(72, 24, 96, 24, 2)
            pyxel.rectb(72, 24, 96, 24, 7)
            pyxel.text(91, 33, "NIGHT BOSS", 7)
        self._draw_player(LANE_X[self.core.lane], 206)

    def _draw_player(self, x: int, y: int) -> None:
        pyxel.tri(x, y - 16, x - 12, y + 12, x + 12, y + 12, 10)
        pyxel.rect(x - 7, y - 2, 14, 10, 7)
        pyxel.pset(x, y - 10, 0)

    def _draw_enemy_car(self, x: int, y: int, color: int) -> None:
        pyxel.rect(x - 10, y - 12, 20, 24, color)
        pyxel.rect(x - 6, y - 8, 12, 8, 5)
        pyxel.rect(x - 8, y + 8, 16, 4, 0)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 24, 0)
        pyxel.text(5, 5, f"level {self.core.level} hp {self.core.hp} score {self.core.score}", 7)
        weapon = "gun" if self.core.weapon_unlocked else "drive"
        pyxel.text(5, 15, f"{weapon}  {self.core.message[:26]}", 10)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 94, 192, 52, 0)
        pyxel.rectb(24, 94, 192, 52, 7)
        self._center(title, 112, 10)
        self._center(subtitle, 130, 7)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    NightRide()

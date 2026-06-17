"""Whiplash Taxi Co - PyxelPico port.

Adapted from the PICO-8 cart by Mot (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=53583
"""

from __future__ import annotations

import math
import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from whiplashtaxi_core import WhiplashTaxiCore  # noqa: E402


SCREEN = 240


class WhiplashTaxi:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Whiplash Taxi Co", fps=30)
        self.core = WhiplashTaxiCore()
        self.screen = "title"
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3e3", "n", "5", "f", 6)
        pyxel.sound(1).set("g3c4", "t", "6", "n", 8)
        pyxel.sound(2).set("c2", "s", "7", "f", 12)
        pyxel.sound(3).set("c4e4g4", "p", "5", "n", 10)

    def update(self) -> None:
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if self.core.shift_over:
            if ih.btnp_a() or ih.btnp_start():
                self.core.restart()
            elif ih.btnp_select():
                self.screen = "title"
            return
        if ih.btnp_select():
            self.core.restart()
        turn = int(ih.btn_right()) - int(ih.btn_left())
        before_money = self.core.money
        self.core.tick(accel=ih.btn_a() or ih.btn_up(), reverse=ih.btn_b() or ih.btn_down(), turn=turn)
        if self.core.money > before_money:
            pyxel.play(3, 1)

    def draw(self) -> None:
        pyxel.cls(3)
        if self.screen == "title":
            self._draw_title()
            return
        self._draw_city()
        self._draw_target()
        self._draw_taxi()
        self._draw_hud()
        if self.core.shift_over:
            self._panel("shift over", f"${self.core.money}  A retry")

    def _draw_title(self) -> None:
        self._draw_city()
        self._draw_taxi_at(122, 132, -0.5)
        self._center("WHIPLASH", 54, 10)
        self._center("TAXI CO", 70, 7)
        self._center("Mot", 92, 6)
        self._center("A gas  B brake/reverse", 202, 7)
        self._center("A start", 218, 10 if pyxel.frame_count % 40 < 28 else 5)

    def _draw_city(self) -> None:
        pyxel.cls(5)
        for x in range(24, SCREEN, 48):
            pyxel.rect(x - 8, 0, 16, SCREEN, 1)
        for y in range(24, SCREEN, 48):
            pyxel.rect(0, y - 8, SCREEN, 16, 1)
        for bx in range(8, SCREEN, 48):
            for by in range(8, SCREEN, 48):
                pyxel.rect(bx, by, 24, 24, 13 if (bx + by) % 96 else 6)
                pyxel.rectb(bx, by, 24, 24, 0)
        for passenger in self.core.passengers:
            if not passenger.delivered and not passenger.aboard:
                x, y = int(passenger.pickup[0]), int(passenger.pickup[1])
                pyxel.circ(x, y, 5, 8)
                pyxel.tri(x, y - 17, x - 6, y - 7, x + 6, y - 7, 8)
            if not passenger.delivered:
                x, y = int(passenger.destination[0]), int(passenger.destination[1])
                pyxel.rect(x - 6, y - 6, 12, 12, 10)
                pyxel.rectb(x - 6, y - 6, 12, 12, 0)

    def _draw_target(self) -> None:
        tx, ty = self.core.target()
        dx, dy = tx - self.core.x, ty - self.core.y
        angle = math.atan2(dy, dx)
        x = 120 + int(math.cos(angle) * 104)
        y = 120 + int(math.sin(angle) * 104)
        pyxel.tri(x, y, x - int(math.cos(angle + 0.6) * 12), y - int(math.sin(angle + 0.6) * 12), x - int(math.cos(angle - 0.6) * 12), y - int(math.sin(angle - 0.6) * 12), 8)

    def _draw_taxi(self) -> None:
        self._draw_taxi_at(int(self.core.x), int(self.core.y), self.core.heading)

    def _draw_taxi_at(self, x: int, y: int, heading: float) -> None:
        nose = (x + int(math.cos(heading) * 13), y + int(math.sin(heading) * 13))
        left = (x + int(math.cos(heading + 2.45) * 10), y + int(math.sin(heading + 2.45) * 10))
        right = (x + int(math.cos(heading - 2.45) * 10), y + int(math.sin(heading - 2.45) * 10))
        pyxel.tri(nose[0], nose[1], left[0], left[1], right[0], right[1], 10)
        pyxel.line(left[0], left[1], right[0], right[1], 0)
        pyxel.pset(x, y, 7)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 26, 0)
        pyxel.text(5, 5, f"${self.core.money} fares {self.core.deliveries} time {int(self.core.time_left):03d}", 7)
        pyxel.text(5, 17, self.core.message[:42], 10)
        pyxel.text(6, 224, "A/Up gas  B/Down brake  Left/Right steer  Select restart", 7)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 94, 192, 52, 0)
        pyxel.rectb(24, 94, 192, 52, 7)
        self._center(title, 112, 10)
        self._center(subtitle, 130, 7)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    WhiplashTaxi()

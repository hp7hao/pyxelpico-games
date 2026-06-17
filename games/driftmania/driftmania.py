"""Driftmania - PyxelPico port.

Adapted from the PICO-8 cart by Max Bize (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=140202
"""

from __future__ import annotations

import math
import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from driftmania_core import DriftmaniaCore  # noqa: E402


SCREEN = 240


class Driftmania:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Driftmania", fps=30)
        self.core = DriftmaniaCore()
        self.screen = "title"
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c2c2g2", "n", "5", "f", 6)
        pyxel.sound(1).set("c3g3c4", "t", "6", "n", 8)
        pyxel.sound(2).set("g1", "s", "7", "f", 12)
        pyxel.sound(3).set("c4e4g4c5", "p", "5", "n", 14)

    def update(self) -> None:
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if self.core.finished:
            if ih.btnp_a() or ih.btnp_start():
                self.core.restart()
            elif ih.btnp_select():
                self.screen = "title"
            return
        if ih.btnp_select():
            self.core.restart()
        turn = int(ih.btn_right()) - int(ih.btn_left())
        self.core.tick(accel=ih.btn_a() or ih.btn_up(), brake=ih.btn_down(), turn=turn, drift=ih.btn_b())
        if self.core.boost_timer == 20:
            pyxel.play(3, 1)

    def draw(self) -> None:
        pyxel.cls(5)
        if self.screen == "title":
            self._draw_title()
            return
        self._draw_track()
        self._draw_car()
        self._draw_hud()
        if self.core.finished:
            self._panel(f"{self.core.medal} medal", "A retry   Select title")

    def _draw_title(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 3)
        self._draw_track()
        for i in range(9):
            pyxel.line(20 + i * 22, 210, 80 + i * 22, 160, 11)
        self._draw_car_at(120, 128, -0.8, 8)
        self._center("DRIFTMANIA", 52, 7)
        self._center("tiny tracks. fast laps.", 72, 10)
        self._center("Max Bize", 92, 6)
        self._center("A accelerate  B drift", 206, 7)
        self._center("A start", 220, 10 if pyxel.frame_count % 40 < 28 else 5)

    def _draw_track(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 3)
        pyxel.circ(120, 120, 91, 11)
        pyxel.circ(120, 120, 54, 3)
        pyxel.rect(72, 82, 96, 76, 11)
        pyxel.rect(95, 101, 50, 38, 3)
        for x, y in self.core.grass_tiles:
            pyxel.circ(int(x), int(y), 22, 3)
        for x, y in self.core.boost_tiles:
            pyxel.rect(int(x) - 10, int(y) - 6, 20, 12, 10)
            pyxel.text(int(x) - 5, int(y) - 2, ">>", 0)
        for i, gate in enumerate(self.core.checkpoints):
            x, y = int(gate[0]), int(gate[1])
            color = 10 if i == self.core.next_checkpoint else 6
            pyxel.circb(x, y, 10, color)
        pyxel.line(99, 198, 141, 198, 7)
        for i in range(6):
            color = 0 if i % 2 else 7
            pyxel.rect(100 + i * 7, 194, 7, 8, color)

    def _draw_car(self) -> None:
        self._draw_car_at(int(self.core.x), int(self.core.y), self.core.heading, 8)
        if self.core.traction < 0.8:
            tx = int(self.core.x - math.cos(self.core.heading) * 12)
            ty = int(self.core.y - math.sin(self.core.heading) * 12)
            pyxel.line(tx - 8, ty, tx + 8, ty + 4, 6)

    def _draw_car_at(self, x: int, y: int, heading: float, color: int) -> None:
        nose = (x + int(math.cos(heading) * 12), y + int(math.sin(heading) * 12))
        left = (x + int(math.cos(heading + 2.35) * 9), y + int(math.sin(heading + 2.35) * 9))
        right = (x + int(math.cos(heading - 2.35) * 9), y + int(math.sin(heading - 2.35) * 9))
        pyxel.tri(nose[0], nose[1], left[0], left[1], right[0], right[1], color)
        pyxel.line(left[0], left[1], right[0], right[1], 0)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 24, 0)
        pyxel.text(5, 5, f"time {self.core.elapsed:05.2f}  speed {abs(self.core.speed):03.1f}", 7)
        pyxel.text(5, 15, self.core.message[:34], 10)
        pyxel.text(170, 5, f"gate {self.core.next_checkpoint + 1}/{len(self.core.checkpoints)}", 7)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 94, 192, 52, 0)
        pyxel.rectb(24, 94, 192, 52, 7)
        self._center(title, 112, 10)
        self._center(subtitle, 130, 7)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    Driftmania()

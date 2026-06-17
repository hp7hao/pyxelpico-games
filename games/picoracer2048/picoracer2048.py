"""PICORACER-2048 — PyxelPico port.

Adapted from the PICO-8 cart by impbox (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=2243
"""

from __future__ import annotations

import math
import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from picoracer2048_core import Picoracer2048Core  # noqa: E402


SCREEN = 240


class Picoracer2048:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="PICORACER-2048", fps=30)
        self.core = Picoracer2048Core()
        self.mode = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3g3c4", "t", "6", "n", 8)
        pyxel.sound(1).set("c4e4g4c5", "p", "5", "f", 6)
        pyxel.sound(2).set("c2", "n", "7", "f", 12)
        pyxel.sound(3).set("g4c5", "s", "6", "n", 6)

    def reset(self) -> None:
        self.core.restart()
        self.mode = "play"
        self.flash = 0

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.mode == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.mode = "play"
                pyxel.play(3, 0)
            return
        if self.core.finished:
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            elif ih.btnp_select():
                self.mode = "title"
            return

        old_message = self.core.message
        self.core.tick(
            accelerate=ih.btn_a() or ih.btn_up(),
            brake=ih.btn_b() or ih.btn_down(),
            left=ih.btn_left(),
            right=ih.btn_right(),
            class_up=ih.btnp_start(),
            class_down=ih.btnp_select(),
        )
        if self.core.message != old_message:
            if self.core.message == "boost":
                pyxel.play(3, 1)
            elif self.core.message == "wall hit":
                pyxel.play(3, 2)
                self.flash = 4
            elif self.core.message == "finished":
                pyxel.play(3, 3)

    def draw(self) -> None:
        pyxel.cls(0 if self.flash == 0 else 8)
        if self.mode == "title":
            self._draw_title()
            return
        self._draw_track()
        self._draw_racers()
        self._draw_hud()
        if self.core.finished:
            self._panel("finished", f"time {self.core.finish_time / 30:.1f}s  A retry")

    def _draw_title(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        for y in range(0, SCREEN, 18):
            pyxel.line(0, y, SCREEN, (y + pyxel.frame_count // 3) % SCREEN, 13)
        self._draw_track_preview(120, 120, 72)
        self._center("picoracer", 38, 11)
        self._center("2048", 54, 10)
        self._center("impbox", 72, 7)
        self._center("A accelerate  B brake", 196, 6)
        self._center("press A", 214, 10 if pyxel.frame_count % 30 < 22 else 6)

    def _draw_track(self) -> None:
        horizon = 38
        center = SCREEN // 2
        progress = self.core.progress_ratio()
        curve_bias = self.core.current_curve() * 38
        for i in range(36):
            depth = i / 35
            y = int(horizon + depth * depth * 190)
            width = int(18 + depth * 114 * self.core.current_width())
            wiggle = math.sin((progress * 20 + i) * 0.45) * 18 + curve_bias * depth
            cx = int(center + wiggle - self.core.player.lane * 44 * depth)
            color = 5 if i % 2 == 0 else 13
            pyxel.line(cx - width, y, cx + width, y, color)
            if i % 5 == 0:
                pyxel.line(cx - width, y, cx - width - 20, y + 8, 7)
                pyxel.line(cx + width, y, cx + width + 20, y + 8, 7)
        for offset, color in ((-55, 3), (55, 11)):
            x = int(center + offset - self.core.player.lane * 30)
            pyxel.rect(x, 150, 12, 58, color)

    def _draw_racers(self) -> None:
        self._draw_ship(120, 184, 10, 7)
        gap = (self.core.ai.segment - self.core.player.segment) % self.core.track_length
        if gap < 45 or gap > self.core.track_length - 20:
            y = 112 if gap < 45 else 204
            x = int(120 + self.core.ai.lane * 42)
            self._draw_ship(x, y, 8, 9)

    def _draw_ship(self, x: int, y: int, body: int, glow: int) -> None:
        pyxel.tri(x, y - 12, x - 10, y + 10, x + 10, y + 10, body)
        pyxel.tri(x - 8, y + 4, x - 18, y + 14, x - 2, y + 12, glow)
        pyxel.tri(x + 8, y + 4, x + 18, y + 14, x + 2, y + 12, glow)
        pyxel.rect(x - 3, y - 4, 6, 6, 12)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 28, 0)
        pyxel.text(8, 6, f"lap {self.core.lap + 1}/{self.core.laps_to_win}", 7)
        pyxel.text(70, 6, f"spd {self.core.player.speed:.1f}", 10)
        pyxel.text(126, 6, f"class {self.core.player.class_index + 1}", 6)
        pyxel.text(184, 6, f"p{self.core.position}", 11)
        pyxel.text(8, 18, self.core.message[:28], 13)

    def _draw_track_preview(self, cx: int, cy: int, radius: int) -> None:
        prev = None
        for i in range(72):
            angle = i / 72 * math.tau
            r = radius + math.sin(angle * 3) * 11 + math.cos(angle * 5) * 5
            point = (int(cx + math.cos(angle) * r), int(cy + math.sin(angle) * r))
            if prev:
                pyxel.line(prev[0], prev[1], point[0], point[1], 7)
            prev = point

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 92, 192, 56, 0)
        pyxel.rectb(24, 92, 192, 56, 7)
        self._center(title, 110, 11)
        self._center(subtitle, 130, 6)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    Picoracer2048()

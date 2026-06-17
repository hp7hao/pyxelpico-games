"""Brutal Pico Race - PyxelPico port.

Adapted from the PICO-8 cart by dhostin / Damien Hostin (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=31490
"""

from __future__ import annotations

import math
import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from brutalpicorace_core import BrutalPicoRaceCore  # noqa: E402


SCREEN = 240


class BrutalPicoRace:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Brutal Pico Race", fps=30)
        self.core = BrutalPicoRaceCore()
        self.screen = "title"
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c2c2", "n", "55", "f", 4)
        pyxel.sound(1).set("c3g3c4", "t", "567", "n", 8)
        pyxel.sound(2).set("c2", "s", "7", "f", 10)
        pyxel.sound(3).set("g3c4g4", "p", "567", "n", 14)

    def update(self) -> None:
        if self.screen == "title":
            if ih.btnp_left() or ih.btnp_right() or ih.btnp_select():
                self.core.cycle_ship()
                pyxel.play(3, 1)
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "race"
                pyxel.play(3, 3)
            return
        if self.core.finished or self.core.health <= 0:
            if ih.btnp_a() or ih.btnp_start():
                self.core.restart()
            elif ih.btnp_select():
                self.screen = "title"
            return
        steer = int(ih.btn_right()) - int(ih.btn_left())
        before = self.core.message
        self.core.tick(accel=ih.btn_a() or ih.btn_down(), brake=ih.btn_b() or ih.btn_up(), boost=ih.btnp_select(), steer=steer)
        if self.core.message == "boost":
            pyxel.play(3, 2)
        elif self.core.message != before and self.core.message.startswith("lap"):
            pyxel.play(3, 3)
        elif pyxel.frame_count % 12 == 0:
            pyxel.play(3, 0)

    def draw(self) -> None:
        pyxel.cls(1)
        if self.screen == "title":
            self._draw_track()
            self._draw_title()
            return
        self._draw_track()
        self._draw_ship()
        self._draw_hud()
        if self.core.finished:
            self._panel(f"finish rank {self.core.rank}", "A race again")
        elif self.core.health <= 0:
            self._panel("ship destroyed", "A rebuild")

    def _draw_track(self) -> None:
        pyxel.rect(0, 0, SCREEN, 86, 1)
        pyxel.rect(0, 86, SCREEN, 154, 0)
        curve = math.sin((self.core.progress / self.core.track_length) * math.tau * 2.0)
        for i in range(18):
            y = 88 + i * 9
            width = 18 + i * 7
            center = 120 + int(curve * i * 4)
            color = 5 if i % 2 else 13
            pyxel.tri(center - width, y, center + width, y, center + width + 10, y + 11, color)
            pyxel.tri(center - width, y, center - width - 10, y + 11, center + width + 10, y + 11, color)
            if i % 3 == 0:
                pyxel.line(center - width, y, center - width - 10, y + 11, 10)
                pyxel.line(center + width, y, center + width + 10, y + 11, 8)
        for idx, ai in enumerate(self.core.ai_progress):
            gap = (ai - (self.core.lap * self.core.track_length + self.core.progress)) % self.core.track_length
            if gap < 50:
                y = 90 + int(gap * 2.0)
                x = 120 + int(math.sin(ai * 0.08 + idx) * 36)
                self._draw_enemy_ship(x, y, [8, 10, 12][idx])

    def _draw_ship(self) -> None:
        x = int(120 + self.core.position_x * 70)
        y = 196
        color = {"heavy": 8, "normal": 10, "light": 12}[self.core.ship_class]
        pyxel.tri(x, y - 24, x - 14, y + 16, x + 14, y + 16, color)
        pyxel.rect(x - 8, y, 16, 8, 7)
        if self.core.message == "boost":
            pyxel.tri(x - 7, y + 18, x, y + 36, x + 7, y + 18, 9)

    def _draw_enemy_ship(self, x: int, y: int, color: int) -> None:
        pyxel.tri(x, y - 8, x - 6, y + 8, x + 6, y + 8, color)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 30, 0)
        pyxel.text(5, 5, f"lap {self.core.lap + 1}/{self.core.laps_required} rank {self.core.rank} {self.core.ship_class}", 7)
        pyxel.text(5, 16, f"spd {self.core.speed:.1f} {self.core.message[:16]}", 10)
        self._bar(138, 6, 90, 5, self.core.health / self.core.stats["health"], 8)
        self._bar(138, 17, 90, 5, self.core.boost_meter / 100, 12)
        pyxel.text(5, 228, "A/Down gas  B/Up brake  Left/Right steer  Select boost", 6)

    def _bar(self, x: int, y: int, w: int, h: int, value: float, color: int) -> None:
        pyxel.rect(x, y, w, h, 5)
        pyxel.rect(x, y, int(w * max(0, min(1, value))), h, color)

    def _draw_title(self) -> None:
        pyxel.rect(18, 44, 204, 82, 0)
        pyxel.rectb(18, 44, 204, 82, 7)
        self._center("BRUTAL PICO RACE", 58, 7)
        self._center("dhostin", 76, 6)
        self._center(f"ship: {self.core.ship_class}", 96, 10)
        self._center("Left/Right class   A start", 110, 7)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 88, 192, 58, 0)
        pyxel.rectb(24, 88, 192, 58, 7)
        self._center(title, 106, 10)
        self._center(subtitle, 126, 7)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    BrutalPicoRace()

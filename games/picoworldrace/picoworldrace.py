"""Pico World Race — PyxelPico port.

Adapted from the PICO-8 cart by PAK9 (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=46495
"""

from __future__ import annotations

import math
import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from picoworldrace_core import PicoWorldRaceCore  # noqa: E402


SCREEN = 240


class PicoWorldRace:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Pico World Race", fps=30)
        self.core = PicoWorldRaceCore()
        self.mode = "title"
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3e3g3", "t", "4", "n", 6)
        pyxel.sound(1).set("g4", "p", "7", "n", 5)
        pyxel.sound(2).set("c2", "n", "7", "f", 12)

    def reset(self) -> None:
        self.core.reset()
        self.mode = "race"

    def update(self) -> None:
        if self.mode == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            return
        if self.mode == "finish":
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            elif ih.btnp_b() or ih.btnp_select():
                self.mode = "title"
            return
        steer = int(ih.btn_right()) - int(ih.btn_left())
        accel = ih.btn_a() or ih.btn_up()
        drift = ih.btn_b() or ih.btn_down()
        self.core.input(accel=accel, steer=steer, drift=drift)
        old_tokens = self.core.tokens_collected
        self.core.tick()
        if self.core.tokens_collected > old_tokens:
            pyxel.play(3, 1)
        elif self.core.crashed and pyxel.frame_count % 8 == 0:
            pyxel.play(3, 2)
        if self.core.finished:
            self.mode = "finish"

    def draw(self) -> None:
        pyxel.cls(12)
        if self.mode == "title":
            self._draw_title()
            return
        self._draw_track()
        self._draw_tokens()
        self._draw_opponents()
        self._draw_car(120 + int(self.core.lane * 46), 180, 8)
        self._draw_hud()
        if self.mode == "finish":
            self._panel("finish", f"pos {self.core.standing()}  score {self.core.score}")

    def _draw_title(self) -> None:
        self._draw_track()
        self._draw_car(120, 172, 8)
        self._center("pico world race", 52, 10)
        self._center("pak9", 68, 6)
        self._center("A/up gas  B/down drift", 194, 7)
        self._center("press A", 216, 11)

    def _draw_track(self) -> None:
        pyxel.rect(0, 0, SCREEN, 104, 12)
        pyxel.rect(0, 104, SCREEN, 136, 3)
        curve = math.sin(self.core.progress / 28) * 18
        for i in range(14):
            y = 104 + i * 10
            half = 26 + i * 6
            cx = 120 + curve * (i / 14)
            color = 5 if i % 2 else 1
            pyxel.line(int(cx - half), y, int(cx - half - 6), y + 10, 7)
            pyxel.line(int(cx + half), y, int(cx + half + 6), y + 10, 7)
            pyxel.line(int(cx), y, int(cx), y + 5, color)
        pyxel.rect(0, 216, SCREEN, 24, 4)

    def _draw_tokens(self) -> None:
        for index, token in enumerate(self.core.tokens):
            if index in self.core.seen_tokens:
                continue
            ahead = (token - self.core.progress) % self.core.track_length
            if ahead < 80:
                y = 174 - int(ahead)
                x = 120 + int(math.sin(token / 12) * 34)
                pyxel.circ(x, y, 3, 10)

    def _draw_opponents(self) -> None:
        player_total = (self.core.lap - 1) * self.core.track_length + self.core.progress
        for index, pos in enumerate(self.core.opponents):
            rel = pos - player_total
            if -20 < rel < 110:
                y = 174 - int(rel)
                x = 92 + index * 24
                self._draw_car(x, y, 9 + index)

    def _draw_car(self, x: int, y: int, color: int) -> None:
        pyxel.rect(x - 8, y - 14, 16, 26, color)
        pyxel.rect(x - 5, y - 18, 10, 8, 6)
        pyxel.rect(x - 10, y - 8, 4, 10, 0)
        pyxel.rect(x + 6, y - 8, 4, 10, 0)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 28, 0)
        pyxel.text(8, 6, f"lap {self.core.lap}/{self.core.total_laps}", 7)
        pyxel.text(76, 6, f"tok {self.core.tokens_collected}/20", 7)
        pyxel.text(154, 6, f"pos {self.core.standing()}", 7)
        pyxel.text(8, 18, f"spd {self.core.speed:0.1f}", 6)
        pyxel.rect(64, 20, int(120 * self.core.progress / self.core.track_length), 4, 10)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(28, 92, 184, 54, 0)
        pyxel.rectb(28, 92, 184, 54, 7)
        self._center(title, 108, 11)
        self._center(subtitle, 128, 6)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    PicoWorldRace()

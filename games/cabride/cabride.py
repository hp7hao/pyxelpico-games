"""Cab Ride - PyxelPico port.

Adapted from the PICO-8 cart by Powersaurus (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=41332
"""

from __future__ import annotations

import math
import os
import random
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from cabride_core import CabRideCore  # noqa: E402


SCREEN = 240


class CabRide:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Cab Ride", fps=30)
        self.core = CabRideCore()
        self.screen = "title"
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3e3g3", "t", "543", "n", 12)
        pyxel.sound(1).set("c2", "s", "7", "f", 18)
        pyxel.sound(2).set("g3c4", "p", "66", "n", 10)
        pyxel.sound(3).set("c4e4g4c5", "t", "4567", "n", 16)

    def update(self) -> None:
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if self.core.journey_over:
            if ih.btnp_a() or ih.btnp_start():
                self.core.restart()
            return
        if ih.btnp_start():
            self.screen = "title"
            return
        throttle = 0
        if ih.btn_up():
            throttle -= 1
        if ih.btn_down():
            throttle += 1
        if ih.btnp_a():
            self.core.horn()
            pyxel.play(3, 1)
        if ih.btnp_b():
            result = self.core.toggle_doors()
            pyxel.play(3, 2 if result in ("stop first", "not at signal") else 3)
        if ih.btnp_right(hold=60, repeat=0) or ih.btnp_select():
            self.core.toggle_express()
            pyxel.play(3, 0)
        if ih.btnp_left(hold=60, repeat=0):
            self.core.announce_last_station()
            pyxel.play(3, 0)
        self.core.tick(throttle=throttle)

    def draw(self) -> None:
        pyxel.cls(1)
        if self.screen == "title":
            self._draw_world()
            self._draw_title()
            return
        self._draw_world()
        self._draw_cab()
        self._draw_hud()
        if self.core.journey_over:
            self._panel("journey complete", "A start another ride")

    def _draw_world(self) -> None:
        weather_color = {"clear": 12, "clouds": 6, "rain": 5}[self.core.weather]
        pyxel.rect(0, 0, SCREEN, 96, weather_color)
        pyxel.rect(0, 96, SCREEN, 144, 3)
        rng = random.Random(self.core.scenery_seed)
        scroll = int(self.core.distance * 130) % 240
        for i in range(12):
            x = (i * 43 - scroll) % 280 - 20
            h = 26 + rng.randrange(72)
            color = [5, 6, 13, 2][i % 4]
            if i % 3 == 0:
                pyxel.tri(x - 18, 98, x + 18, 98, x, 50 - h // 5, color)
            else:
                pyxel.rect(x - 8, 98 - h, 18, h, color)
                for wy in range(100 - h, 92, 14):
                    pyxel.rect(x - 4, wy, 4, 5, 10)
        for i in range(30):
            x = (i * 17 - scroll * 2) % 260 - 10
            y = 143 + int(math.sin(i + pyxel.frame_count * 0.05) * 3)
            pyxel.line(x, y, x + 18, y + 5, 5)
        if self.core.weather == "rain":
            for i in range(36):
                x = (i * 29 + pyxel.frame_count * 3) % SCREEN
                y = (i * 17 + pyxel.frame_count * 5) % 100
                pyxel.line(x, y, x - 3, y + 7, 12)
        self._draw_tracks(scroll)

    def _draw_tracks(self, scroll: int) -> None:
        pyxel.tri(84, 240, 114, 102, 126, 102, 5)
        pyxel.tri(156, 240, 126, 102, 114, 102, 5)
        for y in range(108, 240, 18):
            yy = (y + scroll // 5) % 132 + 108
            width = int((yy - 100) * 0.55)
            pyxel.line(120 - width, yy, 120 + width, yy, 4)

    def _draw_cab(self) -> None:
        pyxel.rect(0, 170, SCREEN, 70, 0)
        pyxel.rectb(12, 160, 216, 48, 7)
        pyxel.rect(16, 164, 208, 40, 1)
        pyxel.rect(32, 212, 176, 18, 5)
        needle = int(92 + self.core.speed * 74)
        pyxel.rect(90, 216, 80, 5, 0)
        pyxel.rect(90, 216, needle - 90, 5, 10)
        pyxel.text(37, 218, "speed", 7)
        pyxel.text(174, 218, f"thr {self.core.throttle_level:+d}", 7)
        if self.core.horn_timer > 0:
            self._center("TOOT", 150, 10)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 26, 0)
        pyxel.text(5, 5, f"st {self.core.station_index}  pax {self.core.passengers}  score {self.core.total_score}", 7)
        dist = max(-0.99, self.core.distance_to_station)
        mode = "express" if self.core.express_mode else "local"
        pyxel.text(5, 16, f"{mode}  next {dist:.2f}  {self.core.status[:18]}", 10)
        if self.core.last_station_announced:
            pyxel.text(148, 16, "last station", 8)

    def _draw_title(self) -> None:
        pyxel.rect(22, 44, 196, 78, 0)
        pyxel.rectb(22, 44, 196, 78, 7)
        self._center("CAB RIDE", 58, 7)
        self._center("Powersaurus", 76, 6)
        self._center("Down throttle   Up brake", 94, 10)
        self._center("B doors   A horn/start", 106, 7)
        self._center("A start", 220, 10 if pyxel.frame_count % 40 < 28 else 5)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 86, 192, 60, 0)
        pyxel.rectb(24, 86, 192, 60, 7)
        self._center(title, 105, 10)
        self._center(subtitle, 124, 7)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    CabRide()

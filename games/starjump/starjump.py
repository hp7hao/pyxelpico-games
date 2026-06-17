"""Starjump - PyxelPico port.

Adapted from the PICO-8 cart by lucatron / Luca Harris (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=41874
"""

from __future__ import annotations

import math
import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from starjump_core import Platform, StarjumpCore  # noqa: E402


SCREEN = 240


class Starjump:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Starjump", fps=30)
        self.core = StarjumpCore()
        self.screen = "title"
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c4g4c5", "t", "456", "n", 10)
        pyxel.sound(1).set("f4a4", "p", "65", "n", 8)
        pyxel.sound(2).set("c3", "n", "7", "f", 8)
        pyxel.sound(3).set("c4e4g4c5", "s", "5678", "n", 18)

    def update(self) -> None:
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if ih.btnp_select():
            self.core.restart()
            return
        if self.core.finished:
            if ih.btnp_a() or ih.btnp_start():
                self.core.restart()
            return
        move = int(ih.btn_right()) - int(ih.btn_left())
        if ih.btnp_a():
            if self.core.jump():
                pyxel.play(3, 0)
        if ih.btnp_b():
            self.core.toggle_color()
            pyxel.play(3, 1)
        if ih.btnp_up():
            self.core.grant_jump_charge()
            pyxel.play(3, 0)
        if ih.btnp_start():
            if self.core.use_cannon():
                pyxel.play(3, 3)
        self.core.tick(move=move)

    def draw(self) -> None:
        pyxel.cls(0)
        self._draw_grid()
        if self.screen == "title":
            self._draw_course()
            self._draw_star()
            self._draw_title()
            return
        self._draw_course()
        self._draw_star()
        self._draw_hud()
        if self.core.finished:
            self._panel("STARJUMP", "back to the beginning")

    def _draw_grid(self) -> None:
        for i in range(0, SCREEN, 16):
            wob = int(math.sin((pyxel.frame_count + i) * 0.07) * self.core.wobble * 2)
            pyxel.line(i + wob, 0, i - wob, SCREEN, 1)
            pyxel.line(0, i - wob, SCREEN, i + wob, 1)

    def _draw_course(self) -> None:
        pyxel.line(0, self.core.ground_y + 5, SCREEN, self.core.ground_y + 5, 7)
        for platform in self.core.platforms:
            self._draw_platform(platform)
        pyxel.circ(int(self.core.cannon_x), int(self.core.cannon_y), 12, 8)
        pyxel.tri(int(self.core.cannon_x) + 8, int(self.core.cannon_y) - 6, int(self.core.cannon_x) + 26, int(self.core.cannon_y) - 18, int(self.core.cannon_x) + 14, int(self.core.cannon_y) + 4, 8)
        pyxel.circ(int(self.core.goal_x), int(self.core.goal_y), 10, 10 if self.core.stage >= self.core.final_stage else 5)

    def _draw_platform(self, platform: Platform) -> None:
        if not platform.active:
            return
        color = 7 if platform.color == "white" else 14
        if platform.color != self.core.solid_color:
            color = 5
        x = int(platform.x - platform.w / 2)
        y = int(platform.y)
        pyxel.line(x, y, x + int(platform.w), y, color)
        pyxel.line(x, y + 1, x + int(platform.w), y + 1, color)
        if platform.breakable:
            for i in range(x, x + int(platform.w), 8):
                pyxel.line(i, y - 4, i + 4, y + 4, 8)

    def _draw_star(self) -> None:
        p = self.core.player
        points = []
        wob = math.sin(pyxel.frame_count * 0.2) * self.core.wobble
        for i in range(10):
            r = 12 if i % 2 == 0 else 5
            a = -math.pi / 2 + i * math.pi / 5 + wob * 0.04
            points.append((int(p.x + math.cos(a) * r), int(p.y + math.sin(a) * r)))
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]
            pyxel.line(x1, y1, x2, y2, 10)
        pyxel.pset(int(p.x - 3), int(p.y - 1), 7)
        pyxel.pset(int(p.x + 3), int(p.y - 1), 7)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 32, 0)
        timer = f" {self.core.timer // 30:02d}s" if self.core.show_timer else ""
        pyxel.text(5, 5, f"stage {self.core.stage}/{self.core.final_stage}{timer}  jumps {self.core.air_jumps}", 7)
        pyxel.text(5, 16, f"solid {self.core.solid_color}  {self.core.message[:24]}", 10)
        pyxel.text(5, 228, "D-pad move  A jump  B toggle  Up jump+  Start cannon  Select reset", 6)

    def _draw_title(self) -> None:
        self._panel("STARJUMP", "lucatron")
        self._center("vector platformer", 122, 10)
        self._center("A start", 220, 10 if pyxel.frame_count % 40 < 28 else 5)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(26, 72, 188, 76, 0)
        pyxel.rectb(26, 72, 188, 76, 7)
        self._center(title, 94, 7)
        self._center(subtitle, 110, 6)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    Starjump()

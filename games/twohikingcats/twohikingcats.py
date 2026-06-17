"""Two Hiking Cats - PyxelPico port.

Adapted from the PICO-8 art cart by solar (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=2719
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from twohikingcats_core import TwoHikingCatsCore  # noqa: E402


SCREEN = 240


class TwoHikingCats:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Two Hiking Cats", fps=30)
        self.core = TwoHikingCatsCore()
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c4g4", "t", "76", "n", 8)
        pyxel.sound(1).set("g3d4", "t", "67", "n", 10)
        pyxel.sound(2).set("c3", "p", "4", "n", 6)

    def update(self) -> None:
        if ih.btnp_left(hold=8, repeat=8):
            self.core.adjust_speed(-1)
        if ih.btnp_right(hold=8, repeat=8):
            self.core.adjust_speed(1)
        if ih.btnp_up():
            self.core.randomize_palette()
            pyxel.play(3, 2)
        if ih.btnp_down() or ih.btnp_start():
            self.core.reset_view()
        if ih.btnp_a():
            self.core.meow(0)
            pyxel.play(3, 0)
        if ih.btnp_b():
            self.core.meow(1)
            pyxel.play(3, 1)
        before = self.core.current_meow
        self.core.tick()
        if before != self.core.current_meow and self.core.manual_meow_timer == 0:
            pyxel.play(3, self.core.active_cat)

    def draw(self) -> None:
        sky, far, near, cat_color = self.core.palette
        pyxel.cls(sky)
        self._draw_sun(far)
        self._draw_hills(0, far)
        self._draw_hills(1, near)
        self._draw_path()
        positions = self.core.cat_positions()
        self._draw_cat(*positions[0], color=cat_color, facing=1, speaking=self.core.active_cat == 0)
        self._draw_cat(*positions[1], color=7, facing=-1, speaking=self.core.active_cat == 1)
        self._draw_dialog(positions)
        self._draw_hud()

    def _draw_sun(self, color: int) -> None:
        x = 190 - int(self.core.scroll * 0.03) % 260
        pyxel.circ(x, 42, 18, color)
        pyxel.circb(x, 42, 24, 7)

    def _draw_hills(self, layer: int, color: int) -> None:
        points = self.core.hill_points(layer)
        bottom = 240
        for left, right in zip(points, points[1:]):
            pyxel.tri(left[0], bottom, left[0], left[1], right[0], right[1], color)
            pyxel.tri(left[0], bottom, right[0], right[1], right[0], bottom, color)
        for x, y in points[::2]:
            pyxel.line(x, y, x + 9, y - 5, 7 if layer == 0 else 5)

    def _draw_path(self) -> None:
        pyxel.rect(0, 176, SCREEN, 64, 4)
        for i in range(16):
            x = (i * 23 - int(self.core.scroll * 2)) % 260 - 10
            pyxel.elli(x, 201 + (i % 3) * 8, 8, 3, 5)

    def _draw_cat(self, x: int, y: int, *, color: int, facing: int, speaking: bool) -> None:
        pyxel.circ(x, y - 19, 9, color)
        pyxel.tri(x - 6, y - 25, x - 2, y - 36, x + 1, y - 25, color)
        pyxel.tri(x + 2, y - 25, x + 7, y - 36, x + 8, y - 24, color)
        pyxel.rect(x - 10, y - 12, 22, 16, color)
        pyxel.line(x + 10 * facing, y - 5, x + 22 * facing, y - 15, color)
        pyxel.pset(x - 3, y - 21, 0)
        pyxel.pset(x + 4, y - 21, 0)
        mouth = 8 if speaking else 0
        pyxel.line(x - 1, y - 17, x + 3, y - 17, mouth)
        foot = 2 if self.core.frame % 12 < 6 else -2
        pyxel.line(x - 6, y + 4, x - 9, y + 12 + foot, color)
        pyxel.line(x + 7, y + 4, x + 10, y + 12 - foot, color)

    def _draw_dialog(self, positions: tuple[tuple[int, int], tuple[int, int]]) -> None:
        x, y = positions[self.core.active_cat]
        bubble_x = max(8, min(164, x - 20))
        pyxel.rect(bubble_x, y - 65, 68, 18, 7)
        pyxel.rectb(bubble_x, y - 65, 68, 18, 0)
        pyxel.text(bubble_x + 8, y - 59, self.core.current_meow[:13], 0)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 22, 0)
        pyxel.text(5, 5, f"speed {self.core.speed:.2f}  palette {self.core.palette_name}", 7)
        pyxel.text(5, 15, "Left/Right speed  Up palette  Down reset  A/B meow", 6)


if __name__ == "__main__":
    TwoHikingCats()

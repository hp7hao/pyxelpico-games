"""Wobblepaint - PyxelPico port.

Adapted from the PICO-8 cart by zep (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=40058
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from wobblepaint_core import WobblepaintCore  # noqa: E402


SCREEN = 240
SCALE = 1
OX = 56
OY = 36


class Wobblepaint:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Wobblepaint", fps=30)
        self.core = WobblepaintCore()
        self.screen = "title"
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c4", "p", "4", "n", 5)
        pyxel.sound(1).set("g3c4", "t", "5", "n", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 8)

    def update(self) -> None:
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "paint"
                pyxel.play(3, 1)
            return
        if ih.btnp_start():
            self.screen = "title"
            return
        if ih.btnp_select():
            self.core.clear()
            pyxel.play(3, 2)
        if ih.btn_b():
            if ih.btnp_left(hold=12, repeat=6):
                self.core.undo()
                pyxel.play(3, 2)
            elif ih.btnp_right(hold=12, repeat=6):
                self.core.cycle_color(1)
                pyxel.play(3, 1)
            elif ih.btnp_up(hold=12, repeat=6):
                self.core.adjust_brush(1)
                pyxel.play(3, 1)
            elif ih.btnp_down(hold=12, repeat=6):
                self.core.adjust_brush(-1)
                pyxel.play(3, 1)
            return
        dx = int(ih.btn_right()) - int(ih.btn_left())
        dy = int(ih.btn_down()) - int(ih.btn_up())
        if dx or dy:
            self.core.move_cursor(dx * 2, dy * 2)
        if ih.btn_a() or ih.btnp_a():
            self.core.paint()
            if pyxel.frame_count % 5 == 0:
                pyxel.play(3, 0)

    def draw(self) -> None:
        pyxel.cls(0)
        if self.screen == "title":
            self._draw_title()
            return
        self._draw_canvas()
        self._draw_hud()

    def _draw_title(self) -> None:
        pyxel.cls(1)
        for i in range(18):
            x = 28 + (i * 37) % 184
            y = 38 + (i * 23) % 132
            color = [10, 11, 12, 8, 9, 14][i % 6]
            pyxel.circ(x, y, 5 + i % 9, color)
        self._center("WOBBLEPAINT", 62, 7)
        self._center("zep", 84, 6)
        self._center("D-pad move   A paint", 180, 7)
        self._center("B+dir tools", 194, 10)
        self._center("A start", 216, 7 if pyxel.frame_count % 40 < 28 else 5)

    def _draw_canvas(self) -> None:
        pyxel.rect(OX - 2, OY - 2, 132, 132, 7)
        pyxel.rect(OX, OY, 128, 128, self.core.background)
        for x, y, color in self.core.animated_points(pyxel.frame_count):
            sx, sy = OX + x * SCALE, OY + y * SCALE
            if OX <= sx < OX + 128 and OY <= sy < OY + 128:
                pyxel.pset(sx, sy, color)
        cx, cy = self.core.cursor
        pyxel.circb(OX + cx, OY + cy, self.core.brush_size + 2, 7)
        pyxel.pset(OX + cx, OY + cy, self.core.color)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 28, 0)
        pyxel.text(5, 5, f"brush {self.core.brush_size} color {self.core.color} strokes {len(self.core.strokes)}", 7)
        pyxel.text(5, 17, self.core.message[:40], 10)
        pyxel.rect(198, 7, 14, 14, self.core.color)
        pyxel.rectb(198, 7, 14, 14, 7)
        pyxel.text(7, 222, "B+Left undo  B+Right color  B+Up/Down brush  Select clear", 7)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    Wobblepaint()

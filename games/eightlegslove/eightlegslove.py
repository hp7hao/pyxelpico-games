"""8 Legs to Love - PyxelPico port.

Adapted from the PICO-8 cart by bridgs (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=29451
"""

from __future__ import annotations

import math
import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from eightlegslove_core import EightLegsCore  # noqa: E402


SCREEN = 240


class EightLegsToLove:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="8 Legs to Love", fps=30)
        self.core = EightLegsCore()
        self.screen = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3g3c4", "t", "5", "n", 8)
        pyxel.sound(1).set("a3c4e4", "p", "6", "f", 10)
        pyxel.sound(2).set("f2", "n", "7", "f", 8)
        pyxel.sound(3).set("c4e4g4c5", "s", "5", "n", 12)

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if self.core.level_clear:
            if ih.btnp_a() or ih.btnp_start():
                self.core.advance_level()
                pyxel.play(3, 3)
            elif ih.btnp_select():
                self.screen = "title"
            return

        old_score = self.core.score
        old_strands = len(self.core.strands)
        spinning = ih.btn_a()
        place_web = self.core.preview_strand() is not None and not spinning
        self.core.tick(
            left=ih.btn_left(),
            right=ih.btn_right(),
            up=ih.btn_up(),
            down=ih.btn_down(),
            spin=spinning,
            place=place_web,
        )
        if ih.btnp_b():
            self._snap_web_to_anchor()
        if ih.btnp_start():
            self.core.restart()
        if self.core.score > old_score:
            pyxel.play(3, 1)
            self.flash = 4
        elif len(self.core.strands) > old_strands:
            pyxel.play(3, 0)

    def _snap_web_to_anchor(self) -> None:
        start = self.core.spider_pos()
        nearest = min(self.core.anchors, key=lambda anchor: math.dist(start, anchor))
        if math.dist(start, nearest) > 10:
            self.core.add_strand(start, nearest)
            self.core.message = "anchored web"
            pyxel.play(3, 0)

    def draw(self) -> None:
        pyxel.cls(7 if self.flash else 0)
        self._draw_background()
        if self.screen == "title":
            self._draw_title()
            return
        self._draw_web()
        self._draw_bugs()
        self._draw_spider()
        self._draw_hud()
        if self.core.level_clear:
            self._panel("web complete", "A next level   Select title")

    def _draw_background(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        pyxel.circb(120, 120, 98, 5)
        pyxel.circb(120, 120, 72, 13)
        pyxel.circb(120, 120, 42, 13)
        for x, y in self.core.anchors:
            pyxel.circ(int(x), int(y), 4, 4)
            pyxel.circb(int(x), int(y), 5, 10)

    def _draw_title(self) -> None:
        self._draw_sample_web()
        self._draw_spider_at(120, 126, 2)
        self._center("8 LEGS", 58, 7)
        self._center("TO LOVE", 72, 8)
        self._center("bridgs", 92, 13)
        self._center("A start", 210, 10 if pyxel.frame_count % 30 < 22 else 6)

    def _draw_sample_web(self) -> None:
        for angle in range(0, 360, 30):
            rad = math.radians(angle + pyxel.frame_count * 0.3)
            pyxel.line(120, 120, int(120 + math.cos(rad) * 86), int(120 + math.sin(rad) * 86), 6)
        for radius in (28, 52, 76):
            pyxel.circb(120, 120, radius, 13)

    def _draw_web(self) -> None:
        for strand in self.core.strands:
            color = 7 if strand.durability >= strand.max_durability else 6
            pyxel.line(int(strand.start[0]), int(strand.start[1]), int(strand.end[0]), int(strand.end[1]), color)
        preview = self.core.preview_strand()
        if preview:
            start, end = preview
            pyxel.line(int(start[0]), int(start[1]), int(end[0]), int(end[1]), 10)

    def _draw_bugs(self) -> None:
        for bug in self.core.bugs:
            x = int(bug.x)
            y = int(bug.y)
            if bug.kind == "beetle":
                pyxel.ellib(x - 5, y - 4, 10, 8, 8)
                pyxel.line(x - 5, y, x + 5, y, 2)
            elif bug.kind == "butterfly":
                pyxel.circ(x - 4, y, 4, 14)
                pyxel.circ(x + 4, y, 4, 12)
                pyxel.line(x, y - 3, x, y + 4, 0)
            else:
                pyxel.circ(x, y, 3, 6)
                pyxel.pset(x - 1, y - 1, 7)

    def _draw_spider(self) -> None:
        x, y = self.core.spider_pos()
        self._draw_spider_at(int(x), int(y), 8)

    def _draw_spider_at(self, x: int, y: int, color: int) -> None:
        phase = 1 if pyxel.frame_count % 20 < 10 else -1
        pyxel.circ(x, y, 6, color)
        pyxel.circ(x, y - 6, 4, color)
        for side in (-1, 1):
            for offset in (-6, -2, 2, 6):
                pyxel.line(x + side * 4, y + offset // 2, x + side * (12 + phase), y + offset, color)
        pyxel.pset(x - 2, y - 7, 7)
        pyxel.pset(x + 2, y - 7, 7)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 22, 0)
        pyxel.text(6, 5, f"lvl {self.core.level} score {self.core.score}/{self.core.goal_score}", 7)
        pyxel.text(158, 5, f"time {self.core.time_left // 30:02d}", 10)
        pyxel.text(6, 15, self.core.message[:42], 13)
        pyxel.rect(0, 222, SCREEN, 18, 0)
        pyxel.text(20, 228, "D-pad move  hold A spin  release place  B anchor", 7)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 92, 192, 56, 0)
        pyxel.rectb(24, 92, 192, 56, 7)
        self._center(title, 111, 10)
        self._center(subtitle, 130, 7)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    EightLegsToLove()

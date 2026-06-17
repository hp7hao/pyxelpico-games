"""Mot's 8-Ball Pool - PyxelPico port.

Adapted from the PICO-8 cart by Mot (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=39859
"""

from __future__ import annotations

import math
import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from mot8ballpool_core import Mot8BallPoolCore  # noqa: E402


SCREEN = 240


class Mot8BallPool:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Mot's 8-Ball Pool", fps=30)
        self.core = Mot8BallPoolCore()
        self.screen = "title"
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3", "n", "5", "f", 5)
        pyxel.sound(1).set("c4g3", "p", "64", "n", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 10)
        pyxel.sound(3).set("g3c4e4", "s", "567", "n", 14)

    def update(self) -> None:
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if ih.btnp_select():
            self.core.restart()
            return
        if self.core.game_over:
            if ih.btnp_a() or ih.btnp_start():
                self.core.restart()
            return
        if self.core.mode == "aim":
            if ih.btn_left():
                self.core.adjust_aim(-1)
            if ih.btn_right():
                self.core.adjust_aim(1)
            if ih.btn_up():
                self.core.adjust_power(1)
            if ih.btn_down():
                self.core.adjust_power(-1)
            if ih.btnp_a():
                self.core.shoot()
                pyxel.play(3, 0)
            if ih.btnp_b():
                self.core.resolve_pocket("solid")
        else:
            self.core.tick()

    def draw(self) -> None:
        pyxel.cls(1)
        if self.screen == "title":
            self._draw_table()
            self._draw_title()
            return
        self._draw_table()
        self._draw_balls()
        self._draw_cue()
        self._draw_hud()
        if self.core.game_over:
            self._panel(f"player {self.core.winner + 1} wins", "A rack again")

    def _draw_table(self) -> None:
        pyxel.rect(12, 54, 216, 132, 4)
        pyxel.rect(22, 64, 196, 112, 3)
        for x, y in [(22, 64), (120, 62), (218, 64), (22, 176), (120, 178), (218, 176)]:
            pyxel.circ(x, y, 7, 0)
        pyxel.rectb(22, 64, 196, 112, 7)

    def _draw_balls(self) -> None:
        for ball in self.core.balls:
            if ball["pocketed"]:
                continue
            color = {"solid": 10, "stripe": 12, "black": 0}[str(ball["color"])]
            pyxel.circ(int(ball["x"]), int(ball["y"]), 4, color)
            pyxel.circb(int(ball["x"]), int(ball["y"]), 4, 7)
        b = self.core.cue_ball
        pyxel.circ(int(b["x"]), int(b["y"]), 4, 7)
        pyxel.circb(int(b["x"]), int(b["y"]), 4, 0)

    def _draw_cue(self) -> None:
        if self.core.mode != "aim":
            return
        b = self.core.cue_ball
        dx = math.cos(self.core.aim)
        dy = math.sin(self.core.aim)
        pyxel.line(int(b["x"] - dx * 54), int(b["y"] - dy * 54), int(b["x"] - dx * 8), int(b["y"] - dy * 8), 6)
        pyxel.line(int(b["x"]), int(b["y"]), int(b["x"] + dx * 42), int(b["y"] + dy * 42), 10)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 42, 0)
        p1, p2 = self.core.players
        turn = self.core.current_player + 1
        pyxel.text(5, 5, f"turn p{turn}  power {int(self.core.power)}  {self.core.message[:24]}", 7)
        pyxel.text(5, 17, f"p1 {p1['color'] or '-'} sunk {p1['sunk']} free {int(bool(p1['free_ball']))}", 10)
        pyxel.text(126, 17, f"p2 {p2['color'] or '-'} sunk {p2['sunk']} free {int(bool(p2['free_ball']))}", 12)
        pyxel.text(5, 228, "Left/Right aim  Up/Down power  A shoot  Select reset", 6)

    def _draw_title(self) -> None:
        pyxel.rect(22, 48, 196, 70, 0)
        pyxel.rectb(22, 48, 196, 70, 7)
        self._center("MOT'S 8-BALL POOL", 64, 7)
        self._center("Mot", 82, 6)
        self._center("simplified rules / free ball", 100, 10)
        self._center("A start", 220, 10 if pyxel.frame_count % 40 < 28 else 5)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 88, 192, 58, 0)
        pyxel.rectb(24, 88, 192, 58, 7)
        self._center(title, 106, 10)
        self._center(subtitle, 126, 7)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    Mot8BallPool()

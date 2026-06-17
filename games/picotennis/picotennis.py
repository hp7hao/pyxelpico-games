"""Pico Tennis - PyxelPico port.

Adapted from the PICO-8 cart by paranoidcactus (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=31450
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from picotennis_core import PicoTennisCore  # noqa: E402


SCREEN = 240
SCALE = 1.25
OX = 45
OY = 8


class PicoTennis:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Pico Tennis", fps=30)
        self.core = PicoTennisCore()
        self.screen = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3", "n", "7", "f", 6)
        pyxel.sound(1).set("c3g3", "t", "6", "n", 8)
        pyxel.sound(2).set("c2", "s", "7", "f", 12)
        pyxel.sound(3).set("c4e4g4", "p", "5", "n", 12)

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if self.core.match_over:
            if ih.btnp_a() or ih.btnp_start():
                self.core.restart()
                self.screen = "play"
            elif ih.btnp_select():
                self.screen = "title"
            return

        move = int(ih.btn_right()) - int(ih.btn_left())
        if not self.core.ball.in_play and self.core.server == 0:
            self.core.player_x = self.core._clamp(self.core.player_x + move * 3.0)
        else:
            self.core.tick(player_move=move)
        if ih.btnp_a():
            self._hit_or_serve(power=False)
        if ih.btnp_b():
            self._hit_or_serve(power=True)
        if ih.btnp_start():
            self.core.serve()
            pyxel.play(3, 0)

    def _hit_or_serve(self, power: bool) -> None:
        if not self.core.ball.in_play:
            ok = self.core.serve()
        else:
            ok = self.core.hit(0, power=power)
        pyxel.play(3, 1 if ok else 2)
        self.flash = 3 if ok else 0

    def draw(self) -> None:
        pyxel.cls(11 if self.flash else 1)
        if self.screen == "title":
            self._draw_title()
            return
        self._draw_court()
        self._draw_players()
        self._draw_ball()
        self._draw_hud()
        if self.core.match_over:
            winner = "player" if self.core.winner == 0 else "ai"
            self._panel(f"{winner} wins", "A replay   Select title")

    def _draw_title(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 3)
        pyxel.rect(40, 18, 160, 204, 11)
        pyxel.rectb(40, 18, 160, 204, 7)
        pyxel.line(120, 18, 120, 222, 7)
        pyxel.line(40, 120, 200, 120, 7)
        self._draw_racket(85, 124, 8)
        self._draw_racket(155, 84, 12)
        pyxel.circ(127, 104, 5, 10)
        self._center("PICO TENNIS", 54, 0)
        self._center("paranoidcactus", 76, 5)
        self._center("A serve / hit", 178, 0)
        self._center("B power shot", 192, 0)
        self._center("A start", 212, 7 if pyxel.frame_count % 40 < 28 else 5)

    def _draw_court(self) -> None:
        x0, y0 = self._xy((self.core.court_left, 0))
        x1, y1 = self._xy((self.core.court_right, self.core.height))
        pyxel.rect(x0, y0, x1 - x0, y1 - y0, 3)
        pyxel.rectb(x0, y0, x1 - x0, y1 - y0, 7)
        pyxel.line(x0, (y0 + y1) // 2, x1, (y0 + y1) // 2, 7)
        pyxel.line((x0 + x1) // 2, y0, (x0 + x1) // 2, y1, 6)
        pyxel.rect(x0, (y0 + y1) // 2 - 2, x1 - x0, 4, 0)
        pyxel.line(x0 + 18, y0 + 44, x1 - 18, y0 + 44, 6)
        pyxel.line(x0 + 18, y1 - 44, x1 - 18, y1 - 44, 6)

    def _draw_players(self) -> None:
        px, py = self._xy((self.core.player_x, self.core.player_y))
        ax, ay = self._xy((self.core.ai_x, self.core.ai_y))
        self._draw_racket(px, py, 12)
        self._draw_racket(ax, ay, 8)

    def _draw_racket(self, x: int, y: int, color: int) -> None:
        pyxel.circ(x, y - 4, 7, color)
        pyxel.circb(x, y - 4, 8, 7)
        pyxel.line(x, y + 3, x - 8, y + 17, 4)
        pyxel.rect(x - 5, y + 11, 10, 10, 15)

    def _draw_ball(self) -> None:
        x, y = self._xy((self.core.ball.x, self.core.ball.y))
        pyxel.circ(x, y, 4, 10)
        pyxel.pset(x - 1, y - 1, 7)

    def _draw_hud(self) -> None:
        labels = ["0", "15", "30", "40"]
        p0 = labels[min(3, self.core.points[0])]
        p1 = labels[min(3, self.core.points[1])]
        pyxel.rect(0, 0, SCREEN, 24, 0)
        pyxel.text(5, 5, f"P {self.core.games[0]}-{self.core.games[1]} AI   pts {p0}-{p1}", 7)
        pyxel.text(5, 15, self.core.message[:38], 10)
        meter = self.core.power[0]
        pyxel.rect(170, 7, 48, 6, 5)
        pyxel.rect(170, 7, meter * 8, 6, 10)
        pyxel.text(170, 16, "power", 7)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 94, 192, 52, 0)
        pyxel.rectb(24, 94, 192, 52, 7)
        self._center(title, 112, 10)
        self._center(subtitle, 130, 7)

    @staticmethod
    def _xy(pos: tuple[float, float]) -> tuple[int, int]:
        return int(OX + pos[0] * SCALE), int(OY + pos[1] * SCALE)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    PicoTennis()

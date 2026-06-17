"""Combo Pool — PyxelPico port.

Adapted from the PICO-8 cart by NuSan (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=3467
"""

from __future__ import annotations

import math
import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from combopool_core import ComboPoolCore  # noqa: E402


SCREEN = 240
BALL_COLORS = [0, 11, 10, 9, 13, 8, 14]


class ComboPool:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Combo Pool", fps=30)
        self.core = ComboPoolCore()
        self.mode = "title"
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c4", "t", "5", "n", 4)
        pyxel.sound(1).set("e4g4c5", "p", "7", "n", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 12)

    def reset(self) -> None:
        self.core.reset()
        self.mode = "play"

    def update(self) -> None:
        if self.mode == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            return
        if self.mode in {"won", "lost"}:
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            elif ih.btnp_b() or ih.btnp_select():
                self.mode = "title"
            return
        direction = int(ih.btn_right()) - int(ih.btn_left())
        self.core.rotate_aim(direction, slow=ih.btn_b() or ih.btn_down())
        if ih.btnp_a():
            self.core.shoot()
            pyxel.play(3, 0)
        old_combo = self.core.combo
        old_life = self.core.life
        self.core.tick()
        if self.core.combo > old_combo:
            pyxel.play(3, 1)
        elif self.core.life < old_life and pyxel.frame_count % 15 == 0:
            pyxel.play(3, 2)
        if self.core.won:
            self.mode = "won"
        elif self.core.lost:
            self.mode = "lost"

    def draw(self) -> None:
        pyxel.cls(1)
        if self.mode == "title":
            self._draw_title()
            return
        self._draw_table()
        for ball in self.core.balls:
            self._draw_ball(ball)
        self._draw_launcher()
        self._draw_hud()
        if self.mode == "won":
            self._panel("pink combo", "A retry  B title")
        elif self.mode == "lost":
            self._panel("sudden death", "A retry  B title")

    def _draw_title(self) -> None:
        self._draw_table()
        self._center("combo pool", 52, 10)
        self._center("merge matching marbles", 68, 7)
        for i in range(5):
            pyxel.circ(76 + i * 22, 126, 9, BALL_COLORS[i + 1])
        self._center("left/right aim  A shoot", 194, 7)
        self._center("hold B for fine aim", 208, 7)

    def _draw_table(self) -> None:
        pyxel.rect(8, 32, 224, 200, 3)
        pyxel.rectb(8, 32, 224, 200, 11)
        for x, y in ((8, 32), (232, 32), (8, 232), (232, 232)):
            pyxel.circ(x, y, 10, 0)

    def _draw_launcher(self) -> None:
        x, y = 24, 120
        tx = x + math.cos(self.core.aim) * 34
        ty = y + math.sin(self.core.aim) * 34
        pyxel.line(x, y, int(tx), int(ty), 7)
        pyxel.circ(x, y, 6, 10 if self.core.cooldown == 0 else 5)

    def _draw_ball(self, ball) -> None:
        color = BALL_COLORS[min(ball.level, len(BALL_COLORS) - 1)]
        pyxel.circ(int(ball.x), int(ball.y), self.core.radius, color)
        pyxel.circb(int(ball.x), int(ball.y), self.core.radius, 0)
        pyxel.text(int(ball.x) - 2, int(ball.y) - 3, str(ball.level), 0)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 28, 0)
        pyxel.text(8, 6, f"score {self.core.score}", 7)
        pyxel.text(94, 6, f"combo {self.core.combo}", 7)
        pyxel.text(168, 6, f"balls {len(self.core.balls)}", 7)
        pyxel.rect(8, 20, 160, 5, 5)
        pyxel.rect(8, 20, max(0, int(160 * self.core.life / 80)), 5, 8 if self.core.life < 20 else 11)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(28, 92, 184, 54, 0)
        pyxel.rectb(28, 92, 184, 54, 7)
        self._center(title, 108, 11)
        self._center(subtitle, 128, 6)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    ComboPool()

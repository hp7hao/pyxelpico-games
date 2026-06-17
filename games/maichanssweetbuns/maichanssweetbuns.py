"""Mai-Chan's Sweet Buns — PyxelPico port.

Adapted from the PICO-8 cart by Krystman (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=31864
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from maichanssweetbuns_core import BakeryCore, BunKind, OrderState  # noqa: E402


SCREEN = 240
CHOICES = (BunKind.PLAIN, BunKind.JAM, BunKind.CHOCOLATE, BunKind.TEA)
COLORS = {
    BunKind.PLAIN: 10,
    BunKind.JAM: 8,
    BunKind.CHOCOLATE: 4,
    BunKind.TEA: 11,
}


class MaiChansSweetBuns:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Mai-Chan's Sweet Buns", fps=30)
        self.core = BakeryCore()
        self.mode = "title"
        self.cursor = 0
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c4e4", "t", "5", "n", 5)
        pyxel.sound(1).set("g4c5e5", "p", "7", "n", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 12)

    def reset(self) -> None:
        self.core.reset()
        self.mode = "play"
        self.cursor = 0
        self.flash = 0

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.mode == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            return
        if self.mode == "gameover":
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            elif ih.btnp_b() or ih.btnp_select():
                self.mode = "title"
            return

        if ih.btnp_left():
            self.cursor = (self.cursor - 1) % len(CHOICES)
        elif ih.btnp_right():
            self.cursor = (self.cursor + 1) % len(CHOICES)
        elif ih.btnp_up():
            self.cursor = max(0, self.cursor - 2)
        elif ih.btnp_down():
            self.cursor = min(len(CHOICES) - 1, self.cursor + 2)
        elif ih.btnp_a():
            prev_patience = self.core.patience
            self.core.choose(CHOICES[self.cursor])
            pyxel.play(3, 0 if self.core.patience == prev_patience else 2)
            if self.core.patience < prev_patience:
                self.flash = 8
        elif ih.btnp_b() or ih.btnp_start():
            self.core.serve()
            pyxel.play(3, 1)

        if pyxel.frame_count % 30 == 0:
            self.core.tick()
        if self.core.state is OrderState.GAME_OVER:
            self.mode = "gameover"

    def draw(self) -> None:
        pyxel.cls(7 if self.flash == 0 else 8)
        if self.mode == "title":
            self._draw_title()
            return
        self._draw_shop()
        if self.mode == "gameover":
            self._panel("closed", "A retry  B title")

    def _draw_title(self) -> None:
        self._draw_shop_backdrop()
        self._center("mai-chan's", 48, 4)
        self._center("sweet buns", 64, 8)
        self._draw_mai(120, 120)
        self._center("match the order", 184, 6)
        self._center("press A", 210, 11)

    def _draw_shop(self) -> None:
        self._draw_shop_backdrop()
        pyxel.rect(0, 0, SCREEN, 28, 0)
        pyxel.text(8, 6, f"day {self.core.day}", 7)
        pyxel.text(70, 6, f"score {self.core.score}", 7)
        pyxel.text(150, 6, "pat " + "*" * self.core.patience, 8 if self.core.patience <= 1 else 7)
        pyxel.rect(8, 22, 224, 4, 5)
        pyxel.rect(8, 22, int(224 * self.core.timer / 48), 4, 10)

        self._center("order", 42, 0)
        for index, bun in enumerate(self.core.order):
            self._draw_bun(82 + index * 26, 64, bun)
        self._center("tray", 92, 0)
        for index, bun in enumerate(self.core.tray):
            self._draw_bun(82 + index * 26, 114, bun)
        self._draw_choices()
        self._center(self.core.message, 216, 5)

    def _draw_choices(self) -> None:
        for index, bun in enumerate(CHOICES):
            x = 66 + (index % 2) * 108
            y = 154 + (index // 2) * 32
            color = 0 if index == self.cursor else 6
            pyxel.rectb(x - 30, y - 12, 60, 24, color)
            self._draw_bun(x - 16, y, bun)
            pyxel.text(x - 2, y - 3, bun.value[:4], color)

    def _draw_shop_backdrop(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 7)
        pyxel.rect(0, 170, SCREEN, 70, 4)
        pyxel.rect(20, 36, 200, 104, 10)
        pyxel.rectb(20, 36, 200, 104, 4)
        pyxel.rect(34, 78, 172, 8, 4)

    def _draw_mai(self, x: int, y: int) -> None:
        pyxel.circ(x, y - 8, 12, 12)
        pyxel.rect(x - 10, y + 4, 20, 28, 8)
        pyxel.circ(x - 5, y - 10, 1, 0)
        pyxel.circ(x + 5, y - 10, 1, 0)
        pyxel.rect(x - 13, y - 24, 26, 8, 0)
        pyxel.rect(x - 11, y - 30, 22, 8, 7)

    def _draw_bun(self, x: int, y: int, bun: BunKind) -> None:
        color = COLORS[bun]
        pyxel.circ(x, y, 9, color)
        pyxel.rect(x - 8, y, 16, 7, color)
        pyxel.rectb(x - 8, y - 4, 16, 12, 4)
        if bun is BunKind.JAM:
            pyxel.circ(x, y, 3, 14)
        elif bun is BunKind.CHOCOLATE:
            pyxel.line(x - 6, y - 2, x + 6, y + 4, 0)
        elif bun is BunKind.TEA:
            pyxel.rect(x - 4, y - 7, 8, 4, 3)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(28, 92, 184, 54, 0)
        pyxel.rectb(28, 92, 184, 54, 7)
        self._center(title, 108, 11)
        self._center(subtitle, 128, 6)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    MaiChansSweetBuns()

"""Marballs 2 — PyxelPico port.

Adapted from the PICO-8 cart by lucatron (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=28414
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from marballs2_core import Marballs2Core  # noqa: E402


SCREEN = 240
TILE = 12


class Marballs2:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Marballs 2", fps=30)
        self.core = Marballs2Core()
        self.mode = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c4e4g4", "p", "6", "n", 8)
        pyxel.sound(1).set("g3c4g4", "s", "6", "f", 9)
        pyxel.sound(2).set("c2", "n", "7", "f", 12)
        pyxel.sound(3).set("e4g4c5", "t", "6", "n", 10)

    def reset(self) -> None:
        self.core.restart()
        self.mode = "play"
        self.flash = 0

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.mode == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.mode = "play"
                pyxel.play(3, 0)
            elif ih.btnp_b() or ih.btnp_select():
                self.core.rotated_controls = not self.core.rotated_controls
            return
        if self.core.cleared:
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            elif ih.btnp_select():
                self.mode = "title"
            return
        if ih.btnp_b() or ih.btnp_select():
            self.reset()
            return

        old_message = self.core.message
        self.core.tick(left=ih.btn_left(), right=ih.btn_right(), up=ih.btn_up(), down=ih.btn_down())
        if self.core.message != old_message:
            if self.core.message == "jump pad":
                pyxel.play(3, 1)
            elif self.core.message == "wall bounce":
                pyxel.play(3, 2)
                self.flash = 3
            elif self.core.message in ("orb", "goal"):
                pyxel.play(3, 3)

    def draw(self) -> None:
        pyxel.cls(1 if self.flash == 0 else 8)
        if self.mode == "title":
            self._draw_title()
            return
        cam_x = max(0, min(self.core.width * TILE - SCREEN, int(self.core.ball.x - SCREEN / 2)))
        cam_y = max(0, min(self.core.height * TILE - SCREEN, int(self.core.ball.y - SCREEN / 2)))
        self._draw_level(cam_x, cam_y)
        self._draw_ball(cam_x, cam_y)
        self._draw_hud()
        if self.core.cleared:
            self._panel("goal", f"{self.core.medal}  {self.core.time / 30:.1f}s")

    def _draw_title(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        for y in range(48, 186, 18):
            pyxel.line(38, y, 202, y - 32, 5)
            pyxel.line(38, y + 1, 202, y - 31, 13)
        pyxel.circ(120, 120, 18, 10)
        pyxel.circb(120, 120, 18, 7)
        pyxel.circ(132, 112, 5, 7)
        self._center("marballs 2", 48, 11)
        self._center("lucatron", 64, 6)
        self._center("D-pad roll  A start", 198, 7)
        self._center("B toggles 45 deg controls", 212, 13)

    def _draw_level(self, cam_x: int, cam_y: int) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 0)
        for y, row in enumerate(self.core.tiles):
            for x, tile in enumerate(row):
                sx = x * TILE - cam_x
                sy = y * TILE - cam_y
                if sx < -TILE or sy < -TILE or sx > SCREEN or sy > SCREEN:
                    continue
                if tile == "#":
                    pyxel.rect(sx, sy, TILE, TILE, 5)
                    pyxel.rectb(sx, sy, TILE, TILE, 13)
                else:
                    pyxel.rect(sx, sy, TILE, TILE, 1 if (x + y) % 2 else 0)
                    if tile == "J":
                        pyxel.tri(sx + 2, sy + 10, sx + 6, sy + 2, sx + 10, sy + 10, 10)
                    elif tile == "o":
                        pyxel.circ(sx + 6, sy + 6, 4, 9)
                        pyxel.circ(sx + 6, sy + 6, 2, 10)
                    elif tile == "G":
                        color = 11 if self.core.orbs >= self.core.total_orbs else 4
                        pyxel.rect(sx + 2, sy + 2, 8, 8, color)
                        pyxel.rectb(sx + 2, sy + 2, 8, 8, 7)

    def _draw_ball(self, cam_x: int, cam_y: int) -> None:
        x = int(self.core.ball.x - cam_x)
        y = int(self.core.ball.y - cam_y + self.core.ball.z)
        shadow = max(2, 6 + int(self.core.ball.z / 2))
        pyxel.elli(x - shadow, int(self.core.ball.y - cam_y) + 5, shadow * 2, 4, 0)
        pyxel.circ(x, y, 6, 10)
        pyxel.circb(x, y, 6, 7)
        pyxel.pset(x - 2, y - 3, 7)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 28, 0)
        pyxel.text(8, 6, f"orbs {self.core.orbs}/{self.core.total_orbs}", 7)
        pyxel.text(84, 6, f"time {self.core.time / 30:.1f}", 10)
        pyxel.text(158, 6, "45" if self.core.rotated_controls else "std", 6)
        pyxel.text(8, 18, self.core.message[:28], 13)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 92, 192, 56, 0)
        pyxel.rectb(24, 92, 192, 56, 7)
        self._center(title, 110, 11)
        self._center(subtitle, 130, 6)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    Marballs2()

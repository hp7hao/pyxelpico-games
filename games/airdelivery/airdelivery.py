"""Air Delivery — PyxelPico port.

Adapted from the PICO-8 cart by pianoman373 (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=52598
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from airdelivery_core import AirDeliveryCore  # noqa: E402


SCREEN = 240
TILE = 12


class AirDelivery:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Air Delivery", fps=30)
        self.core = AirDeliveryCore()
        self.mode = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c4e4g4", "p", "6", "n", 8)
        pyxel.sound(1).set("g4c5", "s", "5", "f", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 10)
        pyxel.sound(3).set("e4g4c5e5", "t", "6", "n", 12)

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
            return
        if self.core.cleared:
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            elif ih.btnp_select():
                self.mode = "title"
            return

        old_message = self.core.message
        old_deaths = self.core.deaths
        self.core.tick(
            left=ih.btn_left(),
            right=ih.btn_right(),
            up=ih.btn_up(),
            down=ih.btn_down(),
            jump=ih.btnp_a(),
            interact=ih.btn_b() or ih.btnp_b(),
        )
        if self.core.deaths > old_deaths:
            pyxel.play(3, 2)
            self.flash = 5
        elif self.core.message != old_message:
            if "letter" in self.core.message or "passage" in self.core.message:
                pyxel.play(3, 1)
            elif self.core.cleared:
                pyxel.play(3, 3)

    def draw(self) -> None:
        pyxel.cls(12 if self.flash == 0 else 8)
        if self.mode == "title":
            self._draw_title()
            return
        cam_x = max(0, min(self.core.width * TILE - SCREEN, int(self.core.player.x - SCREEN / 2)))
        cam_y = max(0, min(self.core.height * TILE - SCREEN, int(self.core.player.y - SCREEN / 2)))
        self._draw_sky(cam_x, cam_y)
        self._draw_room(cam_x, cam_y)
        self._draw_player(cam_x, cam_y)
        self._draw_hud()
        if self.core.cleared:
            self._panel("airship ready", "A replay  Select title")

    def _draw_title(self) -> None:
        self._draw_sky(0, 0)
        pyxel.rect(54, 146, 132, 16, 3)
        pyxel.rect(80, 118, 80, 28, 11)
        pyxel.tri(96, 118, 132, 92, 160, 118, 7)
        self._draw_worker(120, 142)
        self._center("air delivery", 52, 0)
        self._center("pianoman373", 68, 5)
        self._center("A start", 210, 10 if pyxel.frame_count % 30 < 22 else 6)

    def _draw_sky(self, cam_x: int, cam_y: int) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 12)
        for i in range(8):
            x = (i * 47 - cam_x // 4 + pyxel.frame_count // 3) % 280 - 30
            y = 28 + (i * 31 - cam_y // 6) % 160
            pyxel.circ(x, y, 10, 7)
            pyxel.circ(x + 10, y + 2, 8, 7)
            pyxel.rect(x - 10, y + 4, 30, 6, 7)

    def _draw_room(self, cam_x: int, cam_y: int) -> None:
        for y, row in enumerate(self.core.tiles):
            for x, tile in enumerate(row):
                sx = x * TILE - cam_x
                sy = y * TILE - cam_y
                if sx < -TILE or sy < -TILE or sx > SCREEN or sy > SCREEN:
                    continue
                if tile == "#":
                    pyxel.rect(sx, sy, TILE, TILE, 3)
                    pyxel.rectb(sx, sy, TILE, TILE, 11)
                elif tile == "H":
                    pyxel.line(sx + 3, sy, sx + 3, sy + TILE, 4)
                    pyxel.line(sx + 9, sy, sx + 9, sy + TILE, 4)
                    pyxel.line(sx + 3, sy + 6, sx + 9, sy + 6, 4)
                elif tile == "L":
                    pyxel.rect(sx + 3, sy + 4, 7, 5, 7)
                    pyxel.line(sx + 3, sy + 4, sx + 6, sy + 7, 10)
                elif tile == "R":
                    self._draw_recipient(sx + 6, sy + 10, 10)
                elif tile == "r":
                    self._draw_recipient(sx + 6, sy + 10, 5)
                elif tile == "D":
                    pyxel.rect(sx, sy, TILE, TILE, 4)
                    pyxel.text(sx + 3, sy + 3, "?", 7)
                elif tile == "^":
                    pyxel.tri(sx, sy + TILE, sx + 6, sy + 2, sx + TILE, sy + TILE, 8)
                elif tile == "A":
                    pyxel.rect(sx - 4, sy + 3, 20, 7, 5)
                    pyxel.tri(sx + 2, sy + 3, sx + 8, sy - 5, sx + 14, sy + 3, 7)

    def _draw_player(self, cam_x: int, cam_y: int) -> None:
        self._draw_worker(int(self.core.player.x - cam_x + 4), int(self.core.player.y - cam_y + 10))
        if self.core.player.has_glider and self.core.player.dy > 0:
            x = int(self.core.player.x - cam_x + 4)
            y = int(self.core.player.y - cam_y - 2)
            pyxel.line(x - 12, y, x, y - 5, 7)
            pyxel.line(x, y - 5, x + 12, y, 7)

    def _draw_worker(self, x: int, y: int) -> None:
        pyxel.circ(x, y - 12, 4, 10)
        pyxel.rect(x - 4, y - 8, 8, 8, 5)
        pyxel.rect(x + 4, y - 7, 5, 4, 7)
        pyxel.line(x - 3, y, x - 7, y + 5, 1)
        pyxel.line(x + 3, y, x + 7, y + 5, 1)

    def _draw_recipient(self, x: int, y: int, color: int) -> None:
        pyxel.circ(x, y - 8, 4, color)
        pyxel.rect(x - 4, y - 4, 8, 7, 5)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 28, 0)
        pyxel.text(8, 6, f"letters {self.core.letters}/{self.core.found_letters}", 7)
        pyxel.text(88, 6, f"delivered {self.core.delivered}/{self.core.total_recipients}", 10)
        tools = ("G" if self.core.player.has_glider else "-") + ("D" if self.core.player.has_drill else "-")
        pyxel.text(190, 6, tools, 6)
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
    AirDelivery()

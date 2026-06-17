"""BAS — PyxelPico port.

Adapted from the PICO-8 cart by yokozuna/yokoboko (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=54986
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from bas_core import BasCore  # noqa: E402


SCREEN = 240


class Bas:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="BAS", fps=30)
        self.core = BasCore()
        self.mode = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c4e4", "p", "6", "n", 5)
        pyxel.sound(1).set("g3", "t", "7", "f", 7)
        pyxel.sound(2).set("c2", "n", "7", "f", 12)
        pyxel.sound(3).set("e4g4c5", "s", "7", "n", 10)

    def reset(self) -> None:
        highscore = self.core.highscore
        self.core.restart()
        self.core.highscore = highscore
        self.mode = "play"
        self.flash = 0

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.mode == "title":
            if ih.btnp_a() or ih.btnp_left() or ih.btnp_right() or ih.btnp_start():
                self.mode = "play"
            return
        if self.core.state == "dead":
            if ih.btnp_a() or ih.btnp_b() or ih.btnp_start():
                self.reset()
            elif ih.btnp_select():
                self.mode = "title"
            return

        old_score = self.core.score
        if ih.btnp_left() or ih.btnp_a():
            self.core.jump(False)
            pyxel.play(3, 0)
        elif ih.btnp_right() or ih.btnp_b():
            self.core.jump(True)
            pyxel.play(3, 0)
        self.core.tick()
        if self.core.score > old_score:
            pyxel.play(3, 3)
        if self.core.state == "dead":
            pyxel.play(3, 2)
            self.flash = 6

    def draw(self) -> None:
        pyxel.cls(0 if self.flash == 0 else 2)
        if self.mode == "title":
            self._draw_title()
            return
        camera_y = self.core.camera_y
        self._draw_background(camera_y)
        self._draw_columns(camera_y)
        self._draw_trap(camera_y)
        self._draw_player(camera_y)
        self._draw_hud()
        if self.core.state == "dead":
            self._panel("game over", "A retry  Select title")

    def _draw_title(self) -> None:
        self._draw_background(self.core.camera_y)
        self._center("bas", 54, 11)
        self._center("yokoboko", 68, 6)
        self._draw_bird(120, 116, True)
        pyxel.circ(66, 116, 11, 8)
        pyxel.circ(174, 116, 11, 8)
        self._center("left/A jump left", 182, 7)
        self._center("right/B jump right", 196, 7)
        if pyxel.frame_count % 30 < 22:
            self._center("press A", 216, 10)

    def _draw_background(self, camera_y: float) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        for y in range(-40, SCREEN + 40, 24):
            yy = int(y - camera_y * 0.15) % 264 - 24
            pyxel.line(0, yy, SCREEN, yy, 13)
        pyxel.rect(18, 0, 18, SCREEN, 5)
        pyxel.rect(204, 0, 18, SCREEN, 5)
        pyxel.rectb(18, 0, 18, SCREEN, 13)
        pyxel.rectb(204, 0, 18, SCREEN, 13)

    def _draw_columns(self, camera_y: float) -> None:
        for saw in self.core.columns.saws:
            y = int(saw.tile * self.core.tile_height - camera_y)
            x = int(self.core.right_x if saw.right_wall else self.core.left_x)
            if -20 <= y <= SCREEN + 20:
                self._draw_saw(x, y)

    def _draw_saw(self, x: int, y: int) -> None:
        pyxel.circ(x, y, 9, 6)
        pyxel.circb(x, y, 9, 7)
        for i in range(8):
            dx = -9 if i % 2 == 0 else 9
            dy = -9 if i < 4 else 9
            pyxel.line(x, y, x + dx, y + dy, 7)
        pyxel.circ(x, y, 3, 0)

    def _draw_trap(self, camera_y: float) -> None:
        y = int(self.core.trap_y - camera_y)
        pyxel.rect(0, y, SCREEN, SCREEN - y, 8)
        pyxel.line(0, y, SCREEN, y, 9)
        for x in range(0, SCREEN, 12):
            pyxel.tri(x, y, x + 6, y - 10, x + 12, y, 9)

    def _draw_player(self, camera_y: float) -> None:
        self._draw_bird(int(self.core.player.x), int(self.core.player.y - camera_y), self.core.player.right_wall)

    def _draw_bird(self, x: int, y: int, facing_left: bool) -> None:
        pyxel.elli(x - 8, y - 7, 16, 14, 10)
        beak = -1 if facing_left else 1
        pyxel.tri(x + beak * 5, y - 1, x + beak * 15, y + 3, x + beak * 5, y + 7, 9)
        pyxel.line(x - 4, y, x - 14, y - 8, 7)
        pyxel.line(x + 4, y, x + 14, y - 8, 7)
        pyxel.pset(x + beak * 3, y - 3, 0)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 24, 0)
        pyxel.text(8, 6, f"score {self.core.score}", 7)
        pyxel.text(88, 6, f"best {self.core.highscore}", 7)
        pyxel.text(168, 6, self.core.state, 6)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(28, 92, 184, 54, 0)
        pyxel.rectb(28, 92, 184, 54, 7)
        self._center(title, 108, 11)
        self._center(subtitle, 128, 6)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    Bas()

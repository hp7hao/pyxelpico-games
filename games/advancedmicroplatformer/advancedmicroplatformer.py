"""Advanced Micro Platformer - PyxelPico port.

Adapted from the PICO-8 platforming starter kit by mhughson
(CC BY-NC-SA 4.0). Original BBS thread:
https://www.lexaloffle.com/bbs/?tid=28793
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from advancedmicroplatformer_core import AdvancedMicroPlatformerCore  # noqa: E402


SCREEN = 240


class AdvancedMicroPlatformer:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Advanced Micro Platformer", fps=30)
        self.core = AdvancedMicroPlatformerCore()
        self.screen = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3e3g3", "t", "5", "n", 8)
        pyxel.sound(1).set("g3c4", "p", "6", "f", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 8)
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
                self.core.restart()
                self.flash = 4
            return
        if ih.btnp_a():
            if self.core.press_jump():
                pyxel.play(3, 0)
        if ih.btnp_start() or ih.btnp_select():
            self.core.restart()
        self.core.tick(left=ih.btn_left(), right=ih.btn_right(), jump_held=ih.btn_a())
        if self.core.level_clear:
            pyxel.play(3, 3)

    def draw(self) -> None:
        pyxel.cls(12 if self.flash else 1)
        if self.screen == "title":
            self._draw_title()
            return
        self._draw_world()
        self._draw_player()
        self._draw_hud()
        if self.core.level_clear:
            self._panel("demo complete", "A replay")

    def _draw_title(self) -> None:
        self._draw_background()
        self._center("ADV MICRO", 54, 7)
        self._center("PLATFORMER", 70, 10)
        self._center("starter-kit demo", 92, 13)
        self._draw_player_at(120, 142)
        self._center("A start", 210, 7 if pyxel.frame_count % 30 < 22 else 5)

    def _draw_world(self) -> None:
        self._draw_background()
        for x, y, w, h, kind in self.core.visible_rects():
            if kind == "one_way":
                pyxel.rect(x, y, w, h, 11)
                pyxel.line(x, y, x + w, y, 7)
            else:
                pyxel.rect(x, y, w, h, 3)
                pyxel.rectb(x, y, w, h, 0)
        gx = int(self.core.goal_x - self.core.camera_x)
        pyxel.circ(gx, int(self.core.goal_y), 8, 10)
        pyxel.circb(gx, int(self.core.goal_y), 10, 7)

    def _draw_background(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        for y in range(28, 220, 28):
            pyxel.line(0, y, SCREEN, y - 16, 13)

    def _draw_player(self) -> None:
        x = int(self.core.player_x - self.core.camera_x)
        y = int(self.core.player_y)
        self._draw_player_at(x, y)

    def _draw_player_at(self, x: int, y: int) -> None:
        pyxel.rect(x - 6, y - 14, 12, 28, 8)
        pyxel.rect(x - 4, y - 10, 8, 8, 10)
        pyxel.pset(x - 2, y - 8, 0)
        pyxel.pset(x + 2, y - 8, 0)
        pyxel.line(x - 5, y + 15, x - 9, y + 19, 9)
        pyxel.line(x + 5, y + 15, x + 9, y + 19, 9)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 24, 0)
        pyxel.text(6, 5, f"camera {int(self.core.camera_x):03d}", 7)
        pyxel.text(86, 5, "coyote" if self.core.coyote_timer else "air", 10)
        pyxel.text(148, 5, self.core.message[:22], 13)
        pyxel.rect(0, 222, SCREEN, 18, 0)
        pyxel.text(24, 228, "D-pad move  hold A jump  Start restart", 7)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 92, 192, 56, 0)
        pyxel.rectb(24, 92, 192, 56, 7)
        self._center(title, 111, 10)
        self._center(subtitle, 130, 7)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    AdvancedMicroPlatformer()

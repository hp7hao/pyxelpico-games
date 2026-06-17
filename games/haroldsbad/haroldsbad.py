"""Harold's Bad Day - PyxelPico port.

Adapted from the PICO-8 cart by biovoid (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=45507
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from haroldsbad_core import HaroldsBadCore  # noqa: E402


SCREEN = 240


class HaroldsBad:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Harold's Bad Day", fps=30)
        self.core = HaroldsBadCore()
        self.screen = "title"
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3e3g3", "t", "456", "n", 12)
        pyxel.sound(1).set("c2", "n", "7", "f", 12)
        pyxel.sound(2).set("g4e4c4", "s", "666", "n", 10)
        pyxel.sound(3).set("c4g4c5", "p", "567", "n", 18)

    def update(self) -> None:
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if ih.btnp_select():
            self.core.restart()
            return
        if self.core.level_complete:
            if ih.btnp_a() or ih.btnp_start():
                self.core.next_level()
                pyxel.play(3, 3)
            return
        if self.core.game_over:
            if ih.btnp_a() or ih.btnp_start():
                self.core.restart()
            return
        before_deaths = self.core.deaths
        move = int(ih.btn_right()) - int(ih.btn_left())
        self.core.tick(move=move, jump=ih.btnp_a())
        if self.core.deaths > before_deaths:
            pyxel.play(3, 1)
        elif ih.btnp_a():
            pyxel.play(3, 0)

    def draw(self) -> None:
        pyxel.cls(1)
        if self.screen == "title":
            self._draw_level()
            self._draw_title()
            return
        self._draw_level()
        self._draw_corpses()
        self._draw_player()
        self._draw_hud()
        if self.core.level_complete:
            self._panel("level clear", "A next bad day")
        elif self.core.game_over:
            self._panel("no harolds left", "A retry")

    def _draw_level(self) -> None:
        pyxel.rect(0, 0, SCREEN, 240, 1)
        pyxel.rect(0, self.core.ground_y + 9, SCREEN, 60, 3)
        pyxel.rect(0, self.core.ground_y, 88, 10, 6)
        pyxel.rect(118, self.core.ground_y, 58, 10, 6)
        pyxel.rect(194, self.core.ground_y, 46, 10, 6)
        pyxel.rect(112, 180, 54, 42, 12)
        for x in range(178, 194, 5):
            pyxel.tri(x, self.core.ground_y, x + 3, self.core.ground_y - 9, x + 6, self.core.ground_y, 8)
        pyxel.rect(self.core.goal_x - 6, self.core.ground_y - 30, 12, 30, 10)
        pyxel.rect(self.core.goal_x - 10, self.core.ground_y - 36, 20, 7, 7)
        pyxel.text(24, 70, "sometimes dying helps", 7)
        pyxel.text(116, 168, "water", 7)

    def _draw_corpses(self) -> None:
        for corpse in self.core.corpses:
            pyxel.rect(int(corpse.x) - 10, int(corpse.y) - 10, 21, 8, 13)
            pyxel.circ(int(corpse.x) - 8, int(corpse.y) - 12, 4, 13)

    def _draw_player(self) -> None:
        p = self.core.player
        if p.dead:
            return
        x, y = int(p.x), int(p.y)
        pyxel.rect(x - 5, y - 15, 10, 15, 7)
        pyxel.circ(x, y - 20, 5, 15)
        pyxel.pset(x - 2, y - 21, 0)
        pyxel.pset(x + 2, y - 21, 0)
        pyxel.line(x - 3, y, x - 6, y + 7, 7)
        pyxel.line(x + 3, y, x + 6, y + 7, 7)
        if p.drown_timer > 0:
            pyxel.text(x - 10, y - 32, f"{self.core.drown_frames - p.drown_timer}", 7)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 26, 0)
        pyxel.text(5, 5, f"level {self.core.level}/32  lives {self.core.lives}  deaths {self.core.deaths}", 7)
        pyxel.text(5, 16, f"saved {self.core.harolds_saved}  {self.core.message[:24]}", 10)
        pyxel.text(5, 228, "D-pad move  A jump  Select reset", 6)

    def _draw_title(self) -> None:
        pyxel.rect(20, 48, 200, 70, 0)
        pyxel.rectb(20, 48, 200, 70, 7)
        self._center("HAROLD'S BAD DAY", 64, 7)
        self._center("biovoid", 82, 6)
        self._center("save harolds by using them", 100, 10)
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
    HaroldsBad()

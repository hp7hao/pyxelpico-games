"""subsurface - PyxelPico port.

Adapted from the PICO-8 cart by JulianR (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=54080
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from subsurface_core import SubsurfaceCore  # noqa: E402


SCREEN = 240


class Subsurface:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="subsurface", fps=30)
        self.core = SubsurfaceCore()
        self.screen = "title"
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3g3", "t", "65", "n", 10)
        pyxel.sound(1).set("c4", "p", "6", "n", 6)
        pyxel.sound(2).set("c2", "n", "7", "f", 10)
        pyxel.sound(3).set("e3g3c4", "s", "567", "n", 16)

    def update(self) -> None:
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if ih.btnp_select():
            self.core.restart()
            return
        if self.core.victory:
            if ih.btnp_a() or ih.btnp_start():
                self.core.restart()
            return
        move = int(ih.btn_right()) - int(ih.btn_left())
        if ih.btnp_b():
            if self.core.shoot():
                pyxel.play(3, 1)
        if ih.btnp_up():
            self._grant_next_upgrade()
            pyxel.play(3, 3)
        self.core.tick(move=move, jump=ih.btnp_a(), hold_jump=ih.btn_a())

    def _grant_next_upgrade(self) -> None:
        for name in ("wall_jump", "double_jump", "glide", "swim", "health_1", "health_2"):
            if not self.core.upgrades[name]:
                self.core.collect_upgrade(name)
                return

    def draw(self) -> None:
        pyxel.cls(0)
        if self.screen == "title":
            self._draw_cavern()
            self._draw_title()
            return
        self._draw_cavern()
        self._draw_entities()
        self._draw_hud()
        if self.core.victory:
            self._panel("surface reached", "A descend again")

    def _draw_cavern(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        for i in range(16):
            x = i * 18 - (pyxel.frame_count // 3) % 18
            pyxel.line(x, 54, x + 20, 20 + (i % 4) * 8, 5)
        pyxel.rect(0, self.core.ground_y + 8, SCREEN, 70, 5)
        pyxel.rect(0, self.core.ground_y, 102, 9, 6)
        pyxel.rect(138, self.core.ground_y, 102, 9, 6)
        pyxel.rect(102, 180, 36, 52, 12)
        pyxel.rect(self.core.boss_x - 14, self.core.ground_y - 42, 28, 42, 2)
        pyxel.text(28, 70, "up finds next upgrade", 7)

    def _draw_entities(self) -> None:
        p = self.core.player
        pyxel.rect(int(p.x) - 5, int(p.y) - 15, 10, 15, 7)
        pyxel.circ(int(p.x), int(p.y) - 19, 5, 15)
        pyxel.line(int(p.x), int(p.y) - 10, int(p.x) + p.facing * 10, int(p.y) - 12, 10)
        for enemy in self.core.enemies:
            x = int(enemy["x"])
            pyxel.circ(x, self.core.ground_y - 9, 7, 8)
            pyxel.pset(x - 2, self.core.ground_y - 10, 0)
            pyxel.pset(x + 2, self.core.ground_y - 10, 0)
        for bullet in self.core.bullets:
            pyxel.rect(int(bullet["x"]) - 2, int(p.y) - 14, 5, 3, 10)
        if self.core.boss_hp > 0:
            pyxel.text(self.core.boss_x - 18, self.core.ground_y - 52, f"boss {self.core.boss_hp}", 7)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 32, 0)
        pyxel.text(5, 5, f"hp {self.core.health}/{self.core.max_health} energy {self.core.energy}", 7)
        unlocked = ",".join(k[:2] for k, v in self.core.upgrades.items() if v and k != "gun") or "none"
        pyxel.text(5, 16, f"upg {unlocked[:24]}", 10)
        pyxel.text(5, 228, "D-pad move  A jump/glide  B shoot  Up upgrade  Select reset", 6)

    def _draw_title(self) -> None:
        pyxel.rect(26, 52, 188, 76, 0)
        pyxel.rectb(26, 52, 188, 76, 7)
        self._center("subsurface", 68, 7)
        self._center("JulianR", 86, 6)
        self._center("40-screen metroidvania", 104, 10)
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
    Subsurface()

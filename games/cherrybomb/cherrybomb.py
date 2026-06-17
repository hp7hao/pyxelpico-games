"""Cherry Bomb - PyxelPico port.

Adapted from the PICO-8 cart by Krystian Majewski / Lazy Devs Academy
(CC BY-NC-SA 4.0). Original BBS thread:
https://www.lexaloffle.com/bbs/?tid=48986
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from cherrybomb_core import CherryBombCore, Enemy  # noqa: E402


SCREEN = 240


class CherryBomb:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Cherry Bomb", fps=30)
        self.core = CherryBombCore()
        self.screen = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c4c5", "t", "5", "n", 5)
        pyxel.sound(1).set("g3c4e4", "p", "6", "f", 8)
        pyxel.sound(2).set("f2c2", "n", "7", "f", 12)
        pyxel.sound(3).set("c3e3g3c4", "s", "5", "n", 14)

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if ih.btnp_start() or ih.btnp_select():
            self.core.restart()
            self.flash = 4
            return
        if self.core.game_over or self.core.victory:
            if ih.btnp_a():
                self.core.restart()
                self.flash = 4
            return

        before_lives = self.core.lives
        before_score = self.core.score
        if ih.btnp_a():
            if self.core.shoot():
                pyxel.play(3, 0)
        if ih.btnp_b():
            if self.core.bomb():
                self.flash = 6
                pyxel.play(3, 2)
        self.core.tick(left=ih.btn_left(), right=ih.btn_right(), up=ih.btn_up(), down=ih.btn_down())
        if self.core.lives < before_lives:
            self.flash = 10
            pyxel.play(3, 2)
        elif self.core.score > before_score:
            pyxel.play(3, 1)

    def draw(self) -> None:
        pyxel.cls(8 if self.flash else 0)
        if self.screen == "title":
            self._draw_title()
            return
        self._draw_starfield()
        self._draw_playfield()
        self._draw_hud()
        if self.core.game_over:
            self._panel("game over", "A retry")
        elif self.core.victory:
            self._panel("9 waves clear", "A replay")

    def _draw_title(self) -> None:
        self._draw_starfield()
        self._center("CHERRY BOMB", 54, 8)
        self._center("arcade shmup", 76, 7)
        self._draw_ship(120, 126, 8)
        for i in range(7):
            self._draw_cherry(60 + i * 20, 164 + (i % 2) * 8)
        self._center("A start", 210, 7 if pyxel.frame_count % 30 < 22 else 5)

    def _draw_starfield(self) -> None:
        for i in range(70):
            x = (i * 47 + pyxel.frame_count // 2) % SCREEN
            y = (i * 31 + pyxel.frame_count * (1 + i % 3)) % SCREEN
            pyxel.pset(x, y, [1, 5, 13][i % 3])

    def _draw_playfield(self) -> None:
        for bullet in self.core.bullets:
            x, y, _, _ = bullet
            pyxel.rect(int(x) - 1, int(y) - 5, 3, 8, 10)
        for bullet in self.core.enemy_bullets:
            x, y, _, _ = bullet
            pyxel.circ(int(x), int(y), 3, 9)
        for pickup in self.core.pickups:
            self._draw_cherry(int(pickup[0]), int(pickup[1]))
        for enemy in self.core.enemies:
            self._draw_enemy(enemy)
        self._draw_ship(int(self.core.player_x), int(self.core.player_y), 8)

    def _draw_enemy(self, enemy: Enemy) -> None:
        color = [11, 12, 14][(enemy.kind - 1) % 3]
        x, y = int(enemy.x), int(enemy.y)
        pyxel.tri(x, y - 7, x - 10, y + 7, x + 10, y + 7, color)
        pyxel.rect(x - 5, y + 2, 10, 6, 0)
        if enemy.attacking:
            pyxel.circb(x, y, 13, 8)

    def _draw_ship(self, x: int, y: int, color: int) -> None:
        pyxel.tri(x, y - 11, x - 10, y + 10, x + 10, y + 10, color)
        pyxel.rect(x - 4, y - 2, 8, 8, 10)
        pyxel.line(x - 7, y + 11, x - 11, y + 16, 9)
        pyxel.line(x + 7, y + 11, x + 11, y + 16, 9)

    def _draw_cherry(self, x: int, y: int) -> None:
        pyxel.circ(x - 3, y + 2, 4, 8)
        pyxel.circ(x + 3, y + 2, 4, 8)
        pyxel.line(x, y, x + 4, y - 6, 3)
        pyxel.pset(x - 4, y, 7)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 25, 0)
        pyxel.text(5, 5, f"wave {self.core.wave + 1}/9", 7)
        pyxel.text(70, 5, f"score {self.core.score:05d}", 10)
        pyxel.text(164, 5, "heart " + str(self.core.lives), 8)
        pyxel.text(5, 16, f"cherries {self.core.cherries}/10  {self.core.message[:28]}", 14)
        pyxel.rect(0, 222, SCREEN, 18, 0)
        pyxel.text(35, 228, "D-pad move  A shoot  B bomb  Start retry", 7)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 92, 192, 56, 0)
        pyxel.rectb(24, 92, 192, 56, 7)
        self._center(title, 111, 10)
        self._center(subtitle, 130, 7)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    CherryBomb()

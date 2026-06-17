"""Birds With Guns — PyxelPico port.

Adapted from the PICO-8 cart by Yolwoocle and Gouspourd (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=45334
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from birdswithguns_core import BirdsCore, Weapon  # noqa: E402


SCREEN = 240


class BirdsWithGuns:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Birds With Guns", fps=30)
        self.core = BirdsCore()
        self.mode = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3g3", "p", "7", "n", 8)
        pyxel.sound(1).set("c2", "n", "7", "f", 15)
        pyxel.sound(2).set("g3c4e4", "t", "6", "f", 10)

    def reset(self) -> None:
        self.core.reset()
        self.mode = "play"
        self.flash = 0

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
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

        dx = int(ih.btn_right()) - int(ih.btn_left())
        dy = int(ih.btn_down()) - int(ih.btn_up())
        self.core.move_player(dx, dy)

        if ih.btnp_b() or ih.btnp_select():
            self.core.swap_weapon()
            pyxel.play(3, 2)
        if ih.btn_a():
            if self.core.shoot():
                pyxel.play(3, 0)

        prev_hp = self.core.player_hp
        prev_wagon = self.core.wagon
        self.core.tick()
        if self.core.player_hp < prev_hp:
            pyxel.play(3, 1)
            self.flash = 8
        elif self.core.wagon != prev_wagon:
            pyxel.play(3, 2)
        if self.core.won:
            self.mode = "won"
        elif self.core.lost:
            self.mode = "lost"

    def draw(self) -> None:
        pyxel.cls(1 if self.flash == 0 else 2)
        if self.mode == "title":
            self._draw_title()
        else:
            self._draw_train()
            for bullet in self.core.bullets:
                pyxel.circ(int(bullet.x), int(bullet.y), 2, 10)
            for enemy in self.core.enemies:
                self._draw_enemy(enemy)
            self._draw_player()
            self._draw_hud()
            if self.mode == "won":
                self._draw_panel("you cleared the train", "A retry  B title")
            elif self.mode == "lost":
                self._draw_panel("bird down", "A retry  B title")

    def _draw_title(self) -> None:
        self._draw_train()
        for x, y, color in ((68, 116, 12), (104, 92, 9), (148, 128, 10), (180, 82, 14)):
            self._draw_bird(x, y, color, False)
        self._center("birds with guns", 46, 10)
        self._center("yolwoocle + gouspourd", 60, 6)
        self._center("d-pad move  A shoot", 164, 7)
        self._center("B/Select swap weapon", 176, 7)
        if pyxel.frame_count % 30 < 22:
            self._center("press A", 204, 11)

    def _draw_train(self) -> None:
        pyxel.rect(0, 24, SCREEN, SCREEN - 42, 5)
        for y in range(44, 206, 26):
            pyxel.line(0, y, SCREEN, y, 13)
        for x in range(18, SCREEN, 36):
            pyxel.rect(x, 32, 16, 12, 6)
            pyxel.rect(x + 3, 35, 10, 6, 12)
        pyxel.rect(0, 206, SCREEN, 12, 0)
        pyxel.rect(0, 218, SCREEN, 5, 13)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 22, 0)
        pyxel.text(6, 5, f"wagon {self.core.wagon}/{self.core.final_wagon}", 7)
        pyxel.text(88, 5, f"score {self.core.score}", 7)
        weapon = "rev" if self.core.weapon == Weapon.REVOLVER else "shot"
        ammo = self.core.ammo[self.core.weapon]
        pyxel.text(172, 5, f"{weapon} {ammo}", 7 if ammo else 8)
        pyxel.rect(6, 15, 52, 5, 2)
        pyxel.rect(7, 16, int(50 * self.core.player_hp / self.core.max_hp), 3, 8)

    def _draw_player(self) -> None:
        blink = self.core.iframes > 0 and pyxel.frame_count % 6 < 3
        self._draw_bird(int(self.core.player_x), int(self.core.player_y), 12 if not blink else 7, True)

    def _draw_enemy(self, enemy) -> None:
        if enemy.boss:
            pyxel.circ(int(enemy.x), int(enemy.y), 18, 8)
            pyxel.circ(int(enemy.x - 6), int(enemy.y - 4), 3, 0)
            pyxel.circ(int(enemy.x + 6), int(enemy.y - 4), 3, 0)
            pyxel.rect(int(enemy.x - 10), int(enemy.y + 7), 20, 3, 0)
        else:
            self._draw_bird(int(enemy.x), int(enemy.y), 9, False)

    def _draw_bird(self, x: int, y: int, color: int, armed: bool) -> None:
        pyxel.circ(x, y, 7, color)
        pyxel.tri(x + 5, y - 2, x + 14, y, x + 5, y + 3, 10)
        pyxel.pset(x - 2, y - 2, 0)
        pyxel.line(x - 5, y + 7, x - 8, y + 11, 0)
        pyxel.line(x + 2, y + 7, x + 4, y + 11, 0)
        if armed:
            pyxel.rect(x + 8, y + 3, 12, 3, 0)

    def _draw_panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(26, 94, 188, 54, 0)
        pyxel.rectb(26, 94, 188, 54, 7)
        self._center(title, 110, 11)
        self._center(subtitle, 130, 6)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    BirdsWithGuns()

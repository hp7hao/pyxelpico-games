"""UFO Swamp Odyssey — PyxelPico port.

Adapted from the PICO-8 cart by paranoidcactus (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=38153
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from ufoswamp_core import UfoSwampCore  # noqa: E402


SCREEN = 240
TILE = 12


class UfoSwamp:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="UFO Swamp Odyssey", fps=30)
        self.core = UfoSwampCore()
        self.mode = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3g3c4", "t", "6", "n", 10)
        pyxel.sound(1).set("c4e4g4", "p", "5", "f", 8)
        pyxel.sound(2).set("g2c3", "n", "7", "f", 12)
        pyxel.sound(3).set("e4a4c5", "s", "6", "n", 9)

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
        self.core.tick(
            left=ih.btn_left(),
            right=ih.btn_right(),
            jump=ih.btnp_a(),
            shoot=ih.btnp_b(),
            cycle_next=ih.btnp_up(),
            cycle_prev=ih.btnp_down(),
        )
        if self.core.message != old_message:
            if "disabled" in self.core.message:
                pyxel.play(3, 3)
                self.flash = 8
            elif "zapper" in self.core.message or "score" in self.core.message:
                pyxel.play(3, 1)
            elif "stunned" in self.core.message or "grapple" in self.core.message or "portal" in self.core.message:
                pyxel.play(3, 2)

    def draw(self) -> None:
        pyxel.cls(6 if self.flash == 0 else 10)
        if self.mode == "title":
            self._draw_title()
            return

        cam_x = max(0, min(self.core.width * TILE - SCREEN, int(self.core.player.x - SCREEN / 2)))
        cam_y = max(0, min(self.core.height * TILE - SCREEN + 36, int(self.core.player.y - SCREEN / 2)))
        self._draw_background(cam_x, cam_y)
        self._draw_room(cam_x, cam_y)
        self._draw_entities(cam_x, cam_y)
        self._draw_hud()
        if self.core.cleared:
            self._panel("cannon disabled", "A replay  Select title")

    def _draw_title(self) -> None:
        self._draw_background(0, 0)
        pyxel.circ(120, 82, 22, 5)
        pyxel.circb(120, 82, 22, 13)
        pyxel.rect(100, 86, 40, 10, 13)
        pyxel.circ(108, 88, 4, 7)
        pyxel.circ(132, 88, 4, 7)
        self._center("ufo swamp", 124, 11)
        self._center("odyssey", 138, 3)
        self._center("paranoidcactus", 156, 7)
        self._center("A start", 204, 10 if pyxel.frame_count % 30 < 22 else 6)

    def _draw_background(self, cam_x: int, cam_y: int) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        for y in range(24, SCREEN, 34):
            pyxel.line(0, (y - cam_y // 4) % SCREEN, SCREEN, (y - cam_y // 4) % SCREEN, 13)
        for x in range(-40, SCREEN + 40, 40):
            base = (x - cam_x // 5) % (SCREEN + 40) - 20
            pyxel.rect(base, 158, 8, 48, 3)
            pyxel.circ(base + 4, 152, 18, 11)
        pyxel.rect(0, 192, SCREEN, 48, 3)
        pyxel.rect(0, 204, SCREEN, 36, 11)

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
                elif tile in "sEpg":
                    self._draw_pickup(tile, sx + 6, sy + 8)
                elif tile in "12":
                    pyxel.rect(sx + 3, sy + 4, 6, 8, 5)
                    pyxel.circb(sx + 6, sy + 3, 5, 12)
                elif tile == "H":
                    pyxel.circ(sx + 6, sy + 4, 4, 12)
                    pyxel.line(sx + 6, sy + 4, sx + 6, sy + 12, 12)
                elif tile == "C":
                    pyxel.rect(sx + 2, sy + 3, 8, 8, 8)
                    pyxel.circb(sx + 6, sy + 7, 7, 10)

    def _draw_pickup(self, tile: str, x: int, y: int) -> None:
        color = {"s": 10, "E": 8, "p": 12, "g": 7}[tile]
        label = {"s": "+", "E": "E", "p": "P", "g": "G"}[tile]
        bob = 1 if pyxel.frame_count % 24 < 12 else 0
        pyxel.circ(x, y - bob, 4, color)
        pyxel.text(x - 2, y - 3 - bob, label, 0)

    def _draw_entities(self, cam_x: int, cam_y: int) -> None:
        for enemy in self.core.enemies:
            if enemy.alive:
                self._draw_enemy(int(enemy.x - cam_x), int(enemy.y - cam_y), enemy.stunned)
        self._draw_player(int(self.core.player.x - cam_x), int(self.core.player.y - cam_y))
        if self.core.core_charge > 0:
            cx = int(self.core.core_x - cam_x + 6)
            cy = int(self.core.core_y - cam_y + 6)
            pyxel.circb(cx, cy, 8 + self.core.core_charge // 3, 10)

    def _draw_enemy(self, x: int, y: int, stunned: int) -> None:
        pyxel.circ(x + 5, y + 5, 7, 8 if stunned == 0 else 13)
        pyxel.circ(x + 5, y + 5, 3, 7)
        pyxel.pset(x + 5, y + 5, 0)
        if stunned > 0:
            pyxel.text(x - 2, y - 8, "z", 10)

    def _draw_player(self, x: int, y: int) -> None:
        facing = self.core.player.facing
        pyxel.rect(x + 1, y + 2, 8, 8, 13)
        pyxel.circ(x + 5, y + 1, 4, 7)
        pyxel.pset(x + (7 if facing > 0 else 3), y + 1, 0)
        pyxel.line(x + 3, y + 10, x + 1, y + 14, 7)
        pyxel.line(x + 7, y + 10, x + 9, y + 14, 7)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 28, 0)
        pyxel.text(8, 7, f"score {self.core.score}", 7)
        pyxel.text(78, 7, f"gun {self.core.gun if self.core.unlocked_guns else '-'}", 10)
        pyxel.text(156, 7, self.core.message[:19], 6)
        pyxel.text(8, 18, "A jump  B zap  Up/Down gun", 13)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 92, 192, 56, 0)
        pyxel.rectb(24, 92, 192, 56, 7)
        self._center(title, 110, 11)
        self._center(subtitle, 130, 6)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    UfoSwamp()

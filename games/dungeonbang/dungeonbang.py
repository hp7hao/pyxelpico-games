"""DUNGEON! - PyxelPico port.

Adapted from the PICO-8 cart by deklaswas (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=46206
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from dungeonbang_core import DungeonBangCore  # noqa: E402


SCREEN = 240
SHOP_ORDER = ("sword", "bow", "double_jump", "green_cape", "golden_armor")


class DungeonBang:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="DUNGEON!", fps=30)
        self.core = DungeonBangCore()
        self.screen = "title"
        self.shop_index = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3e3", "t", "54", "n", 8)
        pyxel.sound(1).set("c4g3", "p", "65", "n", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 10)
        pyxel.sound(3).set("g3c4e4", "s", "567", "n", 16)

    def update(self) -> None:
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 3)
            return
        if ih.btnp_select():
            self.core.restart()
            return
        if self.core.victory or self.core.game_over:
            if ih.btnp_a() or ih.btnp_start():
                self.core.restart()
            return
        if ih.btnp_up():
            self.shop_index = (self.shop_index - 1) % len(SHOP_ORDER)
        if ih.btnp_down():
            self.shop_index = (self.shop_index + 1) % len(SHOP_ORDER)
        if ih.btnp_b():
            if self.core.buy_powerup(SHOP_ORDER[self.shop_index]):
                pyxel.play(3, 3)
            else:
                self.core.attack()
                pyxel.play(3, 1)
        if ih.btnp_start():
            self.core.enter_portal()
        self.core.tick(move=int(ih.btn_right()) - int(ih.btn_left()), jump=ih.btnp_a())

    def draw(self) -> None:
        pyxel.cls(0)
        if self.screen == "title":
            self._draw_room()
            self._draw_title()
            return
        self._draw_room()
        self._draw_entities()
        self._draw_hud()
        if self.core.victory:
            self._panel("princess rescued", "A delve again")
        elif self.core.game_over:
            self._panel("you died", "A retry")

    def _draw_room(self) -> None:
        colors = {"stone": (1, 5), "fire": (2, 8), "crypt": (13, 5), "garden": (3, 11)}[self.core.zone]
        pyxel.rect(0, 0, SCREEN, SCREEN, colors[0])
        pyxel.rect(0, self.core.ground_y + 8, SCREEN, 60, colors[1])
        pyxel.rect(0, self.core.ground_y, SCREEN, 9, 6)
        for x in range(16, 220, 32):
            pyxel.rect(x, 116 + (x // 32 % 2) * 18, 26, 6, 6)
        pyxel.rect(self.core.portal_x - 10, self.core.ground_y - 34, 20, 34, 12)
        pyxel.circb(self.core.portal_x, self.core.ground_y - 18, 12, 7)

    def _draw_entities(self) -> None:
        for enemy in self.core.enemies:
            x = int(enemy["x"])
            color = {"slime": 11, "bat": 5, "spider": 8}.get(str(enemy["kind"]), 8)
            pyxel.circ(x, self.core.ground_y - 8, 7, color)
            pyxel.text(x - 5, self.core.ground_y - 22, str(enemy["kind"])[0], 0)
        p = self.core.player
        x, y = int(p.x), int(p.y)
        pyxel.rect(x - 5, y - 16, 10, 16, 7)
        pyxel.circ(x, y - 21, 5, 15)
        pyxel.line(x, y - 13, x + p.facing * 12, y - 14, 10 if self.core.powerups["sword"] else 6)
        pyxel.tri(x - 8, y - 10, x, y - 2, x - 3, y - 18, 8)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 36, 0)
        pyxel.text(5, 5, f"depth {self.core.depth}/{self.core.final_depth} hp {self.core.health}/{self.core.max_health} coins {self.core.coins}", 7)
        item = SHOP_ORDER[self.shop_index]
        owned = "owned" if self.core.powerups[item] else "buy/attack"
        pyxel.text(5, 16, f"shop {item} {owned}  {self.core.message[:20]}", 10)
        pyxel.text(5, 228, "Left/Right move  A jump/wall  B buy/attack  Start portal", 6)

    def _draw_title(self) -> None:
        pyxel.rect(26, 52, 188, 72, 0)
        pyxel.rectb(26, 52, 188, 72, 7)
        self._center("DUNGEON!", 68, 7)
        self._center("deklaswas", 86, 6)
        self._center("roguelite platform run", 104, 10)
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
    DungeonBang()

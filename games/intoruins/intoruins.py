"""Into Ruins — PyxelPico port.

Adapted from the PICO-8 cart by Eric Billingsley (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=49928
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from intoruins_core import Enemy, IntoRuinsCore, Tile  # noqa: E402


SCREEN = 240
TILE_W = 10
TILE_H = 8
OX = 18
OY = 54
ENEMY_COLORS = {
    "goblin": 8,
    "bat": 5,
    "mystic": 12,
    "ogre": 4,
    "brute": 4,
    "archer": 10,
    "shade": 13,
}
ITEM_COLORS = {
    "potion": 11,
    "torch": 9,
    "frost": 12,
    "fire": 8,
}


class IntoRuins:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Into Ruins", fps=30)
        self.core = IntoRuinsCore()
        self.mode = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3", "t", "5", "n", 5)
        pyxel.sound(1).set("c3g3", "s", "6", "f", 8)
        pyxel.sound(2).set("g2", "n", "7", "f", 12)
        pyxel.sound(3).set("e4a4c5", "p", "7", "n", 10)

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

        dx = int(ih.btnp_right(8, 6)) - int(ih.btnp_left(8, 6))
        dy = int(ih.btnp_down(8, 6)) - int(ih.btnp_up(8, 6))
        if dx and dy:
            dy = 0
        if dx or dy or ih.btnp_a():
            old_hp = self.core.player_hp
            result = self.core.step(dx, dy)
            if result == "blocked":
                pyxel.play(3, 2)
                self.flash = 4
            elif result == "attack":
                pyxel.play(3, 1)
            elif result == "item":
                pyxel.play(3, 3)
            elif self.core.player_hp < old_hp:
                pyxel.play(3, 2)
            else:
                pyxel.play(3, 0)
        if self.core.won:
            self.mode = "won"
        elif self.core.lost:
            self.mode = "lost"

    def draw(self) -> None:
        pyxel.cls(0 if self.flash == 0 else 2)
        if self.mode == "title":
            self._draw_title()
            return
        self._draw_map()
        self._draw_items()
        self._draw_enemies()
        self._draw_player()
        self._draw_hud()
        if self.mode == "won":
            self._panel("wings of yendor", "A delve again  B title")
        elif self.mode == "lost":
            self._panel("lost in ruins", "A retry  B title")

    def _draw_title(self) -> None:
        self._draw_ruin_backdrop()
        self._center("into ruins", 46, 11)
        self._center("ericb", 60, 6)
        self._draw_wings(120, 102)
        self._center("reach depth 16", 154, 7)
        self._center("d-pad move  A wait", 184, 7)
        self._center("bump enemies, find stairs", 198, 7)
        if pyxel.frame_count % 30 < 22:
            self._center("press A", 216, 10)

    def _draw_map(self) -> None:
        self._draw_ruin_backdrop()
        for y, row in enumerate(self.core.tiles):
            for x, tile in enumerate(row):
                if (x, y) not in self.core.explored:
                    continue
                px, py = self._screen(x, y)
                lit = (x, y) in self.core.visible
                color = self._tile_color(tile, lit)
                if tile is Tile.PIT:
                    pyxel.rect(px, py + 2, TILE_W, TILE_H - 2, 1 if lit else 0)
                    continue
                pyxel.rect(px, py, TILE_W, TILE_H, color)
                if tile is Tile.WALL:
                    pyxel.line(px, py + TILE_H - 1, px + TILE_W - 1, py + TILE_H - 1, 1)
                elif tile is Tile.EXIT:
                    pyxel.text(px + 3, py + 1, ">", 10 if lit else 5)

    def _draw_items(self) -> None:
        for (x, y), kind in self.core.items.items():
            if (x, y) not in self.core.visible:
                continue
            px, py = self._screen(x, y)
            color = ITEM_COLORS.get(kind, 7)
            pyxel.circ(px + 5, py + 4, 3, color)
            if kind == "torch":
                pyxel.line(px + 5, py + 1, px + 5, py + 7, 4)

    def _draw_enemies(self) -> None:
        for enemy in self.core.enemies:
            if (enemy.x, enemy.y) in self.core.visible:
                self._draw_enemy(enemy)

    def _draw_enemy(self, enemy: Enemy) -> None:
        px, py = self._screen(enemy.x, enemy.y)
        color = ENEMY_COLORS.get(enemy.kind, 8)
        if "freeze" in enemy.statuses:
            color = 12
        elif "burn" in enemy.statuses:
            color = 9 if pyxel.frame_count % 8 < 4 else 8
        pyxel.rect(px + 2, py + 1, 6, 7, color)
        pyxel.pset(px + 3, py + 3, 0)
        pyxel.pset(px + 6, py + 3, 0)
        if enemy.ranged:
            pyxel.line(px + 1, py + 7, px + 8, py + 0, 10)

    def _draw_player(self) -> None:
        px, py = self._screen(self.core.player_x, self.core.player_y)
        color = 10 if "freeze" not in self.core.statuses else 12
        if "burn" in self.core.statuses and pyxel.frame_count % 8 < 4:
            color = 9
        pyxel.rect(px + 2, py, 6, 8, color)
        pyxel.rect(px + 3, py + 2, 4, 4, 3)
        pyxel.pset(px + 4, py + 3, 7)
        pyxel.pset(px + 6, py + 3, 7)

    def _draw_hud(self) -> None:
        pyxel.rect(0, 0, SCREEN, 36, 0)
        pyxel.text(8, 6, f"depth {self.core.depth}/{self.core.final_depth}", 7)
        pyxel.text(84, 6, f"hp {self.core.player_hp}/{self.core.max_hp}", 7)
        pyxel.text(152, 6, f"light {self.core.light}", 7)
        pyxel.rect(8, 19, 72, 5, 5)
        pyxel.rect(8, 19, max(0, int(72 * self.core.player_hp / self.core.max_hp)), 5, 8 if self.core.player_hp < 5 else 11)
        x = 88
        for name, turns in self.core.statuses.items():
            pyxel.text(x, 18, f"{name}:{turns}", 12 if name == "freeze" else 9)
            x += 44
        pyxel.text(8, 29, self.core.message[:36], 6)

    def _draw_ruin_backdrop(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        for y in range(38, SCREEN, 16):
            pyxel.line(0, y, SCREEN, y, 13)
        for x in range(0, SCREEN, 20):
            pyxel.line(x, 36, x, SCREEN, 13)

    def _draw_wings(self, x: int, y: int) -> None:
        for i in range(6):
            pyxel.line(x - 6, y, x - 48 + i * 5, y - 24 + i * 8, 7)
            pyxel.line(x + 6, y, x + 48 - i * 5, y - 24 + i * 8, 7)
        pyxel.circ(x, y + 3, 7, 10)
        pyxel.text(x - 2, y, "Y", 0)

    def _tile_color(self, tile: Tile, lit: bool) -> int:
        if tile is Tile.WALL:
            return 5 if lit else 1
        if tile is Tile.EXIT:
            return 3 if lit else 1
        if tile is Tile.PIT:
            return 0
        return 13 if lit else 1

    def _screen(self, x: int, y: int) -> tuple[int, int]:
        return OX + x * TILE_W + (y % 2) * (TILE_W // 2), OY + y * TILE_H

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(24, 92, 192, 58, 0)
        pyxel.rectb(24, 92, 192, 58, 7)
        self._center(title, 110, 11)
        self._center(subtitle, 130, 6)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    IntoRuins()

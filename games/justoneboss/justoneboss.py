"""Just One Boss — PyxelPico port.

Adapted from the PICO-8 cart by bridgs (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=49234
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from justoneboss_core import Direction, GameCore, Phase  # noqa: E402


SCREEN = 240
GRID_COLS = 8
GRID_ROWS = 5
CELL_W = 22
CELL_H = 20
ARENA_X = (SCREEN - GRID_COLS * CELL_W) // 2
ARENA_Y = 72


class JustOneBoss:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Just One Boss", fps=30)
        self.core = GameCore()
        self.mode = "title"
        self.flash = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3e3g3c4", "t", "7", "n", 10)
        pyxel.sound(1).set("g2c3", "s", "6", "f", 12)
        pyxel.sound(2).set("c2", "n", "7", "f", 18)

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

        moved = False
        if ih.btnp_left():
            moved = self.core.step_player(Direction.LEFT)
        elif ih.btnp_right():
            moved = self.core.step_player(Direction.RIGHT)
        elif ih.btnp_up():
            moved = self.core.step_player(Direction.UP)
        elif ih.btnp_down():
            moved = self.core.step_player(Direction.DOWN)

        prev_health = self.core.player_health
        prev_boss = self.core.boss_health
        prev_phase = self.core.phase
        self.core.tick()

        if moved:
            pyxel.play(3, 0)
        if self.core.player_health < prev_health:
            pyxel.play(3, 2)
            self.flash = 8
        elif self.core.boss_health < prev_boss or self.core.phase != prev_phase:
            pyxel.play(3, 1)
            self.flash = 5

        if self.core.won:
            self.mode = "won"
        elif self.core.lost:
            self.mode = "lost"

    def draw(self) -> None:
        pyxel.cls(0)
        if self.mode == "title":
            self._draw_title()
        elif self.mode == "won":
            self._draw_playfield()
            self._draw_center_panel("you did it!", "A/START retry  B menu")
        elif self.mode == "lost":
            self._draw_playfield()
            self._draw_center_panel("try again", "A/START retry  B menu")
        else:
            self._draw_playfield()

    def _draw_title(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        self._draw_boss(120, 63, Phase.ONE, 0)
        self._center_text("just one boss", 104, 10)
        self._center_text("bridgs / pyxelpico", 118, 6)
        self._center_text("d-pad move", 150, 7)
        self._center_text("catch stars, dodge sparks", 160, 7)
        if pyxel.frame_count % 30 < 22:
            self._center_text("press A", 190, 11)

    def _draw_playfield(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1 if self.flash == 0 else 2)
        self._draw_hud()
        self._draw_arena()
        for tile in self.core.tiles:
            self._draw_tile(tile)
        px, py = self._cell_center(self.core.player_col, self.core.player_row)
        self._draw_player(px, py)
        self._draw_boss(120, 47, self.core.phase, self.core.tick_count)

    def _draw_hud(self) -> None:
        pyxel.text(8, 8, f"score {self.core.score:05d}", 7)
        pyxel.text(166, 8, f"phase {self.core.phase.value}/4", 7)
        for i in range(4):
            color = 8 if i < self.core.player_health else 5
            pyxel.circ(12 + i * 10, 24, 4, color)

        max_health = self.core.phase_health(self.core.phase)
        health_w = int(118 * self.core.boss_health / max_health) if max_health else 0
        pyxel.rectb(61, 22, 120, 8, 6)
        pyxel.rect(62, 23, health_w, 6, 11)

    def _draw_arena(self) -> None:
        pyxel.rectb(ARENA_X - 6, ARENA_Y - 6, GRID_COLS * CELL_W + 12, GRID_ROWS * CELL_H + 12, 5)
        for col in range(1, GRID_COLS + 1):
            for row in range(1, GRID_ROWS + 1):
                x = ARENA_X + (col - 1) * CELL_W
                y = ARENA_Y + (row - 1) * CELL_H
                color = 1 if (col + row) % 2 else 13
                pyxel.rect(x, y, CELL_W - 1, CELL_H - 1, color)

    def _draw_tile(self, tile) -> None:
        x, y = self._cell_center(tile.col, tile.row)
        if tile.kind == "magic":
            color = 10 + (pyxel.frame_count // 4) % 5
            pyxel.circ(x, y, 6, color)
            pyxel.pset(x, y - 9, 7)
            pyxel.pset(x, y + 9, 7)
            pyxel.pset(x - 9, y, 7)
            pyxel.pset(x + 9, y, 7)
        else:
            color = 8 if tile.ttl % 12 < 6 else 2
            pyxel.tri(x, y - 8, x - 8, y + 7, x + 8, y + 7, color)

    def _draw_player(self, x: int, y: int) -> None:
        color = 12
        if self.core.invincible_ticks > 0 and pyxel.frame_count % 6 < 3:
            color = 7
        pyxel.rect(x - 5, y - 7, 10, 14, color)
        pyxel.rect(x - 3, y - 10, 6, 4, 12)
        pyxel.pset(x - 2, y - 4, 0)
        pyxel.pset(x + 2, y - 4, 0)

    def _draw_boss(self, x: int, y: int, phase: Phase, frame: int) -> None:
        bob = int(pyxel.sin(frame * 4) * 3)
        body = {Phase.ONE: 11, Phase.TWO: 9, Phase.THREE: 10, Phase.FINAL: 8}[phase]
        pyxel.circ(x, y + bob, 24, body)
        pyxel.circ(x - 9, y + bob - 5, 4, 0)
        pyxel.circ(x + 9, y + bob - 5, 4, 0)
        pyxel.rect(x - 10, y + bob + 8, 20, 3, 0)
        pyxel.line(x - 31, y + bob + 6, x - 46, y + bob + 18, body)
        pyxel.line(x + 31, y + bob + 6, x + 46, y + bob + 18, body)

    def _draw_center_panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(34, 92, 172, 54, 0)
        pyxel.rectb(34, 92, 172, 54, 7)
        self._center_text(title, 108, 11)
        self._center_text(subtitle, 128, 6)

    def _cell_center(self, col: int, row: int) -> tuple[int, int]:
        return (
            ARENA_X + (col - 1) * CELL_W + CELL_W // 2,
            ARENA_Y + (row - 1) * CELL_H + CELL_H // 2,
        )

    @staticmethod
    def _center_text(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    JustOneBoss()

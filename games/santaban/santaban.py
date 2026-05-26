"""Santaban — Sokoban-style holiday puzzle.

Adapted for PyxelPico from PICO-8 cart "Santaban" by skutter-de
(CC BY-NC-SA 4.0).
Source thread: https://www.lexaloffle.com/bbs/?tid=153450
Original cart: https://www.lexaloffle.com/bbs/cposts/sa/santaban-3.p8.png
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from santaban_data import LEVELS, map_tile, tile_has_flag


SCREEN_W = 240
SCREEN_H = 240
FPS = 30

TILE = 16
HUD_H = 24

FLAG_COLLISION = 0
FLAG_GOAL = 1

COL_BG = 1
COL_PANEL = 0
COL_TEXT = 7
COL_WALL = 13
COL_FLOOR = 6
COL_GOAL = 10
COL_BOX = 9
COL_BOX_ON_GOAL = 11
COL_PLAYER = 8


@dataclass
class Snapshot:
    player_x: int
    player_y: int
    boxes: list[tuple[int, int]]
    move_count: int


class Santaban:
    def __init__(self) -> None:
        pyxel.init(SCREEN_W, SCREEN_H, title="Santaban", fps=FPS)
        self._init_audio()

        self.levels = sorted(LEVELS, key=lambda l: l["id"])
        self.max_unlocked = 1

        self.mode = "menu"
        self.menu_index = 0
        self.level_select_index = 0

        self.current_level_idx = 0
        self.player_x = 0
        self.player_y = 0
        self.boxes: list[tuple[int, int]] = []
        self.move_count = 0
        self.history: list[Snapshot] = []
        self.level_complete = False
        self.game_complete = False

        self._load_level(0)
        pyxel.run(self.update, self.draw)

    def _init_audio(self) -> None:
        pyxel.sounds[0].set("g2f2", "p", "75", "n", 12)   # bump
        pyxel.sounds[1].set("c3e3g3", "t", "776", "f", 16)  # push
        pyxel.sounds[2].set("c3e3g3c4", "s", "7777", "f", 18)  # win

    @property
    def level(self) -> dict:
        return self.levels[self.current_level_idx]

    def _load_level(self, level_idx: int) -> None:
        self.current_level_idx = max(0, min(level_idx, len(self.levels) - 1))
        lvl = self.level
        self.player_x = lvl["player_start_x"]
        self.player_y = lvl["player_start_y"]
        self.boxes = [(b["x"], b["y"]) for b in lvl["boxes_start"]]
        self.move_count = 0
        self.history = []
        self.level_complete = False

    def _tile_at(self, gx: int, gy: int) -> int:
        lvl = self.level
        return map_tile(lvl["map_x"] + gx, lvl["map_y"] + gy)

    def _tile_flag(self, gx: int, gy: int, flag_idx: int) -> bool:
        return tile_has_flag(self._tile_at(gx, gy), flag_idx)

    def _has_collision(self, gx: int, gy: int) -> bool:
        return self._tile_flag(gx, gy, FLAG_COLLISION)

    def _has_goal(self, gx: int, gy: int) -> bool:
        return self._tile_flag(gx, gy, FLAG_GOAL)

    def _box_index(self, gx: int, gy: int) -> int:
        for i, (bx, by) in enumerate(self.boxes):
            if bx == gx and by == gy:
                return i
        return -1

    def _is_navigable(self, gx: int, gy: int) -> bool:
        if self._has_collision(gx, gy):
            return False
        return self._box_index(gx, gy) == -1

    def _check_complete(self) -> bool:
        return all(self._has_goal(bx, by) for bx, by in self.boxes)

    def _push_snapshot(self) -> None:
        self.history.append(
            Snapshot(
                player_x=self.player_x,
                player_y=self.player_y,
                boxes=list(self.boxes),
                move_count=self.move_count,
            )
        )

    def _undo(self) -> None:
        if not self.history:
            return
        snap = self.history.pop()
        self.player_x = snap.player_x
        self.player_y = snap.player_y
        self.boxes = list(snap.boxes)
        self.move_count = snap.move_count

    def _next_level(self) -> None:
        if self.current_level_idx >= len(self.levels) - 1:
            self.game_complete = True
            self.mode = "credits"
            return
        self.current_level_idx += 1
        self.max_unlocked = max(self.max_unlocked, self.current_level_idx + 1)
        self._load_level(self.current_level_idx)

    def _move_player(self, dx: int, dy: int) -> None:
        if self.level_complete:
            return

        nx = self.player_x + dx
        ny = self.player_y + dy

        if self._has_collision(nx, ny):
            pyxel.play(3, 0)
            return

        box_i = self._box_index(nx, ny)
        if box_i >= 0:
            bx, by = self.boxes[box_i]
            nnx = bx + dx
            nny = by + dy
            if not self._is_navigable(nnx, nny):
                pyxel.play(3, 0)
                return
            self._push_snapshot()
            self.boxes[box_i] = (nnx, nny)
            self.player_x = nx
            self.player_y = ny
            self.move_count += 1
            pyxel.play(3, 1)
        else:
            self._push_snapshot()
            self.player_x = nx
            self.player_y = ny
            self.move_count += 1

        self.level_complete = self._check_complete()
        if self.level_complete:
            pyxel.play(3, 2)

    def update(self) -> None:
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.mode == "menu":
            self._update_menu()
        elif self.mode == "level_select":
            self._update_level_select()
        elif self.mode == "game":
            self._update_game()
        elif self.mode == "credits":
            self._update_credits()

    def _update_menu(self) -> None:
        items = ["continue", "new game", "level select", "credits"]
        if ih.btnp_up(8, 4):
            self.menu_index = max(0, self.menu_index - 1)
        elif ih.btnp_down(8, 4):
            self.menu_index = min(len(items) - 1, self.menu_index + 1)
        elif ih.btnp_a() or ih.btnp_start():
            sel = items[self.menu_index]
            if sel == "continue":
                self.mode = "game"
            elif sel == "new game":
                self.max_unlocked = 1
                self._load_level(0)
                self.mode = "game"
            elif sel == "level select":
                self.level_select_index = min(self.current_level_idx, self.max_unlocked - 1)
                self.mode = "level_select"
            else:
                self.mode = "credits"

    def _update_level_select(self) -> None:
        if ih.btnp_up(8, 4):
            self.level_select_index = max(0, self.level_select_index - 1)
        elif ih.btnp_down(8, 4):
            self.level_select_index = min(self.max_unlocked - 1, self.level_select_index + 1)
        elif ih.btnp_b() or ih.btnp_select():
            self.mode = "menu"
        elif ih.btnp_a() or ih.btnp_start():
            self._load_level(self.level_select_index)
            self.mode = "game"

    def _update_game(self) -> None:
        if ih.btnp_start():
            self._load_level(self.current_level_idx)
            return

        if ih.btnp_select():
            self.mode = "menu"
            return

        if ih.btnp_b():
            self._undo()
            return

        if self.level_complete:
            if ih.btnp_a():
                self._next_level()
            return

        if ih.btnp_up(8, 4):
            self._move_player(0, -1)
        elif ih.btnp_down(8, 4):
            self._move_player(0, 1)
        elif ih.btnp_left(8, 4):
            self._move_player(-1, 0)
        elif ih.btnp_right(8, 4):
            self._move_player(1, 0)

    def _update_credits(self) -> None:
        if ih.btnp_a() or ih.btnp_start() or ih.btnp_b():
            self.mode = "menu"

    def draw(self) -> None:
        pyxel.cls(COL_BG)
        if self.mode == "menu":
            self._draw_menu()
        elif self.mode == "level_select":
            self._draw_level_select()
        elif self.mode == "game":
            self._draw_game()
        elif self.mode == "credits":
            self._draw_credits()

    def _draw_panel_title(self, title: str) -> None:
        pyxel.rect(0, 0, SCREEN_W, HUD_H, COL_PANEL)
        pyxel.text(8, 8, title, COL_TEXT)

    def _draw_menu(self) -> None:
        self._draw_panel_title("SANTABAN")
        pyxel.text(8, 16, "A/START select", 6)
        items = ["continue", "new game", "level select", "credits"]
        y = 72
        for i, item in enumerate(items):
            c = 10 if i == self.menu_index else 7
            pyxel.text(80, y, item, c)
            y += 14

    def _draw_level_select(self) -> None:
        self._draw_panel_title("LEVEL SELECT")
        pyxel.text(8, 16, "A choose  B/SEL back", 6)

        start = max(0, self.level_select_index - 6)
        end = min(self.max_unlocked, start + 13)
        y = 36
        for i in range(start, end):
            level_num = i + 1
            c = 10 if i == self.level_select_index else 7
            pyxel.text(96, y, f"level {level_num}", c)
            y += 14

    def _draw_game(self) -> None:
        lvl = self.level
        self._draw_panel_title(f"LEVEL {lvl['id']}  MOVES {self.move_count}")
        pyxel.text(8, 16, "B undo  STA restart  SEL menu", 6)

        map_w = lvl["map_size_x"]
        map_h = lvl["map_size_y"]
        ox = (SCREEN_W - map_w * TILE) // 2
        oy = HUD_H + (SCREEN_H - HUD_H - map_h * TILE) // 2

        for gy in range(map_h):
            for gx in range(map_w):
                x = ox + gx * TILE
                y = oy + gy * TILE
                if self._has_collision(gx, gy):
                    pyxel.rect(x, y, TILE, TILE, COL_WALL)
                    pyxel.rectb(x, y, TILE, TILE, 4)
                else:
                    pyxel.rect(x, y, TILE, TILE, COL_FLOOR)
                    pyxel.rectb(x, y, TILE, TILE, 5)

                if self._has_goal(gx, gy):
                    pyxel.circb(x + TILE // 2, y + TILE // 2, 4, COL_GOAL)

        for bx, by in self.boxes:
            x = ox + bx * TILE
            y = oy + by * TILE
            color = COL_BOX_ON_GOAL if self._has_goal(bx, by) else COL_BOX
            pyxel.rect(x + 2, y + 2, TILE - 4, TILE - 4, color)
            pyxel.rectb(x + 2, y + 2, TILE - 4, TILE - 4, 1)

        px = ox + self.player_x * TILE + TILE // 2
        py = oy + self.player_y * TILE + TILE // 2
        pyxel.circ(px, py, 5, COL_PLAYER)
        pyxel.pset(px, py, 7)

        if self.level_complete:
            pyxel.rect(36, 100, 168, 36, 0)
            pyxel.rectb(36, 100, 168, 36, 7)
            pyxel.text(82, 112, "LEVEL COMPLETE!", 10)
            pyxel.text(74, 122, "A -> NEXT LEVEL", 7)

    def _draw_credits(self) -> None:
        self._draw_panel_title("CREDITS")
        pyxel.text(10, 40, "game + art: skutter-de", 7)
        pyxel.text(10, 54, "snow idea: thattomhall", 7)
        pyxel.text(10, 68, "logo: doriencey", 7)
        pyxel.text(10, 82, "special thanks: brytergames", 7)
        pyxel.text(10, 104, "based on sokoban gba", 6)
        pyxel.text(10, 118, "author: juergen werner", 6)
        pyxel.text(10, 132, "levels: david w. skinner", 6)

        if self.game_complete:
            pyxel.text(10, 162, "all levels complete!", 10)

        pyxel.text(10, 192, "A/START/B -> menu", 7)


if __name__ == "__main__":
    Santaban()

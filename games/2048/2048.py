"""2048 — sliding tile puzzle.

Adapted for PyxelPico from PICO-8 cart by straversi (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=153397
"""

from __future__ import annotations

import os
import random
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402


SCREEN_W = 240
SCREEN_H = 240
GRID = 4
CELL = 40
GAP = 6
BOARD_SIZE = GRID * CELL + (GRID + 1) * GAP
BOARD_X = (SCREEN_W - BOARD_SIZE) // 2
BOARD_Y = 40


TILE_COLORS = {
    0: 5,
    2: 7,
    4: 6,
    8: 10,
    16: 9,
    32: 8,
    64: 11,
    128: 3,
    256: 2,
    512: 14,
    1024: 15,
    2048: 4,
}


class Game2048:
    def __init__(self) -> None:
        pyxel.init(SCREEN_W, SCREEN_H, title="2048", fps=30)
        self.best_score = 0
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self) -> None:
        self.board = [[0 for _ in range(GRID)] for _ in range(GRID)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.spawn_tile()
        self.spawn_tile()

    def spawn_tile(self) -> bool:
        empties = [
            (x, y)
            for y in range(GRID)
            for x in range(GRID)
            if self.board[y][x] == 0
        ]
        if not empties:
            return False
        x, y = random.choice(empties)
        self.board[y][x] = 4 if random.random() < 0.1 else 2
        return True

    def merge_line(self, line: list[int]) -> tuple[list[int], int, bool]:
        compact = [v for v in line if v != 0]
        merged: list[int] = []
        gained = 0
        i = 0
        while i < len(compact):
            if i + 1 < len(compact) and compact[i] == compact[i + 1]:
                value = compact[i] * 2
                merged.append(value)
                gained += value
                i += 2
            else:
                merged.append(compact[i])
                i += 1
        merged.extend([0] * (GRID - len(merged)))
        changed = merged != line
        return merged, gained, changed

    def move_left(self) -> bool:
        moved = False
        gained_total = 0
        new_board = []
        for row in self.board:
            merged, gained, changed = self.merge_line(row)
            new_board.append(merged)
            gained_total += gained
            moved = moved or changed
        if moved:
            self.board = new_board
            self.score += gained_total
            self.best_score = max(self.best_score, self.score)
        return moved

    def move_right(self) -> bool:
        self.board = [list(reversed(row)) for row in self.board]
        moved = self.move_left()
        self.board = [list(reversed(row)) for row in self.board]
        return moved

    def move_up(self) -> bool:
        self.transpose()
        moved = self.move_left()
        self.transpose()
        return moved

    def move_down(self) -> bool:
        self.transpose()
        moved = self.move_right()
        self.transpose()
        return moved

    def transpose(self) -> None:
        self.board = [list(row) for row in zip(*self.board)]

    def can_move(self) -> bool:
        for y in range(GRID):
            for x in range(GRID):
                value = self.board[y][x]
                if value == 0:
                    return True
                if x + 1 < GRID and self.board[y][x + 1] == value:
                    return True
                if y + 1 < GRID and self.board[y + 1][x] == value:
                    return True
        return False

    def update(self) -> None:
        if ih.btnp_start() or ih.btnp_a() or ih.btnp_b():
            if self.game_over:
                self.reset()
                return

        if pyxel.btnp(pyxel.KEY_R):
            self.reset()
            return

        if self.game_over:
            return

        moved = False
        if ih.btnp_left():
            moved = self.move_left()
        elif ih.btnp_right():
            moved = self.move_right()
        elif ih.btnp_up():
            moved = self.move_up()
        elif ih.btnp_down():
            moved = self.move_down()

        if moved:
            self.spawn_tile()
            self.won = any(value >= 2048 for row in self.board for value in row)
            if not self.can_move():
                self.game_over = True
        elif not self.can_move():
            self.game_over = True

    def draw_tile(self, gx: int, gy: int, value: int) -> None:
        x = BOARD_X + GAP + gx * (CELL + GAP)
        y = BOARD_Y + GAP + gy * (CELL + GAP)
        color = TILE_COLORS.get(value, 1)
        pyxel.rect(x, y, CELL, CELL, color)
        pyxel.rectb(x, y, CELL, CELL, 1)
        if value:
            text = str(value)
            tx = x + CELL // 2 - (len(text) * 4) // 2
            ty = y + CELL // 2 - 3
            txt_color = 0 if value <= 4 else 7
            pyxel.text(tx, ty, text, txt_color)

    def draw(self) -> None:
        pyxel.cls(0)
        pyxel.text(8, 8, "2048", 7)
        pyxel.text(62, 8, f"SCORE {self.score}", 10)
        pyxel.text(150, 8, f"BEST {self.best_score}", 11)

        pyxel.rect(BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE, 13)
        for y in range(GRID):
            for x in range(GRID):
                self.draw_tile(x, y, self.board[y][x])

        if self.won and not self.game_over:
            pyxel.text(76, 214, "2048 reached! keep going", 3)
        else:
            pyxel.text(78, 214, "D-PAD move tiles", 6)

        pyxel.text(58, 224, "A/B/START restart  R reset", 12)

        if self.game_over:
            pyxel.rect(40, 98, 160, 44, 1)
            pyxel.rectb(40, 98, 160, 44, 7)
            pyxel.text(94, 111, "GAME OVER", 8)
            pyxel.text(56, 124, "A/B/START to restart", 7)


if __name__ == "__main__":
    Game2048()

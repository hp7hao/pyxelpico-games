"""LightWalk - Netwalk-style pipe puzzle.

Adapted for Pico8Go (240x240, 8-button gamepad).
Original game: LightWalk by juliusspeak.
Source: https://github.com/juliusspeak/lightwalk
License: CC BY-NC-SA 4.0 (per PICO-8 BBS metadata)
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass, field
from pathlib import Path

import pyxel

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "lib"))
import input_helper as ih  # noqa: E402


SCREEN_W = 240
SCREEN_H = 240
GRID_SIZE = 8
CELL = 16
BOARD_PX = GRID_SIZE * CELL
BOARD_X = (SCREEN_W - BOARD_PX) // 2
BOARD_Y = 32

DIRS = {
    "l": (-1, 0),
    "r": (1, 0),
    "t": (0, -1),
    "b": (0, 1),
}
OPPOSITE = {"l": "r", "r": "l", "t": "b", "b": "t"}


@dataclass
class Cell:
    x: int
    y: int
    kind: int = 0  # 0 empty, 1 source, 2 wire, 3 lamp
    conns: set[str] = field(default_factory=set)
    powered: bool = False

    def rotate(self) -> None:
        rotated = set()
        for d in self.conns:
            if d == "l":
                rotated.add("t")
            elif d == "t":
                rotated.add("r")
            elif d == "r":
                rotated.add("b")
            elif d == "b":
                rotated.add("l")
        self.conns = rotated


class Grid:
    def __init__(self, sx: int, sy: int):
        self.sx = sx
        self.sy = sy
        self.cells = [[Cell(x + 1, y + 1) for x in range(sx)] for y in range(sy)]
        self.lamps: list[Cell] = []
        self.source: Cell | None = None

    def cell(self, x: int, y: int) -> Cell | None:
        if x < 1 or y < 1 or x > self.sx or y > self.sy:
            return None
        return self.cells[y - 1][x - 1]

    def reset(self) -> None:
        self.lamps.clear()
        for row in self.cells:
            for c in row:
                c.kind = 0
                c.conns.clear()
                c.powered = False

        sx = random.randint(1, self.sx)
        sy = random.randint(1, self.sy)
        start = self.cell(sx, sy)
        assert start is not None
        start.kind = 1
        start.powered = True
        self.source = start

        self._set_line(start)
        while self._has_empty():
            for y in range(1, self.sy + 1):
                for x in range(1, self.sx + 1):
                    c = self.cell(x, y)
                    assert c is not None
                    n = self._neighbors_by_kind(c, 2)
                    if c.kind == 0 and n:
                        c.kind = 2
                        self._bond(c, n[0])
                        self._set_line(c)

        self._shuffle()
        self.supply()

    def _neighbors_by_kind(self, c: Cell, kind: int) -> list[Cell]:
        out: list[Cell] = []
        for dx, dy in DIRS.values():
            n = self.cell(c.x + dx, c.y + dy)
            if n is not None and n.kind == kind:
                out.append(n)
        return out

    def _bond(self, a: Cell, b: Cell) -> None:
        if a.x > b.x:
            a.conns.add("l")
            b.conns.add("r")
        elif a.x < b.x:
            a.conns.add("r")
            b.conns.add("l")
        elif a.y > b.y:
            a.conns.add("t")
            b.conns.add("b")
        elif a.y < b.y:
            a.conns.add("b")
            b.conns.add("t")

    def _set_line(self, start: Cell) -> None:
        passed = [start]
        options = self._neighbors_by_kind(start, 0)
        if not options:
            return
        nxt = random.choice(options)

        while nxt is not None:
            nxt.kind = 2
            self._bond(nxt, passed[-1])
            passed.append(nxt)

            options = self._neighbors_by_kind(nxt, 0)
            options = [o for o in options if o not in passed]
            nxt = random.choice(options) if options else None

        end = passed[-1]
        end.kind = 3
        if end not in self.lamps:
            self.lamps.append(end)

    def _shuffle(self) -> None:
        for row in self.cells:
            for c in row:
                for _ in range(random.randint(0, 3)):
                    c.rotate()

    def _has_empty(self) -> bool:
        return any(c.kind == 0 for row in self.cells for c in row)

    def _connected(self, a: Cell, b: Cell) -> bool:
        if b.x == a.x - 1:
            return "l" in a.conns and "r" in b.conns
        if b.x == a.x + 1:
            return "r" in a.conns and "l" in b.conns
        if b.y == a.y - 1:
            return "t" in a.conns and "b" in b.conns
        if b.y == a.y + 1:
            return "b" in a.conns and "t" in b.conns
        return False

    def supply(self) -> None:
        if self.source is None:
            return
        for row in self.cells:
            for c in row:
                c.powered = c is self.source

        queue = [self.source]
        seen = {(self.source.x, self.source.y)}
        while queue:
            cur = queue.pop(0)
            neighbors = self._neighbors_by_kind(cur, 2) + self._neighbors_by_kind(cur, 3)
            for n in neighbors:
                key = (n.x, n.y)
                if key in seen:
                    continue
                if self._connected(cur, n):
                    n.powered = True
                    seen.add(key)
                    queue.append(n)

    def is_win(self) -> bool:
        return bool(self.lamps) and all(l.powered for l in self.lamps)


class Game:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="LightWalk", fps=30)
        self.grid = Grid(GRID_SIZE, GRID_SIZE)
        self.cx = 1
        self.cy = 1
        self.grid.reset()
        pyxel.run(self.update, self.draw)

    def restart(self) -> None:
        self.cx = 1
        self.cy = 1
        self.grid.reset()

    def update(self) -> None:
        if ih.btnp_left(8, 4):
            self.cx = max(1, self.cx - 1)
        elif ih.btnp_right(8, 4):
            self.cx = min(GRID_SIZE, self.cx + 1)
        elif ih.btnp_up(8, 4):
            self.cy = max(1, self.cy - 1)
        elif ih.btnp_down(8, 4):
            self.cy = min(GRID_SIZE, self.cy + 1)

        if ih.btnp_a():
            c = self.grid.cell(self.cx, self.cy)
            if c is not None:
                c.rotate()
                self.grid.supply()

        if ih.btnp_b() or ih.btnp_start():
            self.restart()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def _draw_cell(self, c: Cell, px: int, py: int) -> None:
        base = 1
        pipe = 10 if c.powered else 5
        center = 8

        pyxel.rect(px, py, CELL, CELL, base)
        pyxel.rectb(px, py, CELL, CELL, 0)

        if c.conns:
            pyxel.circ(px + center, py + center, 3, pipe)
            if "l" in c.conns:
                pyxel.line(px + center, py + center, px + 1, py + center, pipe)
            if "r" in c.conns:
                pyxel.line(px + center, py + center, px + CELL - 2, py + center, pipe)
            if "t" in c.conns:
                pyxel.line(px + center, py + center, px + center, py + 1, pipe)
            if "b" in c.conns:
                pyxel.line(px + center, py + center, px + center, py + CELL - 2, pipe)

        if c.kind == 1:
            pyxel.circ(px + center, py + center, 5, 9)
            pyxel.circ(px + center, py + center, 2, 7)
        elif c.kind == 3:
            col = 10 if c.powered else 2
            pyxel.circb(px + center, py + center, 5, col)
            pyxel.pset(px + center, py + center, col)

    def draw(self) -> None:
        pyxel.cls(0)
        pyxel.text(8, 8, "LIGHTWALK", 7)
        pyxel.text(8, 16, "D-PAD MOVE  [A] ROTATE  [B]/[STA] RESTART", 6)

        for y in range(1, GRID_SIZE + 1):
            for x in range(1, GRID_SIZE + 1):
                c = self.grid.cell(x, y)
                if c is None:
                    continue
                px = BOARD_X + (x - 1) * CELL
                py = BOARD_Y + (y - 1) * CELL
                self._draw_cell(c, px, py)

        cur_x = BOARD_X + (self.cx - 1) * CELL
        cur_y = BOARD_Y + (self.cy - 1) * CELL
        pyxel.rectb(cur_x, cur_y, CELL, CELL, 7)

        if self.grid.is_win():
            w, h = 124, 42
            ox, oy = (SCREEN_W - w) // 2, 184
            pyxel.rect(ox, oy, w, h, 7)
            pyxel.rectb(ox, oy, w, h, 0)
            pyxel.text(ox + 38, oy + 10, "YOU WIN!", 8)
            pyxel.text(ox + 18, oy + 24, "PRESS [B] OR [STA]", 1)


if __name__ == "__main__":
    Game()

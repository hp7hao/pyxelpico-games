"""Pure grid puzzle rules for the Woodworm PyxelPico port."""

from __future__ import annotations

import copy
import random


DIRS = {
    "left": (-1, 0),
    "right": (1, 0),
    "up": (0, -1),
    "down": (0, 1),
}
OPPOSITE = {"left": "right", "right": "left", "up": "down", "down": "up"}


class WoodwormCore:
    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.level = 1
        self.tiles: list[list[str]] = []
        self.worm: list[tuple[int, int]] = []
        self.last_dir = "right"
        self.history: list[tuple] = []
        self.moves = 0
        self.wood_eaten = 0
        self.score = 0
        self.cleared = False
        self.message = "eat the wood"
        self.set_test_level([
            "############",
            "#......G...#",
            "#...@ww...#",
            "#...b.....#",
            "############",
        ])

    def reset(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

    def set_test_level(self, rows: list[str]) -> None:
        self.tiles = []
        self.worm = []
        for y, row in enumerate(rows):
            out = []
            for x, char in enumerate(row):
                if char == "@":
                    self.worm = [(x, y), (x - 1, y), (x - 2, y)]
                    out.append(".")
                else:
                    out.append(char)
            self.tiles.append(out)
        if not self.worm:
            self.worm = [(2, 2), (1, 2), (1, 1)]
        self.last_dir = "right"
        self.history = []
        self.moves = 0
        self.wood_eaten = 0
        self.score = 0
        self.cleared = False
        self.message = "eat the wood"

    @property
    def width(self) -> int:
        return len(self.tiles[0]) if self.tiles else 0

    @property
    def height(self) -> int:
        return len(self.tiles)

    def snapshot(self) -> tuple:
        return (
            tuple(tuple(row) for row in self.tiles),
            tuple(self.worm),
            self.last_dir,
            self.moves,
            self.wood_eaten,
            self.score,
            self.cleared,
        )

    def _restore(self, state: tuple) -> None:
        tiles, worm, self.last_dir, self.moves, self.wood_eaten, self.score, self.cleared = state
        self.tiles = [list(row) for row in tiles]
        self.worm = list(worm)

    def move(self, direction: str) -> bool:
        if self.cleared or direction not in DIRS:
            return False
        if OPPOSITE[direction] == self.last_dir:
            self.message = "no reverse"
            return False
        dx, dy = DIRS[direction]
        hx, hy = self.worm[0]
        nx, ny = hx + dx, hy + dy
        if not self._can_enter(nx, ny):
            self.message = "bonk"
            return False
        self.history.append(self.snapshot())
        self.worm.insert(0, (nx, ny))
        self.last_dir = direction
        self.moves += 1
        tile = self.tile_at(nx, ny)
        if tile == "w":
            self._set_tile(nx, ny, ".")
            self.wood_eaten += 1
            self.score += 10
            self.message = "munch"
        elif tile == "G":
            self.cleared = True
            self.score += max(10, 100 - self.moves)
            self.message = "cleared"
        else:
            self.message = "wiggle"
        while len(self.worm) > 3:
            self.worm.pop()
        self.apply_gravity()
        return True

    def undo(self) -> bool:
        if not self.history:
            self.message = "nothing to undo"
            return False
        self._restore(self.history.pop())
        self.message = "undo"
        return True

    def apply_gravity(self) -> None:
        moved = True
        while moved:
            moved = False
            blocks = [
                (x, y, self.tile_at(x, y))
                for y in range(self.height - 2, -1, -1)
                for x in range(self.width)
                if self.tile_at(x, y) == "b" and self.tile_at(x, y + 1) == "."
            ]
            for x, y, tile in blocks:
                self._set_tile(x, y, ".")
                self._set_tile(x, y + 1, tile)
                moved = True
            if self._worm_can_fall():
                self.worm = [(x, y + 1) for x, y in self.worm]
                moved = True

    def tile_at(self, x: int, y: int) -> str:
        if x < 0 or y < 0 or y >= self.height or x >= self.width:
            return "#"
        return self.tiles[y][x]

    def _set_tile(self, x: int, y: int, value: str) -> None:
        self.tiles[y][x] = value

    def _can_enter(self, x: int, y: int) -> bool:
        tile = self.tile_at(x, y)
        if tile == "#" or tile == "b":
            return False
        tail = self.worm[-1]
        return (x, y) not in self.worm[:-1] or (x, y) == tail

    def _worm_can_fall(self) -> bool:
        occupied = set(self.worm)
        for x, y in self.worm:
            below = (x, y + 1)
            if below in occupied:
                continue
            if self.tile_at(x, y + 1) != ".":
                return False
        return True

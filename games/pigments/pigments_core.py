"""Pure tile-painting pursuit rules for the pigments PyxelPico port."""

from __future__ import annotations

import random


class PigmentsCore:
    width = 9
    height = 9

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.spawn = (4, 4)
        self.player = self.spawn
        self.pigment = 6
        self.max_pigment = 12
        self.score = 0
        self.moves = 0
        self.game_over = False
        self.level_clear = False
        self.message = "paint all tiles"
        self.grass: set[tuple[int, int]] = {(1, 1), (7, 1), (1, 7), (7, 7)}
        self.water: set[tuple[int, int]] = {(3, 3), (5, 5)}
        self.triggers: set[tuple[int, int]] = {(4, 1), (4, 7)}
        self.walls: set[tuple[int, int]] = {(0, y) for y in range(self.height)} | {
            (self.width - 1, y) for y in range(self.height)
        } | {(x, 0) for x in range(self.width)} | {(x, self.height - 1) for x in range(self.width)}
        self.safe_tiles: set[tuple[int, int]] = {
            (x, y)
            for x in range(self.width)
            for y in range(self.height)
            if (x, y) not in self.walls
        }
        self.painted: set[tuple[int, int]] = {self.spawn}
        self.droplets: set[tuple[int, int]] = {(2, 2), (6, 2), (2, 6), (6, 6)}
        self.discs: list[tuple[int, int]] = [(2, 4), (6, 4)]

    def move(self, dx: int, dy: int) -> bool:
        if self.game_over or self.level_clear:
            return False
        if abs(dx) + abs(dy) != 1:
            return False
        target = (self.player[0] + dx, self.player[1] + dy)
        if target in self.walls or target not in self.safe_tiles:
            self.message = "wall blocks"
            return False
        self.player = target
        self.moves += 1
        self._paint_tile(target)
        self._collect_droplet(target)
        if target in self.water:
            self._spend_pigment(1, "water hide")
        if target in self.triggers:
            self.dash_discs()
            self.message = "trigger dash"
        else:
            self.tick_discs()
        self._check_clear()
        return True

    def wait(self) -> None:
        if self.game_over or self.level_clear:
            return
        self.moves += 1
        if self.player in self.water:
            self._spend_pigment(1, "water hide")
        self.tick_discs()
        self._check_clear()

    def tick_discs(self) -> None:
        self.discs = [self._step_disc(pos, steps=1) for pos in self.discs]
        self._check_disc_hit()

    def dash_discs(self) -> None:
        self.discs = [self._step_disc(pos, steps=3) for pos in self.discs]
        self._check_disc_hit()

    def restart(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

    def _paint_tile(self, tile: tuple[int, int]) -> None:
        if tile in self.painted:
            return
        if tile in self.water:
            self.painted.add(tile)
            self.score += 1
            return
        if self.pigment <= 0:
            self.message = "need pigment"
            return
        self.painted.add(tile)
        self.pigment -= 1
        self.score += 1
        self.message = "paint"

    def _collect_droplet(self, tile: tuple[int, int]) -> None:
        if tile not in self.droplets:
            return
        self.droplets.remove(tile)
        self.pigment = min(self.max_pigment, self.pigment + 5)
        self.score += 5
        self.message = "droplet"
        self._spawn_droplet()

    def _spawn_droplet(self) -> None:
        choices = sorted(
            self.safe_tiles
            - self.walls
            - self.grass
            - self.water
            - set(self.discs)
            - {self.player}
            - self.droplets
        )
        if choices:
            self.droplets.add(self.rng.choice(choices))

    def _spend_pigment(self, amount: int, message: str) -> None:
        if self.pigment >= amount:
            self.pigment -= amount
            self.message = message
        else:
            self.message = "out of pigment"

    def _step_disc(self, start: tuple[int, int], *, steps: int) -> tuple[int, int]:
        x = max(1, min(self.width - 2, start[0]))
        y = max(1, min(self.height - 2, start[1]))
        for _ in range(steps):
            if self.player in self.water and self.pigment >= 0:
                self.message = "hidden in water"
                break
            dx = self._sign(self.player[0] - x)
            dy = self._sign(self.player[1] - y)
            options = []
            if abs(self.player[0] - x) >= abs(self.player[1] - y) and dx:
                options.append((x + dx, y))
            if dy:
                options.append((x, y + dy))
            if dx:
                options.append((x + dx, y))
            moved = False
            for target in options:
                if target not in self.walls and target not in self.grass:
                    x, y = target
                    moved = True
                    break
            if not moved:
                break
        return x, y

    def _check_disc_hit(self) -> None:
        if self.player not in self.discs:
            return
        if self.player in self.water and self.pigment >= 0:
            self.message = "disc missed water"
            return
        self.game_over = True
        self.message = "sliced"

    def _check_clear(self) -> None:
        if self.safe_tiles <= self.painted:
            self.level_clear = True
            self.message = "fully painted"

    @staticmethod
    def _sign(value: int) -> int:
        return (value > 0) - (value < 0)

    @property
    def painted_ratio(self) -> float:
        return len(self.painted & self.safe_tiles) / max(1, len(self.safe_tiles))

    def tile_kind(self, tile: tuple[int, int]) -> str:
        if tile in self.walls:
            return "wall"
        if tile in self.water:
            return "water"
        if tile in self.grass:
            return "grass"
        if tile in self.triggers:
            return "trigger"
        return "floor"

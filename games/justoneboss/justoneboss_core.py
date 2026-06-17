"""Pure gameplay core for the Just One Boss PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import random


class Direction(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


class Phase(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FINAL = 4


@dataclass
class Tile:
    col: int
    row: int
    ttl: int
    kind: str
    expired: bool = False

    def tick(self) -> None:
        if self.expired:
            return
        self.ttl -= 1
        if self.ttl <= 0:
            self.expired = True


class GameCore:
    min_col = 1
    max_col = 8
    min_row = 1
    max_row = 5

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.player_col = 4
        self.player_row = 3
        self.player_health = 4
        self.invincible_ticks = 0
        self.phase = Phase.ONE
        self.boss_health = self.phase_health(self.phase)
        self.score = 0
        self.combo = 0
        self.tick_count = 0
        self.won = False
        self.lost = False
        self.tiles: list[Tile] = []

    def reset(self) -> None:
        seed = self.rng.randint(0, 999_999)
        self.__init__(seed=seed)

    @staticmethod
    def phase_health(phase: Phase) -> int:
        return {
            Phase.ONE: 8,
            Phase.TWO: 10,
            Phase.THREE: 12,
            Phase.FINAL: 16,
        }[phase]

    def step_player(self, direction: Direction) -> bool:
        if self.won or self.lost:
            return False
        dx, dy = direction.value
        next_col = max(self.min_col, min(self.max_col, self.player_col + dx))
        next_row = max(self.min_row, min(self.max_row, self.player_row + dy))
        moved = (next_col, next_row) != (self.player_col, self.player_row)
        self.player_col = next_col
        self.player_row = next_row
        return moved

    def spawn_magic_tile(self, col: int | None = None, row: int | None = None, ttl: int = 72) -> Tile:
        tile = Tile(
            col=self._random_col() if col is None else col,
            row=self._random_row() if row is None else row,
            ttl=ttl,
            kind="magic",
        )
        self.tiles.append(tile)
        return tile

    def spawn_hazard(self, col: int | None = None, row: int | None = None, ttl: int = 96) -> Tile:
        tile = Tile(
            col=self._random_col() if col is None else col,
            row=self._random_row() if row is None else row,
            ttl=ttl,
            kind="hazard",
        )
        self.tiles.append(tile)
        return tile

    def tick(self) -> None:
        if self.won or self.lost:
            return

        self.tick_count += 1
        if self.invincible_ticks > 0:
            self.invincible_ticks -= 1

        self._spawn_pattern()
        for tile in self.tiles:
            if not tile.expired and tile.col == self.player_col and tile.row == self.player_row:
                if tile.kind == "magic":
                    self._hit_boss(tile)
                elif tile.kind == "hazard":
                    self._hurt_player(tile)
            tile.tick()

        self.tiles = [tile for tile in self.tiles if not tile.expired]

    def _hit_boss(self, tile: Tile) -> None:
        tile.expired = True
        self.combo = min(self.combo + 1, 8)
        self.score += 100 * self.combo
        self.boss_health -= 1
        if self.boss_health <= 0:
            self._advance_phase()

    def _hurt_player(self, tile: Tile) -> None:
        tile.expired = True
        if self.invincible_ticks > 0:
            return
        self.combo = 0
        self.player_health -= 1
        self.invincible_ticks = 90
        if self.player_health <= 0:
            self.lost = True

    def _advance_phase(self) -> None:
        if self.phase == Phase.FINAL:
            self.won = True
            self.boss_health = 0
            self.score += max(0, 4000 - self.tick_count * 2)
            return

        next_phase = {
            Phase.ONE: Phase.TWO,
            Phase.TWO: Phase.THREE,
            Phase.THREE: Phase.FINAL,
        }[self.phase]
        self.phase = next_phase
        self.boss_health = self.phase_health(next_phase)
        self.tiles.clear()

    def _spawn_pattern(self) -> None:
        phase_value = self.phase.value
        magic_period = max(24, 58 - phase_value * 6)
        hazard_period = max(18, 48 - phase_value * 5)
        if self.tick_count % magic_period == 1:
            self.spawn_magic_tile()
        if self.tick_count % hazard_period == hazard_period // 2:
            self.spawn_hazard()

    def _random_col(self) -> int:
        return self.rng.randint(self.min_col, self.max_col)

    def _random_row(self) -> int:
        return self.rng.randint(self.min_row, self.max_row)

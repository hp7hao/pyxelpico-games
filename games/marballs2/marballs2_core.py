"""Pure rolling-ball rules for the Marballs 2 PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class Ball:
    x: float
    y: float
    z: float = 0.0
    dx: float = 0.0
    dy: float = 0.0
    dz: float = 0.0


class Marballs2Core:
    tile = 12
    accel = 0.16
    friction = 0.965
    max_speed = 2.8
    gravity_z = 0.24
    jump_pad_speed = -4.2
    wall_bounce = 0.82

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.tiles: list[list[str]] = []
        self.spawn_x = self.tile
        self.spawn_y = self.tile
        self.goal_x = 0
        self.goal_y = 0
        self.total_orbs = 0
        self.orbs = 0
        self.time = 0
        self.gold_time = 155
        self.ace_time = 125
        self.wall_hits = 0
        self.cleared = False
        self.medal = ""
        self.rotated_controls = False
        self.message = "simple"
        self.set_test_level([
            "################",
            "#@.............#",
            "#....J....o...G#",
            "#..............#",
            "################",
        ])

    def set_test_level(self, rows: list[str]) -> None:
        self.height = len(rows)
        self.width = len(rows[0])
        self.tiles = []
        self.total_orbs = 0
        self.orbs = 0
        self.time = 0
        self.wall_hits = 0
        self.cleared = False
        self.medal = ""
        self.message = "roll"
        for y, row in enumerate(rows):
            out = []
            for x, char in enumerate(row):
                if char == "@":
                    self.spawn_x = x * self.tile + self.tile / 2
                    self.spawn_y = y * self.tile + self.tile / 2
                    out.append(".")
                elif char == "G":
                    self.goal_x = x
                    self.goal_y = y
                    out.append("G")
                elif char == "o":
                    self.total_orbs += 1
                    out.append("o")
                else:
                    out.append(char)
            self.tiles.append(out)
        self.ball = Ball(self.spawn_x, self.spawn_y)

    def tick(
        self,
        *,
        left: bool = False,
        right: bool = False,
        up: bool = False,
        down: bool = False,
    ) -> None:
        if self.cleared:
            return
        self.time += 1
        ax, ay = self._input_axis(left=left, right=right, up=up, down=down)
        self.ball.dx += ax * self.accel
        self.ball.dy += ay * self.accel
        self._cap_speed()
        self.ball.dx *= self.friction
        self.ball.dy *= self.friction
        self._update_z()
        self._move_x(self.ball.dx)
        self._move_y(self.ball.dy)
        self._collect_or_trigger()

    def _input_axis(self, *, left: bool, right: bool, up: bool, down: bool) -> tuple[float, float]:
        x = int(right) - int(left)
        y = int(down) - int(up)
        if self.rotated_controls:
            return (x - y) * 0.72, (x + y) * 0.72
        return float(x), float(y)

    def _cap_speed(self) -> None:
        speed = (self.ball.dx * self.ball.dx + self.ball.dy * self.ball.dy) ** 0.5
        if speed > self.max_speed:
            scale = self.max_speed / speed
            self.ball.dx *= scale
            self.ball.dy *= scale

    def _update_z(self) -> None:
        if self.ball.z > 0 or self.ball.dz < 0:
            self.ball.dz += self.gravity_z
            self.ball.z += self.ball.dz
            if self.ball.z >= 0:
                self.ball.z = 0
                self.ball.dz = 0

    def _move_x(self, dx: float) -> None:
        self.ball.x += dx
        if self._blocked_at_ball():
            self.ball.x -= dx
            self.ball.dx = -self.ball.dx * self.wall_bounce
            self.wall_hits += 1
            self.message = "wall bounce"

    def _move_y(self, dy: float) -> None:
        self.ball.y += dy
        if self._blocked_at_ball():
            self.ball.y -= dy
            self.ball.dy = -self.ball.dy * self.wall_bounce
            self.wall_hits += 1
            self.message = "wall bounce"

    def _collect_or_trigger(self) -> None:
        tx, ty = self.ball_tile()
        tile = self.tile_at(tx, ty)
        if tile == "J" and self.ball.z == 0:
            self.ball.dz = self.jump_pad_speed
            self.ball.dx *= 1.08
            self.ball.dy *= 1.08
            self.message = "jump pad"
        elif tile == "o":
            self.orbs += 1
            self._set_tile(tx, ty, ".")
            self.message = "orb"
        elif tile == "G" and self.orbs >= self.total_orbs:
            self.cleared = True
            self.medal = "ace" if self.time <= self.ace_time else "gold" if self.time <= self.gold_time else "clear"
            self.message = "goal"
        elif tile == "G":
            self.message = "need orbs"

    def _blocked_at_ball(self) -> bool:
        radius = 4.5
        points = [
            (self.ball.x - radius, self.ball.y),
            (self.ball.x + radius, self.ball.y),
            (self.ball.x, self.ball.y - radius),
            (self.ball.x, self.ball.y + radius),
        ]
        return any(self.tile_at(int(x // self.tile), int(y // self.tile)) == "#" for x, y in points)

    def ball_tile(self) -> tuple[int, int]:
        return int(self.ball.x // self.tile), int(self.ball.y // self.tile)

    def tile_at(self, x: int, y: int) -> str:
        if x < 0 or y < 0 or y >= self.height or x >= self.width:
            return "#"
        return self.tiles[y][x]

    def _set_tile(self, x: int, y: int, value: str) -> None:
        self.tiles[y][x] = value

    def restart(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

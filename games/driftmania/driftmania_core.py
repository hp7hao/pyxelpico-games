"""Pure arcade drift-racing rules for the Driftmania PyxelPico port."""

from __future__ import annotations

import math
import random


class DriftmaniaCore:
    width = 240
    height = 240

    def __init__(self, seed: int = 1) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.start = (120.0, 198.0)
        self.x, self.y = self.start
        self.heading = -math.pi / 2
        self.speed = 0.0
        self.traction = 1.0
        self.boost_timer = 0
        self.elapsed = 0.0
        self.lap = 0
        self.next_checkpoint = 0
        self.finished = False
        self.medal: str | None = None
        self.message = "tiny tracks"
        self.checkpoints = [(120.0, 160.0), (182.0, 120.0), (120.0, 62.0), (58.0, 120.0), (120.0, 198.0)]
        self.boost_tiles = [(170.0, 142.0), (74.0, 94.0)]
        self.grass_tiles = [(44.0, 44.0), (196.0, 44.0), (44.0, 196.0), (196.0, 196.0)]

    def tick(self, *, accel: bool = False, brake: bool = False, turn: int = 0, drift: bool = False) -> None:
        if self.finished:
            return
        self.elapsed += 1 / 30
        on_grass = self._near_any(self.grass_tiles, radius=24)
        self.traction = 0.52 if on_grass else 0.72 if drift else 1.0
        if accel:
            self.speed += 0.18
        if brake:
            self.speed -= 0.24 if self.speed > 0 else 0.08
        self.speed *= 0.992 if not on_grass else 0.986
        self.speed = max(-1.8, min(self.speed, 5.4 + (1.6 if self.boost_timer > 0 else 0)))
        turn_rate = (0.028 + abs(self.speed) * 0.006) * (1.8 if drift else 1.0)
        self.heading += turn * turn_rate
        slide = (1.0 - self.traction) * turn * 1.4
        self.x += math.cos(self.heading) * self.speed + math.cos(self.heading + math.pi / 2) * slide
        self.y += math.sin(self.heading) * self.speed + math.sin(self.heading + math.pi / 2) * slide
        self.x = max(12, min(self.width - 12, self.x))
        self.y = max(12, min(self.height - 12, self.y))
        if self.boost_timer > 0:
            self.boost_timer -= 1
        if self._near_any(self.boost_tiles, radius=12):
            self.speed = min(7.0, self.speed + 1.4)
            self.boost_timer = 20
            self.message = "boost"
        self._check_checkpoint()

    def _check_checkpoint(self) -> None:
        gate = self.checkpoints[self.next_checkpoint]
        if self.distance((self.x, self.y), gate) > 13:
            return
        self.next_checkpoint += 1
        self.message = "checkpoint"
        if self.next_checkpoint >= len(self.checkpoints):
            self.lap += 1
            self.finished = True
            self.medal = self._medal_for_time(self.elapsed)
            self.message = f"{self.medal} medal"

    @staticmethod
    def _medal_for_time(elapsed: float) -> str:
        if elapsed <= 38:
            return "gold"
        if elapsed <= 48:
            return "silver"
        if elapsed <= 62:
            return "bronze"
        return "finish"

    def _near_any(self, points: list[tuple[float, float]], radius: float) -> bool:
        return any(self.distance((self.x, self.y), point) <= radius for point in points)

    @staticmethod
    def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def restart(self) -> None:
        self.__init__(self.seed)

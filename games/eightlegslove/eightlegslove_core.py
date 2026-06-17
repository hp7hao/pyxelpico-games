"""Pure web-building arcade rules for the 8 Legs to Love PyxelPico port."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import math
import random


ARENA_MIN = 24
ARENA_MAX = 216


@dataclass
class Strand:
    start: tuple[float, float]
    end: tuple[float, float]
    max_durability: int = 4
    durability: int = 4

    def length(self) -> float:
        return math.dist(self.start, self.end)


@dataclass
class Bug:
    kind: str
    x: float
    y: float
    vx: float
    vy: float


class EightLegsCore:
    score_values = {"fly": 10, "beetle": 30, "butterfly": 100}

    def __init__(self, seed: int = 1) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.level = 1
        self.spawn = (120.0, 120.0)
        self.x, self.y = self.spawn
        self.anchors = [
            (36.0, 36.0),
            (120.0, 26.0),
            (204.0, 36.0),
            (214.0, 120.0),
            (204.0, 204.0),
            (120.0, 214.0),
            (36.0, 204.0),
            (26.0, 120.0),
        ]
        self.strands: list[Strand] = []
        self.bugs: list[Bug] = []
        self.caught_counts: Counter[str] = Counter()
        self.score = 0
        self.time_left = 30 * 60
        self.goal_score = 70
        self.level_clear = False
        self.message = "spin a web"
        self._spin_start: tuple[float, float] | None = None
        self._spawn_timer = 20

    def tick(
        self,
        *,
        left: bool = False,
        right: bool = False,
        up: bool = False,
        down: bool = False,
        spin: bool = False,
        place: bool = False,
    ) -> None:
        if self.level_clear:
            return
        self._move_spider(left=left, right=right, up=up, down=down)
        if spin and self._spin_start is None:
            self._spin_start = self.spider_pos()
            self.message = "spinning web"
        if place and self._spin_start is not None:
            if math.dist(self._spin_start, self.spider_pos()) >= 2:
                self.add_strand(self._spin_start, self.spider_pos())
                self.message = "web placed"
            self._spin_start = None
        if not spin and place:
            self._spin_start = None

        self._spawn_timer -= 1
        if self._spawn_timer <= 0:
            self._spawn_random_bug()
            self._spawn_timer = max(12, 36 - self.level * 3)
        self._update_bugs()
        self.time_left = max(0, self.time_left - 1)
        if self.score >= self.goal_score or self.time_left == 0:
            self.level_clear = True
            self.message = "level clear" if self.score >= self.goal_score else "web complete"

    def _move_spider(self, *, left: bool, right: bool, up: bool, down: bool) -> None:
        speed = 3.0
        dx = (-speed if left else 0.0) + (speed if right else 0.0)
        dy = (-speed if up else 0.0) + (speed if down else 0.0)
        if dx and dy:
            dx *= 0.707
            dy *= 0.707
        self.x = min(ARENA_MAX, max(ARENA_MIN, self.x + dx))
        self.y = min(ARENA_MAX, max(ARENA_MIN, self.y + dy))

    def _spawn_random_bug(self) -> None:
        roll = self.rng.random()
        if roll < 0.08:
            kind = "butterfly"
        elif roll < 0.28:
            kind = "beetle"
        else:
            kind = "fly"
        side = self.rng.randrange(4)
        if side == 0:
            x, y, vx, vy = self.rng.uniform(36, 204), 18.0, 0.0, self.rng.uniform(1.0, 2.0)
        elif side == 1:
            x, y, vx, vy = 222.0, self.rng.uniform(36, 204), -self.rng.uniform(1.0, 2.0), 0.0
        elif side == 2:
            x, y, vx, vy = self.rng.uniform(36, 204), 222.0, 0.0, -self.rng.uniform(1.0, 2.0)
        else:
            x, y, vx, vy = 18.0, self.rng.uniform(36, 204), self.rng.uniform(1.0, 2.0), 0.0
        if kind == "butterfly":
            vx *= 1.25
            vy *= 1.25
        self.spawn_bug(kind=kind, x=x, y=y, vx=vx, vy=vy)

    def _update_bugs(self) -> None:
        survivors: list[Bug] = []
        for bug in self.bugs:
            bug.x += bug.vx
            bug.y += bug.vy
            strand = self._hit_strand(bug.x, bug.y)
            if strand is not None:
                self.score += self.score_values[bug.kind]
                self.caught_counts[bug.kind] += 1
                if bug.kind == "beetle":
                    strand.durability -= 2
                    self.message = "beetle chewed web"
                elif bug.kind == "butterfly":
                    self.message = "butterfly caught"
                else:
                    self.message = "bug caught"
                continue
            if ARENA_MIN - 18 <= bug.x <= ARENA_MAX + 18 and ARENA_MIN - 18 <= bug.y <= ARENA_MAX + 18:
                survivors.append(bug)
        self.bugs = survivors
        self.strands = [strand for strand in self.strands if strand.durability > 0]

    def _hit_strand(self, x: float, y: float) -> Strand | None:
        for strand in self.strands:
            if self._distance_to_segment((x, y), strand.start, strand.end) <= 5.0:
                return strand
        return None

    @staticmethod
    def _distance_to_segment(
        point: tuple[float, float], start: tuple[float, float], end: tuple[float, float]
    ) -> float:
        px, py = point
        ax, ay = start
        bx, by = end
        dx = bx - ax
        dy = by - ay
        if dx == 0 and dy == 0:
            return math.dist(point, start)
        t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
        return math.dist(point, (ax + t * dx, ay + t * dy))

    def add_strand(self, start: tuple[float, float], end: tuple[float, float]) -> Strand:
        strand = Strand(start=start, end=end, max_durability=4 + self.level // 2, durability=4 + self.level // 2)
        self.strands.append(strand)
        return strand

    def spawn_bug(self, *, kind: str, x: float, y: float, vx: float, vy: float) -> None:
        if kind not in self.score_values:
            raise ValueError(f"unknown bug kind: {kind}")
        self.bugs.append(Bug(kind=kind, x=x, y=y, vx=vx, vy=vy))

    def spider_pos(self) -> tuple[float, float]:
        return self.x, self.y

    def preview_strand(self) -> tuple[tuple[float, float], tuple[float, float]] | None:
        if self._spin_start is None:
            return None
        return self._spin_start, self.spider_pos()

    def advance_level(self) -> int:
        self.level += 1
        level = self.level
        next_seed = self.rng.randint(0, 999_999)
        self.__init__(seed=next_seed)
        self.level = level
        self.goal_score = 70 + (level - 1) * 35
        self.time_left = max(30 * 35, 30 * (65 - level * 4))
        self.message = f"level {level}"
        return self.level

    def restart(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

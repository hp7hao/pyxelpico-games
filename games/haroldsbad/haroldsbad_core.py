"""Pure puzzle-platformer rules for the Harold's Bad Day PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class Harold:
    x: float = 24.0
    y: float = 152.0
    vx: float = 0.0
    vy: float = 0.0
    grounded: bool = True
    dead: bool = False
    drown_timer: int = 0


@dataclass(frozen=True)
class Corpse:
    x: float
    y: float
    reason: str


class HaroldsBadCore:
    ground_y = 172
    goal_x = 214
    drown_frames = 70

    def __init__(self, seed: int = 1) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.player = Harold()
        self.lives = 6
        self.corpses: list[Corpse] = []
        self.deaths = 0
        self.harolds_saved = 0
        self.elapsed_frames = 0
        self.level = 1
        self.level_complete = False
        self.game_over = False
        self.message = "save harold"
        self.wind = 0.0

    def tick(self, *, move: int = 0, jump: bool = False) -> None:
        if self.level_complete or self.game_over:
            return
        self.elapsed_frames += 1
        p = self.player
        if p.dead:
            return
        if jump and p.grounded:
            p.vy = -5.0
            p.grounded = False
        p.vx += max(-1, min(1, move)) * 0.45 + self.wind
        p.vx *= 0.82
        p.vx = max(-2.1, min(2.1, p.vx))
        p.vy += 0.32
        p.vy = min(5.0, p.vy)
        p.x += p.vx
        p.y += p.vy
        p.x = max(8.0, min(232.0, p.x))
        self._platform_collisions()
        self._water_and_hazards()
        self.check_goal()

    def kill_player(self, reason: str) -> None:
        p = self.player
        if p.dead:
            return
        p.dead = True
        self.deaths += 1
        self.lives -= 1
        self.corpses.append(Corpse(p.x, min(self.ground_y, p.y), reason))
        self.message = reason
        if self.lives <= 0:
            self.game_over = True
        else:
            self.player = Harold()

    def check_goal(self) -> None:
        p = self.player
        if not p.dead and abs(p.x - self.goal_x) < 12 and p.y <= self.ground_y:
            self.level_complete = True
            self.harolds_saved = max(0, self.lives)
            self.message = "level clear"

    def next_level(self) -> None:
        self.level += 1
        old_saved = self.harolds_saved
        self.__init__(self.seed + self.level)
        self.level = min(32, self.level)
        self.harolds_saved = old_saved

    def restart(self) -> None:
        self.__init__(self.seed)

    def _platform_collisions(self) -> None:
        p = self.player
        p.grounded = False
        if p.y >= self.ground_y and not self._over_gap(p.x):
            p.y = self.ground_y
            p.vy = 0.0
            p.grounded = True
        for corpse in self.corpses:
            if abs(p.x - corpse.x) < 22 and corpse.y - 12 <= p.y <= corpse.y + 6 and p.vy >= 0:
                p.y = corpse.y - 12
                p.vy = 0.0
                p.grounded = True
        if p.y > 230 and not (112 <= p.x <= 166):
            self.kill_player("fell")

    def _over_gap(self, x: float) -> bool:
        if 88 <= x <= 118:
            return not any(abs(corpse.x - 100) < 28 for corpse in self.corpses)
        return False

    def _water_and_hazards(self) -> None:
        p = self.player
        if 112 <= p.x <= 166 and p.y >= 176:
            p.y = min(p.y, 196)
            p.drown_timer += 1
            p.vy -= 0.16
            p.vx *= 0.86
            if p.drown_timer > self.drown_frames:
                self.kill_player("drowned")
        else:
            p.drown_timer = max(0, p.drown_timer - 3)
        if 176 <= p.x <= 194 and p.y >= self.ground_y:
            self.kill_player("spikes")

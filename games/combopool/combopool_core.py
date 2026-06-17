"""Pure marble-merge pool rules for the Combo Pool PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import math
import random


@dataclass
class Ball:
    x: float
    y: float
    level: int
    vx: float = 0.0
    vy: float = 0.0
    rebounds: int = 0
    dead: bool = False


class ComboPoolCore:
    width = 240
    height = 240
    radius = 8
    final_level = 5

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.aim = 0.0
        self.cooldown = 0
        self.life = 80
        self.score = 0
        self.combo = 0
        self.won = False
        self.lost = False
        self.balls = [
            Ball(82, 100, 1),
            Ball(152, 110, 1),
            Ball(120, 152, 2),
        ]

    def reset(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

    def rotate_aim(self, direction: int, slow: bool = False) -> None:
        self.aim += direction * (0.035 if slow else 0.08)
        self.aim = max(-1.2, min(1.2, self.aim))

    def shoot(self) -> None:
        if self.cooldown > 0 or self.won or self.lost:
            return
        speed = 4.2
        self.balls.append(
            Ball(
                x=24,
                y=self.height / 2,
                level=1,
                vx=math.cos(self.aim) * speed,
                vy=math.sin(self.aim) * speed,
            )
        )
        self.cooldown = 30

    def tick(self) -> None:
        if self.won or self.lost:
            return
        self.cooldown = max(0, self.cooldown - 1)
        pressure = max(0, len(self.balls) - 5) + sum(max(0, ball.level - 3) for ball in self.balls)
        if pressure > 0:
            self.life -= pressure
            if self.life <= 0:
                self.lost = True
                return
        for ball in self.balls:
            if ball.dead:
                continue
            ball.x += ball.vx
            ball.y += ball.vy
            ball.vx *= 0.985
            ball.vy *= 0.985
            self._bounce(ball)
        self._collide_and_merge()
        self.balls = [ball for ball in self.balls if not ball.dead]

    def _bounce(self, ball: Ball) -> None:
        if ball.x <= self.radius:
            ball.x = self.radius
            ball.vx = abs(ball.vx)
            ball.rebounds += 1
        elif ball.x >= self.width - self.radius:
            ball.x = self.width - self.radius
            ball.vx = -abs(ball.vx)
            ball.rebounds += 1
        if ball.y <= 32 + self.radius:
            ball.y = 32 + self.radius
            ball.vy = abs(ball.vy)
            ball.rebounds += 1
        elif ball.y >= self.height - self.radius:
            ball.y = self.height - self.radius
            ball.vy = -abs(ball.vy)
            ball.rebounds += 1

    def _collide_and_merge(self) -> None:
        for i, left in enumerate(self.balls):
            if left.dead:
                continue
            for right in self.balls[i + 1 :]:
                if right.dead:
                    continue
                dx = right.x - left.x
                dy = right.y - left.y
                if dx * dx + dy * dy > (self.radius * 2) ** 2:
                    continue
                if left.level == right.level:
                    self._merge(left, right)
                else:
                    left.vx, right.vx = right.vx, left.vx
                    left.vy, right.vy = right.vy, left.vy

    def _merge(self, left: Ball, right: Ball) -> None:
        level = min(self.final_level + 1, left.level + 1)
        left.x = (left.x + right.x) / 2
        left.y = (left.y + right.y) / 2
        left.level = level
        left.vx = (left.vx + right.vx) * 0.25
        left.vy = (left.vy + right.vy) * 0.25
        left.rebounds = max(left.rebounds, right.rebounds)
        right.dead = True
        self.combo += 1
        self.score += level * 10 + left.rebounds * 2 + self.combo * 5
        self.life = min(80, self.life + 8)
        if level > self.final_level:
            self.won = True

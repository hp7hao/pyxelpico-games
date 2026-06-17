"""Pure platform-shooter rules for the X-Zero PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class Enemy:
    x: float
    y: float
    hp: int
    dead: bool = False


@dataclass
class Shot:
    x: float
    y: float
    dx: float
    dy: float
    ttl: int = 36
    dead: bool = False


class XZeroCore:
    width = 240
    height = 240
    ground_y = 184.0
    exit_x = 220.0
    final_zone = 4

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.zone = 1
        self.max_hp = 5
        self.player_hp = self.max_hp
        self.player_x = 24.0
        self.player_y = self.ground_y
        self.vx = 0.0
        self.vy = 0.0
        self.facing = 1
        self.aim_y = 0
        self.on_ground = True
        self.iframes = 0
        self.cooldown = 0
        self.score = 0
        self.won = False
        self.lost = False
        self.enemies: list[Enemy] = []
        self.shots: list[Shot] = []
        self.pickups: list[tuple[float, float]] = []
        self._populate_zone()

    def reset(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

    def move(self, direction: int) -> None:
        if self.won or self.lost:
            return
        self.vx = max(-2.4, min(2.4, self.vx + direction * 0.7))
        if direction:
            self.facing = 1 if direction > 0 else -1

    def jump(self) -> None:
        if self.on_ground and not (self.won or self.lost):
            self.vy = -6.2
            self.on_ground = False

    def shoot(self) -> None:
        if self.cooldown > 0 or self.won or self.lost:
            return
        speed = 5.0
        dy = self.aim_y * 2.2
        dx = self.facing * speed
        self.shots.append(Shot(self.player_x + self.facing * 8, self.player_y - 8, dx, dy))
        self.cooldown = 8

    def tick(self) -> None:
        if self.won or self.lost:
            return
        self.cooldown = max(0, self.cooldown - 1)
        self.iframes = max(0, self.iframes - 1)
        self._physics()
        self._update_shots()
        self._enemy_contacts()
        self._collect_pickups()
        if self.player_x >= self.exit_x:
            self._advance_zone()
        if self.player_hp <= 0:
            self.lost = True

    def _physics(self) -> None:
        self.player_x = max(12, min(self.exit_x, self.player_x + self.vx))
        self.player_y += self.vy
        self.vx *= 0.82
        self.vy += 0.35
        if self.player_y >= self.ground_y:
            self.player_y = self.ground_y
            self.vy = 0
            self.on_ground = True

    def _update_shots(self) -> None:
        for shot in self.shots:
            shot.x += shot.dx
            shot.y += shot.dy
            shot.ttl -= 1
            if shot.ttl <= 0 or shot.x < 0 or shot.x > self.width or shot.y < 0 or shot.y > self.height:
                shot.dead = True
                continue
            for enemy in self.enemies:
                if enemy.dead:
                    continue
                if abs(shot.x - enemy.x) <= 9 and abs(shot.y - enemy.y) <= 12:
                    shot.dead = True
                    enemy.hp -= 1
                    if enemy.hp <= 0:
                        enemy.dead = True
                        self.score += 10
                        self.pickups.append((enemy.x, enemy.y))
                    break
        self.shots = [shot for shot in self.shots if not shot.dead]

    def _enemy_contacts(self) -> None:
        for enemy in self.enemies:
            if enemy.dead:
                continue
            enemy.x += -0.4 if enemy.x > self.player_x else 0.4
            if abs(enemy.x - self.player_x) <= 10 and abs(enemy.y - self.player_y) <= 14 and self.iframes == 0:
                self.player_hp -= 1
                self.iframes = 40

    def _collect_pickups(self) -> None:
        kept = []
        for x, y in self.pickups:
            if abs(x - self.player_x) <= 12 and abs(y - self.player_y) <= 16:
                self.player_hp = min(self.max_hp, self.player_hp + 2)
                self.score += 5
            else:
                kept.append((x, y))
        self.pickups = kept

    def _advance_zone(self) -> None:
        if self.zone >= self.final_zone:
            self.won = True
            return
        self.zone += 1
        self.player_x = 24.0
        self.player_y = self.ground_y
        self.vx = self.vy = 0.0
        self._populate_zone()

    def _populate_zone(self) -> None:
        self.enemies = []
        self.shots = []
        self.pickups = []
        for index in range(2 + self.zone):
            x = 72 + index * 38 + self.rng.randint(-8, 8)
            self.enemies.append(Enemy(float(min(205, x)), self.ground_y, hp=1 + self.zone // 2))

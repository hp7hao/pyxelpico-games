"""Pure gameplay core for the Birds With Guns PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math
import random


class Weapon(Enum):
    REVOLVER = 0
    SHOTGUN = 1


@dataclass
class Enemy:
    x: float
    y: float
    hp: int
    speed: float
    boss: bool = False
    dead: bool = False


@dataclass
class Bullet:
    x: float
    y: float
    dx: float
    dy: float
    ttl: int
    damage: int
    dead: bool = False


class BirdsCore:
    width = 240
    height = 240
    final_wagon = 7

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.player_x = 48.0
        self.player_y = 120.0
        self.player_hp = 10
        self.max_hp = 10
        self.iframes = 0
        self.weapon = Weapon.REVOLVER
        self.ammo = {Weapon.REVOLVER: 80, Weapon.SHOTGUN: 28}
        self.cooldown = 0
        self.wagon = 1
        self.score = 0
        self.kills = 0
        self.tick_count = 0
        self.won = False
        self.lost = False
        self.enemies: list[Enemy] = []
        self.bullets: list[Bullet] = []
        self.spawn_wagon()

    def reset(self) -> None:
        seed = self.rng.randint(0, 999_999)
        self.__init__(seed=seed)

    def move_player(self, dx: float, dy: float) -> None:
        if self.won or self.lost:
            return
        length = math.hypot(dx, dy)
        if length > 0:
            speed = 2.1
            dx = dx / length * speed
            dy = dy / length * speed
        self.player_x = min(self.width - 12, max(12, self.player_x + dx))
        self.player_y = min(self.height - 18, max(24, self.player_y + dy))

    def swap_weapon(self) -> None:
        self.weapon = Weapon.SHOTGUN if self.weapon == Weapon.REVOLVER else Weapon.REVOLVER

    def spawn_enemy(self, x: float, y: float, boss: bool = False) -> Enemy:
        enemy = Enemy(
            x=x,
            y=y,
            hp=10 if boss else 2,
            speed=0.45 if boss else 0.65 + self.wagon * 0.04,
            boss=boss,
        )
        self.enemies.append(enemy)
        return enemy

    def spawn_wagon(self) -> None:
        self.enemies.clear()
        self.bullets.clear()
        if self.wagon >= self.final_wagon:
            self.spawn_enemy(self.width - 48, self.height / 2, boss=True)
            return
        count = min(2 + self.wagon, 7)
        for index in range(count):
            x = self.rng.randint(92, self.width - 22)
            y = self.rng.randint(42, self.height - 32)
            enemy = self.spawn_enemy(x, y)
            if index % 3 == 0:
                enemy.hp += 1

    def shoot(self) -> bool:
        if self.won or self.lost or self.cooldown > 0 or self.ammo[self.weapon] <= 0:
            return False
        target = self.nearest_enemy()
        if target is None:
            return False
        angle = math.atan2(target.y - self.player_y, target.x - self.player_x)
        if self.weapon == Weapon.REVOLVER:
            self._spawn_bullet(angle, damage=1, ttl=48)
            self.cooldown = 9
        else:
            for offset in (-0.22, 0.0, 0.22):
                self._spawn_bullet(angle + offset, damage=1, ttl=28)
            self.cooldown = 18
        self.ammo[self.weapon] -= 1
        return True

    def nearest_enemy(self) -> Enemy | None:
        living = [enemy for enemy in self.enemies if not enemy.dead]
        if not living:
            return None
        return min(living, key=lambda enemy: self._dist2(enemy.x, enemy.y, self.player_x, self.player_y))

    def tick(self) -> None:
        if self.won or self.lost:
            return
        self.tick_count += 1
        self.cooldown = max(0, self.cooldown - 1)
        self.iframes = max(0, self.iframes - 1)
        self._update_bullets()
        self._update_enemies()
        self.enemies = [enemy for enemy in self.enemies if not enemy.dead]
        self.bullets = [bullet for bullet in self.bullets if not bullet.dead]
        if not self.enemies:
            if self.wagon >= self.final_wagon:
                self.won = True
            else:
                self.wagon += 1
                self.player_x = 28
                self.spawn_wagon()

    def _spawn_bullet(self, angle: float, damage: int, ttl: int) -> None:
        speed = 4.2
        self.bullets.append(
            Bullet(
                x=self.player_x,
                y=self.player_y,
                dx=math.cos(angle) * speed,
                dy=math.sin(angle) * speed,
                ttl=ttl,
                damage=damage,
            )
        )

    def _update_bullets(self) -> None:
        for bullet in self.bullets:
            bullet.x += bullet.dx
            bullet.y += bullet.dy
            bullet.ttl -= 1
            if bullet.ttl <= 0 or bullet.x < 0 or bullet.x > self.width or bullet.y < 0 or bullet.y > self.height:
                bullet.dead = True
                continue
            for enemy in self.enemies:
                if enemy.dead:
                    continue
                radius = 13 if enemy.boss else 8
                if self._dist2(bullet.x, bullet.y, enemy.x, enemy.y) <= radius * radius:
                    enemy.hp -= bullet.damage
                    bullet.dead = True
                    if enemy.hp <= 0:
                        enemy.dead = True
                        self.kills += 1
                        self.score += 500 if enemy.boss else 100
                    break

    def _update_enemies(self) -> None:
        for enemy in self.enemies:
            if enemy.dead:
                continue
            dx = self.player_x - enemy.x
            dy = self.player_y - enemy.y
            length = math.hypot(dx, dy) or 1.0
            enemy.x += dx / length * enemy.speed
            enemy.y += dy / length * enemy.speed
            if self._dist2(enemy.x, enemy.y, self.player_x, self.player_y) <= (14 if enemy.boss else 10) ** 2:
                self._touch_enemy(enemy)

    def _touch_enemy(self, enemy: Enemy) -> None:
        if self.iframes > 0:
            return
        self.player_hp -= 2 if enemy.boss else 1
        self.iframes = 45
        if not enemy.boss:
            enemy.dead = True
        if self.player_hp <= 0:
            self.lost = True

    @staticmethod
    def _dist2(ax: float, ay: float, bx: float, by: float) -> float:
        return (ax - bx) ** 2 + (ay - by) ** 2

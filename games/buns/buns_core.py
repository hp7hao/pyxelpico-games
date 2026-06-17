"""Pure survivor rules for the Buns PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math
import random


class Upgrade(Enum):
    DAMAGE = "damage"
    HASTE = "haste"
    HEART = "heart"


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
    damage: int
    ttl: int
    dead: bool = False


@dataclass
class Gem:
    x: float
    y: float
    dead: bool = False


class BunsCore:
    width = 240
    height = 240
    boss_time = 580

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.player_x = 120.0
        self.player_y = 120.0
        self.max_hp = 6
        self.player_hp = self.max_hp
        self.iframes = 0
        self.speed = 2.0
        self.damage = 1
        self.fire_cooldown = 0
        self.fire_rate = 18
        self.timer = 0
        self.spawn_timer = 0
        self.level = 0
        self.exp = 0
        self.exp_needed = 3
        self.kills = 0
        self.awaiting_upgrade = False
        self.boss_spawned = False
        self.won = False
        self.lost = False
        self.enemies: list[Enemy] = []
        self.bullets: list[Bullet] = []
        self.gems: list[Gem] = []

    def reset(self) -> None:
        seed = self.rng.randint(0, 999_999)
        self.__init__(seed=seed)

    def move_player(self, dx: float, dy: float) -> None:
        if self.won or self.lost:
            return
        length = math.hypot(dx, dy)
        if length > 0:
            dx = dx / length * self.speed
            dy = dy / length * self.speed
        self.player_x = min(self.width - 12, max(12, self.player_x + dx))
        self.player_y = min(self.height - 12, max(20, self.player_y + dy))

    def tick(self) -> None:
        if self.won or self.lost or self.awaiting_upgrade:
            return
        self.timer += 1
        self.iframes = max(0, self.iframes - 1)
        self.fire_cooldown = max(0, self.fire_cooldown - 1)
        self._maybe_spawn()
        self._auto_fire()
        self._update_bullets()
        self._update_enemies()
        self._collect_gems()
        self.enemies = [enemy for enemy in self.enemies if not enemy.dead]
        self.bullets = [bullet for bullet in self.bullets if not bullet.dead]
        self.gems = [gem for gem in self.gems if not gem.dead]

    def spawn_enemy(self, x: float, y: float, hp: int = 2, boss: bool = False) -> Enemy:
        enemy = Enemy(x=x, y=y, hp=hp, speed=0.55 if not boss else 0.35, boss=boss)
        self.enemies.append(enemy)
        return enemy

    def spawn_gem(self, x: float, y: float) -> Gem:
        gem = Gem(x=x, y=y)
        self.gems.append(gem)
        return gem

    def apply_upgrade(self, upgrade: Upgrade) -> None:
        if upgrade is Upgrade.DAMAGE:
            self.damage += 1
        elif upgrade is Upgrade.HASTE:
            self.fire_rate = max(6, self.fire_rate - 3)
            self.speed += 0.25
        elif upgrade is Upgrade.HEART:
            self.max_hp += 1
            self.player_hp = self.max_hp
        self.awaiting_upgrade = False

    def _maybe_spawn(self) -> None:
        if self.timer >= self.boss_time and not self.boss_spawned:
            self.boss_spawned = True
            self.spawn_enemy(self.width - 32, self.height / 2, hp=24, boss=True)
            return
        if self.boss_spawned:
            return
        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.spawn_timer = max(15, 48 - self.timer // 30)
            angle = self.rng.random()
            radius = 125
            self.spawn_enemy(
                self.player_x + math.cos(angle * math.tau) * radius,
                self.player_y + math.sin(angle * math.tau) * radius,
                hp=1 + self.timer // 180,
            )

    def _auto_fire(self) -> None:
        if self.fire_cooldown > 0:
            return
        target = self._nearest_enemy()
        if target is None:
            return
        angle = math.atan2(target.y - self.player_y, target.x - self.player_x)
        speed = 4.5
        self.bullets.append(
            Bullet(
                x=self.player_x,
                y=self.player_y,
                dx=math.cos(angle) * speed,
                dy=math.sin(angle) * speed,
                damage=self.damage,
                ttl=48,
            )
        )
        self.fire_cooldown = self.fire_rate

    def _nearest_enemy(self) -> Enemy | None:
        living = [enemy for enemy in self.enemies if not enemy.dead]
        if not living:
            return None
        return min(living, key=lambda enemy: self._dist2(enemy.x, enemy.y, self.player_x, self.player_y))

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
                radius = 15 if enemy.boss else 8
                if self._dist2(bullet.x, bullet.y, enemy.x, enemy.y) <= radius * radius:
                    bullet.dead = True
                    self._damage_enemy(enemy, bullet.damage)
                    break

    def _damage_enemy(self, enemy: Enemy, amount: int) -> None:
        enemy.hp -= amount
        if enemy.hp <= 0:
            enemy.dead = True
            self.kills += 1
            if enemy.boss:
                self.won = True
            else:
                self.spawn_gem(enemy.x, enemy.y)

    def _update_enemies(self) -> None:
        for enemy in self.enemies:
            if enemy.dead:
                continue
            dx = self.player_x - enemy.x
            dy = self.player_y - enemy.y
            length = math.hypot(dx, dy) or 1.0
            enemy.x += dx / length * enemy.speed
            enemy.y += dy / length * enemy.speed
            if self._dist2(enemy.x, enemy.y, self.player_x, self.player_y) <= (15 if enemy.boss else 10) ** 2:
                self._touch_enemy(enemy)

    def _touch_enemy(self, enemy: Enemy) -> None:
        if self.iframes > 0:
            return
        self.player_hp -= 2 if enemy.boss else 1
        self.iframes = 50
        if not enemy.boss:
            enemy.dead = True
        if self.player_hp <= 0:
            self.lost = True

    def _collect_gems(self) -> None:
        for gem in self.gems:
            if self._dist2(gem.x, gem.y, self.player_x, self.player_y) <= 14 * 14:
                gem.dead = True
                self.exp += 1
                if self.exp >= self.exp_needed:
                    self.level += 1
                    self.exp = 0
                    self.exp_needed = 7 if self.level == 1 else min(90, int(self.exp_needed * 1.2) + 1)
                    self.awaiting_upgrade = True

    @staticmethod
    def _dist2(ax: float, ay: float, bx: float, by: float) -> float:
        return (ax - bx) ** 2 + (ay - by) ** 2

"""Pure platform-adventure rules for the Little Dragon Adventure port."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class Player:
    x: float
    y: float
    dx: float = 0.0
    dy: float = 0.0
    facing: int = 1
    on_ground: bool = True
    jumps_left: int = 2
    fire_cooldown: int = 0


@dataclass
class Enemy:
    x: float
    y: float
    hp: int
    kind: str = "skeleton"
    alive: bool = True


@dataclass
class Fireball:
    x: float
    y: float
    dx: float
    life: int = 35


class LittleDragonCore:
    floor_y = 96.0
    gravity = 0.42
    move_speed = 2.1
    jump_speed = -6.2
    checkpoint_x = 84
    total_eggs = 3

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.player = Player(20, self.floor_y)
        self.spawn_x = 20
        self.spawn_y = self.floor_y
        self.eggs = 0
        self.deaths = 0
        self.cleared = False
        self.message = "save the dragon eggs"
        self.fireballs: list[Fireball] = []
        self.enemies = [Enemy(76, self.floor_y, 1), Enemy(142, self.floor_y, 2, "jelly"), Enemy(186, self.floor_y, 1)]
        self.boss = Enemy(218, self.floor_y, 3, "chiro boss")
        self.hazards = [(120, self.floor_y), (170, self.floor_y)]

    def tick(
        self,
        *,
        left: bool = False,
        right: bool = False,
        jump: bool = False,
        fire: bool = False,
    ) -> None:
        if self.cleared:
            return
        self._update_player(left=left, right=right, jump=jump, fire=fire)
        self._update_fireballs()
        self._check_world_events()

    def _update_player(self, *, left: bool, right: bool, jump: bool, fire: bool) -> None:
        axis = int(right) - int(left)
        if axis:
            self.player.facing = axis
        self.player.dx = axis * self.move_speed
        self.player.x = max(0, min(232, self.player.x + self.player.dx))
        if jump and self.player.jumps_left > 0:
            self.player.dy = self.jump_speed
            self.player.on_ground = False
            self.player.jumps_left -= 1
            self.message = "hop"
        self.player.dy += self.gravity
        self.player.y += self.player.dy
        if self.player.y >= self.floor_y:
            self.player.y = self.floor_y
            self.player.dy = 0
            self.player.on_ground = True
            self.player.jumps_left = 2
        if self.player.fire_cooldown > 0:
            self.player.fire_cooldown -= 1
        if fire and self.player.fire_cooldown == 0:
            self.fireballs.append(Fireball(self.player.x + self.player.facing * 8, self.player.y - 6, self.player.facing * 4.2))
            self.player.fire_cooldown = 10
            self.message = "fire blast"

    def _update_fireballs(self) -> None:
        kept = []
        for ball in self.fireballs:
            ball.x += ball.dx
            ball.life -= 1
            hit = self._hit_enemy_or_boss(ball)
            if ball.life > 0 and not hit and 0 <= ball.x <= 240:
                kept.append(ball)
        self.fireballs = kept

    def _hit_enemy_or_boss(self, ball: Fireball) -> bool:
        for enemy in self.enemies:
            if enemy.alive and abs(ball.x - enemy.x) < 8 and abs(ball.y - enemy.y) < 14:
                enemy.hp -= 1
                if enemy.hp <= 0:
                    enemy.alive = False
                    self.eggs = min(self.total_eggs, self.eggs + 1)
                    self.message = "egg rescued"
                else:
                    self.message = "enemy hit"
                return True
        if abs(ball.x - self.boss.x) < 12 and abs(ball.y - self.boss.y) < 18:
            if self.eggs < self.total_eggs:
                self.message = "need dragon eggs"
                return True
            self.boss.hp -= 1
            self.message = "boss hit"
            if self.boss.hp <= 0:
                self.cleared = True
                self.message = "eggs saved"
            return True
        return False

    def _check_world_events(self) -> None:
        if abs(self.player.x - self.checkpoint_x) < 7 and self.player.on_ground:
            self.spawn_x = self.checkpoint_x
            self.spawn_y = self.floor_y
            self.message = "checkpoint"
        for hx, hy in self.hazards:
            if abs(self.player.x - hx) < 6 and abs(self.player.y - hy) < 10:
                self._respawn()
                return
        for enemy in self.enemies:
            if enemy.alive and abs(self.player.x - enemy.x) < 7 and abs(self.player.y - enemy.y) < 12:
                self._respawn()
                return

    def _respawn(self) -> None:
        self.deaths += 1
        self.player = Player(self.spawn_x, self.spawn_y)
        self.fireballs = []
        self.message = "checkpoint"

    def restart(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

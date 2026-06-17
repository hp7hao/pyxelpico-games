"""Pure arcade-shooter rules for the Cherry Bomb PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class Enemy:
    x: float
    y: float
    kind: int = 1
    hp: int = 1
    attacking: bool = False
    vx: float = 0.0
    vy: float = 0.25


class CherryBombCore:
    width = 240
    height = 240
    max_lives = 4

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.player_x = 120.0
        self.player_y = 204.0
        self.wave = 0
        self.score = 0
        self.lives = self.max_lives
        self.cherries = 0
        self.game_over = False
        self.victory = False
        self.cooldown = 0
        self.tick_count = 0
        self.wave_clear_timer = 0
        self.message = "blast 9 waves"
        self.bullets: list[tuple[float, float, float, float]] = []
        self.enemy_bullets: list[tuple[float, float, float, float]] = []
        self.pickups: list[tuple[float, float]] = []
        self.enemies: list[Enemy] = []
        self.spawn_wave(0)

    def spawn_wave(self, wave: int) -> None:
        self.wave = wave
        cols = min(6, 3 + wave // 2)
        rows = min(3, 1 + wave // 3)
        self.enemies = []
        for row in range(rows):
            for col in range(cols):
                kind = 1 + ((row + wave) % 3)
                hp = 1 if kind < 3 else 2
                self.enemies.append(Enemy(48 + col * 26, 38 + row * 22, kind=kind, hp=hp))
        self.bullets = []
        self.enemy_bullets = []
        self.pickups = []
        self.message = f"wave {wave + 1}"

    def tick(
        self,
        *,
        left: bool = False,
        right: bool = False,
        up: bool = False,
        down: bool = False,
    ) -> None:
        if self.game_over or self.victory:
            return
        self.tick_count += 1
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.wave_clear_timer > 0:
            self.wave_clear_timer -= 1
        self._move_player(left=left, right=right, up=up, down=down)
        self._update_bullets()
        self._update_enemies()
        self._update_pickups()
        self._check_player_hits()
        if not self.enemies and not self.game_over and self.wave_clear_timer == 0:
            if self.wave >= 8:
                self.victory = True
                self.message = "all waves clear"
            else:
                self.spawn_wave(self.wave + 1)

    def shoot(self) -> bool:
        if self.game_over or self.victory or self.cooldown > 0:
            return False
        self.bullets.append((self.player_x, self.player_y - 10, 0.0, -6.0))
        self.cooldown = 7
        self.message = "shoot"
        return True

    def bomb(self) -> bool:
        if self.game_over or self.victory or self.cherries <= 0:
            self.message = "need cherries"
            return False
        radius = 32 + self.cherries * 8
        spent = self.cherries
        self.cherries = 0
        cleared_bullets = len(self.enemy_bullets)
        self.enemy_bullets = []
        survivors: list[Enemy] = []
        for enemy in self.enemies:
            if self._dist(enemy.x, enemy.y, self.player_x, self.player_y) <= radius:
                self.score += 100 * enemy.kind
                self._maybe_drop_cherry(enemy.x, enemy.y, force=spent >= 5)
            else:
                survivors.append(enemy)
        self.enemies = survivors
        self.score += cleared_bullets * 25
        self.message = "cherry bomb"
        return True

    def restart(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

    def _move_player(self, *, left: bool, right: bool, up: bool, down: bool) -> None:
        speed = 3.2
        self.player_x += (int(right) - int(left)) * speed
        self.player_y += (int(down) - int(up)) * speed
        self.player_x = max(10, min(self.width - 10, self.player_x))
        self.player_y = max(142, min(self.height - 18, self.player_y))

    def _update_bullets(self) -> None:
        next_bullets: list[tuple[float, float, float, float]] = []
        for x, y, vx, vy in self.bullets:
            x += vx
            y += vy
            hit = self._hit_enemy(x, y)
            if not hit and y > -8:
                next_bullets.append((x, y, vx, vy))
        self.bullets = next_bullets
        self.enemy_bullets = [
            (x + vx, y + vy, vx, vy)
            for x, y, vx, vy in self.enemy_bullets
            if -8 <= x <= self.width + 8 and y <= self.height + 8
        ]

    def _hit_enemy(self, x: float, y: float) -> bool:
        for enemy in list(self.enemies):
            if abs(enemy.x - x) <= 10 and abs(enemy.y - y) <= 9:
                enemy.hp -= 1
                if enemy.hp <= 0:
                    self.enemies.remove(enemy)
                    if not self.enemies:
                        self.wave_clear_timer = 24
                    self.score += (200 if enemy.attacking else 100) * enemy.kind
                    self._maybe_drop_cherry(enemy.x, enemy.y)
                    self.message = "alien down"
                return True
        return False

    def _update_enemies(self) -> None:
        direction = 1 if (self.tick_count // 36) % 2 == 0 else -1
        for enemy in self.enemies:
            enemy.x += direction * (0.25 + self.wave * 0.03)
            if self.rng.random() < 0.004 + self.wave * 0.001:
                enemy.attacking = True
                enemy.vx = self._sign(self.player_x - enemy.x) * (0.7 + 0.05 * self.wave)
                enemy.vy = 1.0 + 0.04 * self.wave
            if enemy.attacking:
                enemy.x += enemy.vx
                enemy.y += enemy.vy
                if enemy.y > self.height + 12:
                    enemy.y = 36
                    enemy.attacking = False
            if self.rng.random() < 0.003 + self.wave * 0.001:
                self.enemy_bullets.append((enemy.x, enemy.y + 8, 0.0, 2.2 + self.wave * 0.08))

    def _update_pickups(self) -> None:
        next_pickups: list[tuple[float, float]] = []
        for x, y in self.pickups:
            y += 1.6
            if abs(x - self.player_x) <= 12 and abs(y - self.player_y) <= 12:
                self._collect_cherry()
            elif y < self.height + 8:
                next_pickups.append((x, y))
        self.pickups = next_pickups

    def _collect_cherry(self) -> None:
        self.cherries += 1
        self.score += 25
        if self.cherries >= 10:
            self.cherries = 0
            if self.lives < self.max_lives:
                self.lives += 1
                self.message = "heart restored"
            else:
                self.score += 1000
                self.message = "cherry bonus"
        else:
            self.message = "cherry"

    def _check_player_hits(self) -> None:
        for index, (x, y, vx, vy) in enumerate(list(self.enemy_bullets)):
            if abs(x - self.player_x) <= 8 and abs(y - self.player_y) <= 8:
                del vx, vy
                self.enemy_bullets.pop(index)
                self._damage()
                return
        for enemy in self.enemies:
            if abs(enemy.x - self.player_x) <= 12 and abs(enemy.y - self.player_y) <= 12:
                self._damage()
                enemy.y = -20
                return

    def _damage(self) -> None:
        self.lives -= 1
        self.message = "hit"
        if self.lives <= 0:
            self.game_over = True
            self.message = "game over"

    def _maybe_drop_cherry(self, x: float, y: float, *, force: bool = False) -> None:
        if force or self.rng.random() < 0.22:
            self.pickups.append((x, y))

    @staticmethod
    def _dist(ax: float, ay: float, bx: float, by: float) -> float:
        return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5

    @staticmethod
    def _sign(value: float) -> int:
        return (value > 0) - (value < 0)

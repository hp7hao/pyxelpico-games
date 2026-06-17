"""Pure exploration-platformer rules for the subsurface PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class Explorer:
    x: float = 24.0
    y: float = 156.0
    vx: float = 0.0
    vy: float = 0.0
    grounded: bool = True
    facing: int = 1


class SubsurfaceCore:
    ground_y = 172
    boss_x = 210

    def __init__(self, seed: int = 1) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.player = Explorer()
        self.upgrades = {
            "gun": True,
            "wall_jump": False,
            "double_jump": False,
            "glide": False,
            "swim": False,
            "health_1": False,
            "health_2": False,
        }
        self.max_health = 3
        self.health = self.max_health
        self.energy = 0
        self.room = 0
        self.enemies = [{"x": 82.0, "hp": 1}, {"x": 154.0, "hp": 1}]
        self.bullets: list[dict[str, float]] = []
        self.boss_hp = 8
        self.victory = False
        self.message = "subsurface"
        self.double_jump_ready = True

    def collect_upgrade(self, name: str) -> None:
        if name not in self.upgrades:
            return
        self.upgrades[name] = True
        if name.startswith("health"):
            self.max_health += 1
            self.health = self.max_health
        self.message = f"{name} unlocked"

    def shoot(self) -> bool:
        if self.victory:
            return False
        if not self.upgrades.get("gun", False):
            self.message = "no weapon"
            return False
        self.bullets.append({"x": self.player.x + self.player.facing * 8, "dir": float(self.player.facing)})
        self.message = "shoot"
        return True

    def tick(self, *, move: int = 0, jump: bool = False, hold_jump: bool = False) -> None:
        if self.victory:
            return
        p = self.player
        if move:
            p.facing = 1 if move > 0 else -1
        p.vx += max(-1, min(1, move)) * 0.35
        p.vx *= 0.84
        if jump:
            if p.grounded:
                p.vy = -4.6
                p.grounded = False
                self.double_jump_ready = True
            elif self.upgrades["double_jump"] and self.double_jump_ready:
                p.vy = -4.1
                self.double_jump_ready = False
            elif self.upgrades["wall_jump"] and (p.x <= 10 or p.x >= 230):
                p.vy = -4.0
                p.vx = -p.facing * 2.0
        if hold_jump and self.upgrades["glide"] and p.vy > 0:
            p.vy = min(p.vy, 0.8)
        p.vy += 0.28
        p.vx = max(-2.0, min(2.0, p.vx))
        p.vy = min(4.5, p.vy)
        p.x = max(4.0, min(236.0, p.x + p.vx))
        p.y += p.vy
        if p.y >= self.ground_y:
            p.y = self.ground_y
            p.vy = 0.0
            p.grounded = True
            self.double_jump_ready = True
        else:
            p.grounded = False
        self._water_check()
        self._move_bullets()
        self._check_boss()

    def _water_check(self) -> None:
        p = self.player
        if 102 <= p.x <= 138 and p.y >= 170 and not self.upgrades["swim"]:
            self.health -= 1
            self.message = "need swim"
            p.x = 92
            if self.health <= 0:
                self.health = self.max_health
                p.x, p.y = 24.0, self.ground_y

    def _move_bullets(self) -> None:
        for bullet in self.bullets:
            bullet["x"] += bullet["dir"] * 5.0
        for bullet in list(self.bullets):
            for enemy in list(self.enemies):
                if abs(bullet["x"] - enemy["x"]) < 8:
                    enemy["hp"] -= 1
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if enemy["hp"] <= 0:
                        self.enemies.remove(enemy)
                        self.energy += 1
                        self.message = "enemy down"
                    break
            if bullet in self.bullets and not (0 <= bullet["x"] <= 240):
                self.bullets.remove(bullet)

    def _check_boss(self) -> None:
        if abs(self.player.x - self.boss_x) > 56:
            return
        for bullet in list(self.bullets):
            if bullet["x"] >= self.boss_x - 24:
                self.bullets.remove(bullet)
                self.boss_hp -= 1
                self.message = "boss hit"
                if self.boss_hp <= 0:
                    self.victory = True
                    self.message = "surface reached"

    def restart(self) -> None:
        self.__init__(self.seed)

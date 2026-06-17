"""Pure roguelite-platformer rules for the DUNGEON! PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class Knight:
    x: float = 24.0
    y: float = 166.0
    vx: float = 0.0
    vy: float = 0.0
    grounded: bool = True
    facing: int = 1


class DungeonBangCore:
    ground_y = 172
    portal_x = 220
    final_depth = 8

    def __init__(self, seed: int = 1) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.player = Knight()
        self.depth = 1
        self.zone = "stone"
        self.health = 3
        self.max_health = 3
        self.coins = 0
        self.powerups = {
            "sword": False,
            "bow": False,
            "double_jump": False,
            "green_cape": False,
            "golden_armor": False,
        }
        self.enemies: list[dict[str, float | int | str]] = []
        self.victory = False
        self.game_over = False
        self.message = "dungeon!"
        self.double_jump_ready = True
        self._spawn_room()

    def tick(self, *, move: int = 0, jump: bool = False) -> None:
        if self.victory or self.game_over:
            return
        p = self.player
        if move:
            p.facing = 1 if move > 0 else -1
        if jump:
            if p.grounded:
                p.vy = -4.6
                p.grounded = False
                self.double_jump_ready = True
                self.message = "jump"
            elif (p.x <= 8 or p.x >= 232):
                p.vy = -4.3
                p.vx = 2.2 if p.x <= 8 else -2.2
                self.message = "wall jump"
            elif self.powerups["double_jump"] and self.double_jump_ready:
                p.vy = -3.9
                self.double_jump_ready = False
                self.message = "double jump"
        p.vx += max(-1, min(1, move)) * (0.42 if self.powerups["green_cape"] else 0.32)
        p.vx *= 0.84
        p.vy += 0.28
        p.vx = max(-2.2, min(2.2, p.vx))
        p.vy = min(4.8, p.vy)
        p.x = max(4.0, min(236.0, p.x + p.vx))
        p.y += p.vy
        if p.y >= self.ground_y:
            p.y = self.ground_y
            p.vy = 0.0
            p.grounded = True
            self.double_jump_ready = True
        self._enemy_contact()

    def attack(self) -> bool:
        reach = 30 if self.powerups["bow"] else 16 if self.powerups["sword"] else 10
        damage = 2 if self.powerups["sword"] else 1
        for enemy in list(self.enemies):
            if abs(float(enemy["x"]) - self.player.x) <= reach:
                enemy["hp"] = int(enemy["hp"]) - damage
                if int(enemy["hp"]) <= 0:
                    self.enemies.remove(enemy)
                    self.coins += 2 + self.depth // 2
                    self.message = "monster down"
                else:
                    self.message = "hit"
                return True
        self.message = "swing"
        return False

    def buy_powerup(self, name: str) -> bool:
        costs = {"sword": 5, "bow": 7, "double_jump": 6, "green_cape": 4, "golden_armor": 8}
        if name not in costs or self.powerups.get(name, False) or self.coins < costs[name]:
            self.message = "need coins"
            return False
        self.coins -= costs[name]
        self.powerups[name] = True
        if name == "golden_armor":
            self.max_health += 1
            self.health = self.max_health
        self.message = f"bought {name}"
        return True

    def enter_portal(self) -> bool:
        if abs(self.player.x - self.portal_x) > 14:
            self.message = "find portal"
            return False
        if self.depth >= self.final_depth:
            self.victory = True
            self.message = "princess rescued"
            return True
        self.depth += 1
        self.zone = ["stone", "fire", "crypt", "garden"][(self.depth - 1) % 4]
        self.player.x, self.player.y = 24.0, self.ground_y
        self._spawn_room()
        self.message = f"depth {self.depth}"
        return True

    def _spawn_room(self) -> None:
        count = min(5, 1 + self.depth // 2)
        self.enemies = []
        for index in range(count):
            self.enemies.append({"x": 74.0 + index * 28, "hp": 1 + self.depth // 4, "kind": self.rng.choice(["slime", "bat", "spider"])})

    def _enemy_contact(self) -> None:
        for enemy in self.enemies:
            if abs(float(enemy["x"]) - self.player.x) < 9 and self.player.y >= self.ground_y - 6:
                self.health -= 1
                self.player.x = max(12.0, self.player.x - self.player.facing * 18)
                self.message = f"hit by {enemy['kind']}"
                if self.health <= 0:
                    self.game_over = True
                    self.message = "you died"
                return

    def restart(self) -> None:
        self.__init__(self.seed)

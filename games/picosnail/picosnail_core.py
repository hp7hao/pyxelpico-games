"""Pure platform-adventure rules for the Pico Snail PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class SnailChan:
    x: float = 24.0
    y: float = 168.0
    vx: float = 0.0
    vy: float = 0.0
    grounded: bool = True
    facing: int = 1


class PicoSnailCore:
    ground_y = 172
    warp_x = 222
    max_stars = 5
    boss_level = 6

    def __init__(self, seed: int = 1) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.player = SnailChan()
        self.levels = [
            "garden",
            "courtyard",
            "entrance",
            "halls",
            "rooftops",
            "the moon",
            "nightmare",
            "the end",
        ]
        self.level_index = 0
        self.level_name = self.levels[0]
        self.stars = 0
        self.max_health = 3
        self.health = self.max_health
        self.door_open = False
        self.boss_hp = 6
        self.boss_defeated = False
        self.victory = False
        self.message = "dream castle"
        self.double_jump_ready = False
        self.shots: list[dict[str, float]] = []
        self.enemies: list[dict[str, float | int | str]] = []
        self._spawn_level()

    def collect_star(self) -> bool:
        if self.stars >= self.max_stars:
            self.message = "star pouch full"
            return False
        self.stars += 1
        self.double_jump_ready = True
        self.message = "star found"
        return True

    def tick(self, *, move: int = 0, jump: bool = False, hold_jump: bool = False) -> None:
        if self.victory:
            return
        p = self.player
        if move:
            p.facing = 1 if move > 0 else -1
        p.vx += max(-1, min(1, move)) * 0.28
        p.vx *= 0.84
        if jump:
            if p.grounded:
                p.vy = -4.4
                p.grounded = False
                self.double_jump_ready = self.stars > 0
                self.message = "jump"
            elif self.double_jump_ready and self.stars > 0:
                self.stars -= 1
                self.double_jump_ready = False
                p.vy = -4.1
                self.message = "double jump"
        gravity = 0.22 if self.level_name in ("the moon", "nightmare") else 0.3
        if hold_jump and p.vy < 0:
            p.vy -= 0.04
        p.vy += gravity
        p.vx = max(-1.8, min(1.8, p.vx))
        p.vy = min(4.7, p.vy)
        p.x = max(4.0, min(236.0, p.x + p.vx))
        p.y += p.vy
        if p.y >= self.ground_y:
            p.y = self.ground_y
            p.vy = 0.0
            p.grounded = True
            self.double_jump_ready = self.stars > 0
        self._move_shots()
        self._enemy_contact()

    def cast_wand(self) -> bool:
        if self.stars <= 0:
            self.message = "need stars"
            return False
        self.stars -= 1
        self.shots.append({"x": self.player.x + self.player.facing * 8, "y": self.player.y - 12, "dir": float(self.player.facing)})
        self.message = "star shot"
        return True

    def thwack(self) -> bool:
        for enemy in list(self.enemies):
            if abs(float(enemy["x"]) - self.player.x) <= 18:
                self.enemies.remove(enemy)
                self.collect_star()
                self.message = "dream safe"
                return True
        self.message = "wand swing"
        return False

    def hit_hazard(self, kind: str = "thorn") -> None:
        if self.stars > 0:
            self.stars -= 1
            self.message = f"star blocked {kind}"
            return
        self.health -= 1
        self.message = f"ouch {kind}"
        self.player.x = max(12.0, self.player.x - self.player.facing * 18)
        if self.health <= 0:
            self.health = self.max_health
            self.stars = 0
            self.player.x, self.player.y = 24.0, self.ground_y
            self.message = "wake up again"

    def press_switch(self) -> None:
        self.door_open = True
        self.message = "door opened"

    def enter_warp(self) -> bool:
        if abs(self.player.x - self.warp_x) > 20:
            self.message = "find warp"
            return False
        if self.level_index == self.boss_level:
            if not self.boss_defeated:
                self.message = "cat blocks the dream"
                return False
            self.victory = True
            self.message = "dream castle saved"
            return True
        if self.level_index >= len(self.levels) - 1:
            self.victory = True
            self.message = "dream castle saved"
            return True
        self.level_index += 1
        self.level_name = self.levels[self.level_index]
        self.player.x, self.player.y = 24.0, self.ground_y
        self.door_open = False
        self._spawn_level()
        self.message = self.level_name
        return True

    def attack_boss(self) -> bool:
        if self.level_index != self.boss_level:
            self.message = "no cat here"
            return False
        if not self.door_open:
            self.message = "open the door first"
            return False
        self.boss_hp -= 1
        self.message = "cat bonked"
        if self.boss_hp <= 0:
            self.boss_defeated = True
            self.message = "cat naps"
        return True

    def _spawn_level(self) -> None:
        count = 1 + min(3, self.level_index)
        self.enemies = []
        for index in range(count):
            self.enemies.append({"x": 72.0 + index * 36, "hp": 1, "kind": self.rng.choice(["thorn", "salt", "tar"])})

    def _move_shots(self) -> None:
        for shot in self.shots:
            shot["x"] += shot["dir"] * 5.0
        for shot in list(self.shots):
            for enemy in list(self.enemies):
                if abs(float(enemy["x"]) - shot["x"]) < 8:
                    self.enemies.remove(enemy)
                    self.shots.remove(shot)
                    self.collect_star()
                    self.message = "star burst"
                    break
            if shot in self.shots and not (0 <= shot["x"] <= 240):
                self.shots.remove(shot)

    def _enemy_contact(self) -> None:
        for enemy in self.enemies:
            if abs(float(enemy["x"]) - self.player.x) < 9 and self.player.y >= self.ground_y - 6:
                self.hit_hazard(str(enemy["kind"]))
                return

    def restart(self) -> None:
        self.__init__(self.seed)

"""Pure night-driving shooter rules for the Night Ride PyxelPico port."""

from __future__ import annotations

import random


class NightRideCore:
    lanes = 3
    level_distance = 30
    boss_level = 7

    def __init__(self, seed: int = 1) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.lane = 1
        self.hp = 3
        self.level = 1
        self.distance = 0
        self.score = 0
        self.weapon_unlocked = False
        self.traffic: list[dict[str, object]] = []
        self.bullets: list[dict[str, float]] = []
        self.spawn_delay = 0
        self.boss_hp = 0
        self.game_over = False
        self.victory = False
        self.message = "night ride"

    def tick(self, *, turn: int = 0) -> None:
        if self.game_over or self.victory:
            return
        if turn:
            self.lane = max(0, min(self.lanes - 1, self.lane + turn))
        self.distance += 1
        if self.distance >= self.level_distance and self.level < self.boss_level:
            self.distance = 0
            self.level += 1
            if self.level >= 3:
                self.weapon_unlocked = True
            self.message = f"level {self.level}"
        if self.level >= self.boss_level and self.boss_hp <= 0:
            self.start_boss()
        self._spawn_traffic()
        self._move_bullets()
        self._move_traffic()
        self._check_collisions()

    def shoot(self) -> bool:
        if not self.weapon_unlocked and self.boss_hp <= 0:
            self.message = "no weapon"
            return False
        if self.boss_hp > 0:
            self.boss_hp -= 1
            self.score += 150
            self.message = "boss hit"
            if self.boss_hp <= 0:
                self.victory = True
                self.message = "sunrise"
            return True
        self.bullets.append({"lane": float(self.lane), "y": 0.86})
        self.message = "shoot"
        return True

    def start_boss(self) -> None:
        self.boss_hp = 5
        self.weapon_unlocked = True
        self.message = "boss"

    def _spawn_traffic(self) -> None:
        if self.spawn_delay > 0:
            self.spawn_delay -= 1
            return
        if self.boss_hp > 0 or self.bullets:
            return
        if len(self.traffic) < 4 and self.rng.random() < 0.16 + self.level * 0.015:
            lane = self.rng.randrange(self.lanes)
            kind = "bike" if self.level >= 3 and self.rng.random() < 0.25 else "car"
            self.traffic.append({"lane": lane, "y": -0.1, "kind": kind})

    def _move_bullets(self) -> None:
        for bullet in self.bullets:
            bullet["y"] -= 0.12
        self.bullets = [bullet for bullet in self.bullets if bullet["y"] > -0.1]

    def _move_traffic(self) -> None:
        speed = 0.08 + self.level * 0.004
        for car in self.traffic:
            car["y"] = float(car["y"]) + speed
        self.traffic = [car for car in self.traffic if float(car["y"]) < 1.2]

    def _check_collisions(self) -> None:
        for bullet in list(self.bullets):
            if self.boss_hp > 0 and float(bullet["y"]) < 0.2:
                self.bullets.remove(bullet)
                self.boss_hp -= 1
                self.score += 150
                self.message = "boss hit"
                if self.boss_hp <= 0:
                    self.victory = True
                    self.message = "sunrise"
                continue
            for car in list(self.traffic):
                if int(car["lane"]) == int(bullet["lane"]) and abs(float(car["y"]) - float(bullet["y"])) < 0.12:
                    self.traffic.remove(car)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    self.score += 100
                    self.spawn_delay = 12
                    self.message = "clear"
                    break
        for car in list(self.traffic):
            if int(car["lane"]) == self.lane and float(car["y"]) >= 0.9:
                self.traffic.remove(car)
                self.hp -= 1
                self.message = "crash"
                if self.hp <= 0:
                    self.game_over = True
                    self.message = "wrecked"

    def restart(self) -> None:
        self.__init__(self.seed)

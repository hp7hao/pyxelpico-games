"""Pure racing rules for the Brutal Pico Race PyxelPico port."""

from __future__ import annotations

import math
import random


SHIP_CLASSES = {
    "heavy": {"accel": 0.040, "max_speed": 2.7, "health": 130, "turn": 0.045},
    "normal": {"accel": 0.050, "max_speed": 3.0, "health": 100, "turn": 0.055},
    "light": {"accel": 0.063, "max_speed": 3.35, "health": 75, "turn": 0.068},
}


class BrutalPicoRaceCore:
    def __init__(self, seed: int = 1, ship_class: str = "normal") -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.ship_class = ship_class if ship_class in SHIP_CLASSES else "normal"
        self.stats = SHIP_CLASSES[self.ship_class]
        self.position_x = 0.0
        self.progress = 0.0
        self.speed = 0.0
        self.boost_meter = 100.0
        self.health = int(self.stats["health"])
        self.lap = 0
        self.laps_required = 3
        self.track_length = 120.0
        self.finished = False
        self.race_time = 0
        self.rank = 1
        self.message = self.ship_class
        self.ai_progress = [0.0, -5.0, -10.0]
        self.ai_speed = [2.15, 2.0, 1.9]

    def tick(self, *, steer: int = 0, accel: bool = False, brake: bool = False, boost: bool = False) -> None:
        if self.finished or self.health <= 0:
            return
        self.race_time += 1
        if accel:
            self.speed += float(self.stats["accel"])
        if brake:
            self.speed -= 0.08
        if boost and self.boost_meter > 0:
            self.speed += 0.12
            self.boost_meter = max(0.0, self.boost_meter - 2.4)
            self.message = "boost"
        else:
            self.boost_meter = min(100.0, self.boost_meter + 0.25)
        self.speed *= 0.992
        self.speed = max(0.0, min(float(self.stats["max_speed"]), self.speed))
        curve = math.sin((self.progress / self.track_length) * math.tau * 2.0) * 0.018
        self.position_x += steer * float(self.stats["turn"]) + curve * self.speed
        if abs(self.position_x) > 1.0:
            self.health -= 2
            self.speed *= 0.72
            self.position_x = max(-1.05, min(1.05, self.position_x))
            self.message = "wall hit"
        self._apply_drafting()
        self.progress += self.speed
        self._update_laps()
        self._update_ai()
        self._update_rank()

    def cycle_ship(self) -> None:
        order = ["heavy", "normal", "light"]
        next_index = (order.index(self.ship_class) + 1) % len(order)
        self.__init__(self.seed, order[next_index])

    def _apply_drafting(self) -> None:
        for ai in self.ai_progress:
            gap = ai - self.progress
            if 1.0 < gap < 9.0 and abs(self.position_x) < 0.35:
                self.speed = min(float(self.stats["max_speed"]), self.speed + 0.035)
                self.message = "draft"

    def _update_laps(self) -> None:
        while self.progress >= self.track_length:
            self.progress -= self.track_length
            self.lap += 1
            self.message = f"lap {self.lap}"
            if self.lap >= self.laps_required:
                self.finished = True
                self.message = "finish"
                break

    def _update_ai(self) -> None:
        for index, speed in enumerate(self.ai_speed):
            wobble = math.sin((self.race_time + index * 23) * 0.04) * 0.03
            self.ai_progress[index] += speed + wobble
            if self.ai_progress[index] >= self.track_length * self.laps_required:
                self.ai_progress[index] = self.track_length * self.laps_required

    def _update_rank(self) -> None:
        player_total = self.lap * self.track_length + self.progress
        self.rank = 1 + sum(1 for ai in self.ai_progress if ai > player_total)

    def restart(self) -> None:
        self.__init__(self.seed, self.ship_class)

"""Pure train-sim rules for the Cab Ride PyxelPico port."""

from __future__ import annotations

import random


class CabRideCore:
    def __init__(self, seed: int = 1) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.speed = 0.0
        self.throttle_level = 0
        self.distance = 0.0
        self.distance_to_station = self._next_station_distance()
        self.station_index = 1
        self.doors_open = False
        self.passengers = 0
        self.waiting_passengers = 5
        self.total_score = 0
        self.rating = "depart"
        self.status = "drive forever"
        self.express_mode = False
        self.last_station_announced = False
        self.journey_over = False
        self.horn_timer = 0
        self.weather = "clear"
        self.scenery_seed = self.rng.randrange(9999)

    def tick(self, *, throttle: int = 0) -> None:
        if self.journey_over:
            return
        if self.doors_open:
            self.speed = 0.0
            self.status = "doors open"
            return
        if self.express_mode and throttle == 0:
            throttle = 1
        self.throttle_level = max(-3, min(3, self.throttle_level + throttle))
        accel = self.throttle_level * 0.0065
        drag = 0.004 + self.speed * 0.01
        self.speed = max(0.0, min(1.2, self.speed + accel - drag))
        moved = self.speed * 0.025
        self.distance += moved
        self.distance_to_station -= moved
        if self.distance_to_station < -0.25:
            self._pass_station()
        if self.horn_timer > 0:
            self.horn_timer -= 1
        if self.rng.random() < 0.003:
            self.weather = self.rng.choice(["clear", "clouds", "rain"])
        self.status = self._approach_status()

    def horn(self) -> None:
        self.horn_timer = 18
        self.status = "horn"

    def toggle_express(self) -> bool:
        self.express_mode = not self.express_mode
        self.status = "express" if self.express_mode else "local"
        return self.express_mode

    def announce_last_station(self) -> None:
        self.last_station_announced = True
        self.status = "last station"

    def toggle_doors(self) -> str:
        if self.doors_open:
            self.doors_open = False
            self.status = "depart"
            self._prepare_next_station()
            return "depart"
        if self.speed > 0.05:
            self.status = "stop first"
            return self.status
        if abs(self.distance_to_station) > 0.08:
            self.status = "not at signal"
            return self.status
        self.doors_open = True
        self.rating = self._rating_for_stop(abs(self.distance_to_station))
        disembark = min(self.passengers, self.rng.randint(0, 3))
        board = min(self.waiting_passengers, self.rng.randint(1, 4))
        self.passengers += board - disembark
        self.waiting_passengers -= board
        self.total_score += {"great stop": 120, "good stop": 75, "rough stop": 35}[self.rating]
        self.total_score += board * 12 + disembark * 8
        self.status = self.rating
        if self.last_station_announced:
            self.journey_over = True
            self.status = "journey complete"
        return self.status

    def _rating_for_stop(self, miss: float) -> str:
        if miss <= 0.025:
            return "great stop"
        if miss <= 0.055:
            return "good stop"
        return "rough stop"

    def _pass_station(self) -> None:
        self.rating = "missed stop"
        self.total_score = max(0, self.total_score - 30)
        self.status = "missed stop"
        self._prepare_next_station()

    def _prepare_next_station(self) -> None:
        self.station_index += 1
        self.distance_to_station = self._next_station_distance()
        self.waiting_passengers = 3 + self.rng.randrange(7)
        self.scenery_seed = self.rng.randrange(9999)

    def _next_station_distance(self) -> float:
        return 1.8 + self.rng.random() * 1.2

    def _approach_status(self) -> str:
        if self.distance_to_station < 0.18:
            return "station now"
        if self.distance_to_station < 0.55:
            return "brake soon"
        if self.express_mode:
            return "express"
        return "rolling"

    def restart(self) -> None:
        self.__init__(self.seed)

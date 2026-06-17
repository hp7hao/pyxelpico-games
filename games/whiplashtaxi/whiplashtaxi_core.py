"""Pure taxi delivery rules for the Whiplash Taxi Co PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import math
import random


@dataclass
class Passenger:
    pickup: tuple[float, float]
    destination: tuple[float, float]
    aboard: bool = False
    delivered: bool = False


class WhiplashTaxiCore:
    width = 240
    height = 240
    shift_seconds = 300.0

    def __init__(self, seed: int = 1) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.x = 120.0
        self.y = 120.0
        self.heading = -math.pi / 2
        self.speed = 0.0
        self.money = 0
        self.deliveries = 0
        self.time_left = self.shift_seconds
        self.shift_over = False
        self.message = "pick up fares"
        self.passengers = [
            Passenger((58.0, 52.0), (184.0, 64.0)),
            Passenger((196.0, 178.0), (42.0, 188.0)),
            Passenger((52.0, 172.0), (182.0, 196.0)),
            Passenger((184.0, 42.0), (74.0, 116.0)),
        ]
        self.current_passenger: Passenger | None = None
        self.next_index = 0

    def tick(self, *, accel: bool = False, reverse: bool = False, turn: int = 0) -> None:
        if self.shift_over:
            return
        self.time_left = max(0.0, self.time_left - 1 / 30)
        if self.time_left <= 0:
            self.shift_over = True
            self.speed = 0.0
            self.message = "shift over"
            return
        if accel:
            if self.speed < 0:
                self.speed = 0.0
            else:
                self.speed += 0.18
        if reverse:
            if self.speed > 0:
                self.speed = 0.0
            else:
                self.speed -= 0.12
        self.speed *= 0.985
        self.speed = max(-2.0, min(4.8, self.speed))
        self.heading += turn * (0.025 + abs(self.speed) * 0.008)
        self.x += math.cos(self.heading) * self.speed
        self.y += math.sin(self.heading) * self.speed
        bounced = False
        if self.x < 14 or self.x > self.width - 14:
            self.x = max(14, min(self.width - 14, self.x))
            bounced = True
        if self.y < 14 or self.y > self.height - 14:
            self.y = max(14, min(self.height - 14, self.y))
            bounced = True
        if bounced:
            self.speed *= -0.25
            self.message = "crash"
        self.try_pickup()
        self.try_dropoff()

    def try_pickup(self) -> bool:
        if self.current_passenger is not None or abs(self.speed) > 0.2:
            return False
        passenger = self.active_passenger()
        if passenger is None or self.distance((self.x, self.y), passenger.pickup) > 12:
            return False
        passenger.aboard = True
        self.current_passenger = passenger
        self.message = "passenger aboard"
        return True

    def try_dropoff(self) -> bool:
        passenger = self.current_passenger
        if passenger is None or abs(self.speed) > 0.3:
            return False
        if self.distance((self.x, self.y), passenger.destination) > 14:
            return False
        passenger.delivered = True
        passenger.aboard = False
        self.current_passenger = None
        self.deliveries += 1
        bonus = max(0, int(self.time_left // 30))
        self.money += 25 + bonus
        self.next_index = (self.next_index + 1) % len(self.passengers)
        self.message = "+$" + str(25 + bonus)
        return True

    def active_passenger(self) -> Passenger | None:
        if self.current_passenger is not None:
            return self.current_passenger
        for offset in range(len(self.passengers)):
            passenger = self.passengers[(self.next_index + offset) % len(self.passengers)]
            if not passenger.delivered:
                return passenger
        for passenger in self.passengers:
            passenger.delivered = False
        self.next_index = 0
        return self.passengers[0]

    def target(self) -> tuple[float, float]:
        passenger = self.active_passenger()
        if passenger is None:
            return self.x, self.y
        return passenger.destination if passenger.aboard else passenger.pickup

    @staticmethod
    def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def restart(self) -> None:
        self.__init__(self.seed)

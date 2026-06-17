"""Pure racing rules for the Pico World Race PyxelPico port."""

from __future__ import annotations

import random


class PicoWorldRaceCore:
    track_length = 360.0
    total_laps = 3

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.speed = 0.0
        self.max_speed = 4.8
        self.lane = 0.0
        self.progress = 0.0
        self.lap = 1
        self.frame = 0
        self.score = 0
        self.tokens_collected = 0
        self.finished = False
        self.crashed = False
        self.accel = False
        self.steer = 0
        self.drift = False
        self.tokens = [18.0 + i * 16.5 for i in range(20)]
        self.seen_tokens: set[int] = set()
        self.opponents = [0.0, -18.0, -36.0]
        self.opponent_speeds = [3.0, 2.8, 2.65]

    def reset(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

    def input(self, accel: bool, steer: int, drift: bool) -> None:
        self.accel = accel
        self.steer = max(-1, min(1, steer))
        self.drift = drift

    def tick(self) -> None:
        if self.finished:
            return
        self.frame += 1
        if self.accel:
            self.speed = min(self.max_speed, self.speed + 0.18)
        else:
            self.speed = max(0.0, self.speed - 0.12)

        turn_gain = 0.075 if not self.drift else 0.13
        self.lane += self.steer * turn_gain * max(0.8, self.speed)
        self.lane *= 0.94
        if self.drift and self.steer:
            self.speed *= 0.96
        if abs(self.lane) > 1.25:
            self.speed *= 0.82
            self.crashed = True
        else:
            self.crashed = False

        old_progress = self.progress
        self.progress += self.speed
        self._collect_tokens(old_progress, self.progress)
        self._update_opponents()
        if self.progress >= self.track_length:
            self.progress -= self.track_length
            if self.lap >= self.total_laps:
                self.finished = True
                self.score += 50 + self.tokens_collected
            else:
                self.lap += 1

    def standing(self) -> int:
        player_total = (self.lap - 1) * self.track_length + self.progress
        ahead = sum(1 for opp in self.opponents if opp > player_total)
        return ahead + 1

    def _collect_tokens(self, old: float, new: float) -> None:
        for index, token in enumerate(self.tokens):
            if index in self.seen_tokens:
                continue
            if old <= token <= new:
                self.seen_tokens.add(index)
                self.tokens_collected += 1
                self.score += 5

    def _update_opponents(self) -> None:
        for index, speed in enumerate(self.opponent_speeds):
            self.opponents[index] += speed

"""Pure racing rules for the PICORACER-2048 PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class Racer:
    segment: float = 0.0
    lane: float = 0.0
    speed: float = 0.0
    class_index: int = 1


class Picoracer2048Core:
    laps_to_win = 3
    speed_classes = (2.2, 2.9, 3.6, 4.3)
    accel = 0.08
    drag = 0.985
    brake_drag = 0.88
    steer_rate = 0.07
    airbrake_steer = 0.06
    curve_push = 0.035

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.track: list[tuple[int, float, float]] = [
            (30, 0.00, 1.15),
            (24, 0.35, 1.05),
            (20, -0.42, 0.95),
            (18, 0.00, 0.78),
            (26, 0.48, 0.88),
            (30, -0.24, 1.05),
            (22, 0.00, 1.20),
            (16, -0.50, 0.82),
        ]
        self.boost_pads: dict[int, int] = {22: 18, 89: 20, 142: 18}
        self.rebuild_track()
        self.player = Racer(class_index=1)
        self.ai = Racer(segment=-8.0, lane=0.15, speed=1.7, class_index=1)
        self.lap = 0
        self.time = 0
        self.finish_time = 0
        self.finished = False
        self.wall_hits = 0
        self.position = 1
        self.message = "ready"

    def rebuild_track(self) -> None:
        self.segments: list[tuple[float, float]] = []
        for length, curve, width in self.track:
            for _ in range(length):
                self.segments.append((curve, width))
        self.track_length = max(1, len(self.segments))

    def tick(
        self,
        *,
        accelerate: bool = False,
        brake: bool = False,
        left: bool = False,
        right: bool = False,
        class_up: bool = False,
        class_down: bool = False,
    ) -> None:
        if self.finished:
            return
        if class_up:
            self.player.class_index = min(3, self.player.class_index + 1)
            self.message = f"class {self.player.class_index + 1}"
        elif class_down:
            self.player.class_index = max(0, self.player.class_index - 1)
            self.message = f"class {self.player.class_index + 1}"

        self.time += 1
        previous_segment = self.player.segment
        self._update_racer(self.player, accelerate=accelerate, brake=brake, left=left, right=right, is_player=True)
        self._update_ai()
        self._update_lap(previous_segment)
        self.position = 1 if self.player.segment >= self.ai.segment else 2

    def _update_racer(
        self,
        racer: Racer,
        *,
        accelerate: bool,
        brake: bool,
        left: bool,
        right: bool,
        is_player: bool,
    ) -> None:
        max_speed = self.speed_classes[racer.class_index]
        if accelerate:
            racer.speed += self.accel * (1.0 + racer.class_index * 0.18)
        if brake:
            racer.speed *= self.brake_drag
        racer.speed *= self.drag
        racer.speed = max(0.0, min(max_speed, racer.speed))

        segment_index = int(racer.segment) % self.track_length
        curve, width = self.segments[segment_index]
        steer = int(right) - int(left)
        steer_power = self.steer_rate + (self.airbrake_steer if brake else 0.0)
        racer.lane += steer * steer_power * (0.6 + racer.speed / max_speed)
        racer.lane += curve * self.curve_push * (0.5 + racer.speed)

        if is_player and segment_index in self.boost_pads and abs(racer.lane) < 0.28:
            racer.speed = min(max_speed + 0.55, racer.speed + self.boost_pads[segment_index] / 90)
            self.message = "boost"

        if abs(racer.lane) > width:
            overshoot = abs(racer.lane) - width
            racer.lane = width * (1 if racer.lane > 0 else -1)
            racer.speed *= max(0.35, 0.72 - overshoot * 0.22)
            if is_player:
                self.wall_hits += 1
                self.message = "wall hit"
        elif is_player and self.message == "wall hit":
            self.message = "racing"

        racer.segment += racer.speed

    def _update_ai(self) -> None:
        index = int(self.ai.segment) % self.track_length
        curve, _width = self.segments[index]
        desired_lane = -curve * 0.35
        left = self.ai.lane > desired_lane + 0.04
        right = self.ai.lane < desired_lane - 0.04
        brake = abs(curve) > 0.42 and self.ai.speed > 2.0
        self._update_racer(self.ai, accelerate=True, brake=brake, left=left, right=right, is_player=False)

    def _update_lap(self, previous_segment: float) -> None:
        previous_lap = int(previous_segment // self.track_length)
        current_lap = int(self.player.segment // self.track_length)
        if current_lap > previous_lap:
            self.lap = min(current_lap, self.laps_to_win)
            self.message = f"lap {self.lap}"
        if self.lap >= self.laps_to_win:
            self.finished = True
            self.finish_time = self.time
            self.message = "finished"

    def current_curve(self) -> float:
        return self.segments[int(self.player.segment) % self.track_length][0]

    def current_width(self) -> float:
        return self.segments[int(self.player.segment) % self.track_length][1]

    def progress_ratio(self) -> float:
        return (self.player.segment % self.track_length) / self.track_length

    def restart(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

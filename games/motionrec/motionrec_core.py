"""Pure motion-recording platform rules for the MOTION REC PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class Actor:
    x: float
    y: float
    dx: float = 0.0
    dy: float = 0.0
    facing: int = 1
    on_ground: bool = True


class MotionRecCore:
    floor_y = 164.0
    gravity = 0.35
    accel = 0.45
    friction = 0.78
    max_dx = 2.8
    jump_speed = -6.3
    max_record_frames = 96

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.spawn_x = 28.0
        self.spawn_y = self.floor_y
        self.switch_x = 142.0
        self.goal_x = 204.0
        self.player = Actor(self.spawn_x, self.spawn_y)
        self.clone = Actor(self.spawn_x, self.spawn_y)
        self.mode = "play"
        self.recorded_path: list[tuple[float, float]] = []
        self._record_origin = (self.spawn_x, self.spawn_y)
        self._playback_origin = (self.spawn_x, self.spawn_y)
        self._playback_path: list[tuple[float, float]] = []
        self._playback_index = 0
        self.switch_active = False
        self.goal_locked = True
        self.cleared = False
        self.message = "record motion"

    def tick(
        self,
        *,
        left: bool = False,
        right: bool = False,
        jump: bool = False,
    ) -> None:
        if self.cleared:
            return
        if self.mode == "playback":
            self._update_playback()
        else:
            self._update_player(left=left, right=right, jump=jump)
            if self.mode == "record":
                self._append_record_frame()
        self._update_switch_and_goal()

    def start_recording(self) -> None:
        self.mode = "record"
        self.recorded_path = []
        self._record_origin = (self.player.x, self.player.y)
        self._append_record_frame()
        self.message = "recording"

    def stop_recording(self) -> None:
        if self.mode == "record":
            self.mode = "play"
            self.message = "motion stored"

    def start_playback(self, *, reverse: bool = False) -> bool:
        if not self.recorded_path:
            self.message = "no motion recorded"
            return False
        self.mode = "playback"
        self._playback_origin = (self.player.x, self.player.y)
        if reverse:
            self._playback_path = [(-x, -y) for x, y in self.recorded_path]
        else:
            self._playback_path = list(self.recorded_path)
        self._playback_index = 0
        self.message = "reverse replay" if reverse else "replay motion"
        return True

    def restart_level(self) -> None:
        self.player = Actor(self.spawn_x, self.spawn_y)
        self.clone = Actor(self.spawn_x, self.spawn_y)
        self.mode = "play"
        self.recorded_path = []
        self._playback_path = []
        self._playback_index = 0
        self.switch_active = False
        self.goal_locked = True
        self.cleared = False
        self.message = "record cleared"

    def _update_player(self, *, left: bool, right: bool, jump: bool) -> None:
        move = int(right) - int(left)
        if move:
            self.player.dx += move * self.accel
            self.player.dx = max(-self.max_dx, min(self.max_dx, self.player.dx))
            self.player.facing = move
        else:
            self.player.dx *= self.friction
            if abs(self.player.dx) < 0.04:
                self.player.dx = 0.0
        if jump and self.player.on_ground:
            self.player.dy = self.jump_speed
            self.player.on_ground = False
            self.message = "jump"
        self.player.dy = min(5.8, self.player.dy + self.gravity)
        self.player.x = max(6, min(228, self.player.x + self.player.dx))
        self.player.y += self.player.dy
        if self.player.y >= self.floor_y:
            self.player.y = self.floor_y
            self.player.dy = 0.0
            self.player.on_ground = True

    def _append_record_frame(self) -> None:
        if len(self.recorded_path) >= self.max_record_frames:
            self.stop_recording()
            return
        ox, oy = self._record_origin
        self.recorded_path.append((round(self.player.x - ox, 3), round(self.player.y - oy, 3)))

    def _update_playback(self) -> None:
        if self._playback_index >= len(self._playback_path):
            self.mode = "play"
            self.message = "motion complete"
            return
        ox, oy = self._playback_origin
        px, py = self._playback_path[self._playback_index]
        self.player.x = ox + px
        self.player.y = oy + py
        self.player.on_ground = self.player.y >= self.floor_y
        self.clone.x = self.player.x
        self.clone.y = self.player.y
        self._playback_index += 1
        if self._playback_index >= len(self._playback_path):
            self.mode = "play"
            self.message = "motion complete"

    def _update_switch_and_goal(self) -> None:
        self.switch_active = abs(self.clone.x - self.switch_x) <= 8 or abs(self.player.x - self.switch_x) <= 8
        self.goal_locked = not self.switch_active
        if not self.goal_locked and abs(self.player.x - self.goal_x) <= 8 and self.player.on_ground:
            self.cleared = True
            self.message = "motion solved"

    @property
    def recording_ratio(self) -> float:
        return min(1.0, len(self.recorded_path) / self.max_record_frames)

    def replay_ghost_points(self) -> list[tuple[float, float]]:
        ox, oy = self.player.x, self.player.y
        return [(ox + px, oy + py) for px, py in self.recorded_path[:: max(1, len(self.recorded_path) // 12 or 1)]]

"""Pure platformer-starter-kit rules for the Advanced Micro Platformer port."""

from __future__ import annotations

import random


class AdvancedMicroPlatformerCore:
    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.spawn_x = 36.0
        self.spawn_y = 144.0
        self.player_x = self.spawn_x
        self.player_y = self.spawn_y
        self.vx = 0.0
        self.vy = 0.0
        self.facing = 1
        self.on_ground = True
        self.coyote_timer = 6
        self.jump_buffer = 0
        self.jump_hold_timer = 0
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.goal_x = 360.0
        self.goal_y = 146.0
        self.level_clear = False
        self.message = "starter kit demo"
        self.solid_rects = [
            (0, 160, 430, 24),
            (0, 96, 100, 16),
            (214, 132, 58, 14),
            (306, 116, 88, 14),
        ]
        self.one_way_rects = [(122, 112, 72, 8)]

    def press_jump(self) -> bool:
        self.jump_buffer = 14
        if self.on_ground or self.coyote_timer > 0:
            self._start_jump()
            return True
        return False

    def tick(
        self,
        *,
        left: bool = False,
        right: bool = False,
        jump_held: bool = False,
    ) -> None:
        if self.level_clear:
            return
        if self.jump_buffer > 0:
            self.jump_buffer -= 1
        if self.on_ground:
            self.coyote_timer = 6
        elif self.coyote_timer > 0:
            self.coyote_timer -= 1

        move = int(right) - int(left)
        if move:
            self.vx += move * 0.48
            self.facing = move
        else:
            self.vx *= 0.76 if self.on_ground else 0.9
        self.vx = max(-3.0, min(3.0, self.vx))

        if jump_held and self.jump_hold_timer > 0 and self.vy < 0:
            self.vy -= 0.42
            self.jump_hold_timer -= 1
        else:
            self.jump_hold_timer = 0
        self.vy = min(6.5, self.vy + 0.35)

        self._move_x(self.vx)
        was_airborne = not self.on_ground
        self.on_ground = False
        self._move_y(self.vy)
        if self.on_ground and was_airborne and self.jump_buffer > 0:
            self._start_jump()

        self._update_camera()
        if abs(self.player_x - self.goal_x) <= 12 and abs(self.player_y - self.goal_y) <= 18:
            self.level_clear = True
            self.message = "demo complete"

    def restart(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

    def _start_jump(self) -> None:
        self.vy = -5.7
        self.on_ground = False
        self.coyote_timer = 0
        self.jump_buffer = 0
        self.jump_hold_timer = 9
        self.message = "jump"

    def _move_x(self, dx: float) -> None:
        self.player_x += dx
        if self._collides_solid(self.player_x, self.player_y):
            step = -1 if dx > 0 else 1
            while self._collides_solid(self.player_x, self.player_y):
                self.player_x += step
            self.vx = 0

    def _move_y(self, dy: float) -> None:
        prev_y = self.player_y
        self.player_y += dy
        if dy >= 0:
            platform_y = self._landing_y(prev_y, self.player_y)
            if platform_y is not None:
                self.player_y = platform_y - 14
                self.vy = 0
                self.on_ground = True
                self.message = "land"
                return
        if self._collides_solid(self.player_x, self.player_y):
            step = -1 if dy > 0 else 1
            while self._collides_solid(self.player_x, self.player_y):
                self.player_y += step
            if dy > 0:
                self.on_ground = True
                if self.jump_buffer == 0:
                    self.message = "land"
            self.vy = 0

    def _landing_y(self, prev_y: float, next_y: float) -> float | None:
        foot_prev = prev_y + 14
        foot_next = next_y + 14
        for x, y, w, _ in self.one_way_rects:
            if foot_prev <= y <= foot_next and x - 7 <= self.player_x <= x + w + 7:
                return y
        return None

    def _collides_solid(self, x: float, y: float) -> bool:
        left, right = x - 6, x + 6
        top, bottom = y - 14, y + 14
        for rx, ry, rw, rh in self.solid_rects:
            if left < rx + rw and right > rx and top < ry + rh and bottom > ry:
                return True
        return False

    def _update_camera(self) -> None:
        min_x = self.camera_x + 84
        max_x = self.camera_x + 156
        if self.player_x < min_x:
            self.camera_x = max(0, self.player_x - 84)
        elif self.player_x > max_x:
            self.camera_x = min(210, self.player_x - 156)

    def visible_rects(self) -> list[tuple[int, int, int, int, str]]:
        rects = [(int(x - self.camera_x), y, w, h, "solid") for x, y, w, h in self.solid_rects]
        rects += [(int(x - self.camera_x), y, w, h, "one_way") for x, y, w, h in self.one_way_rects]
        return rects

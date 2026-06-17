"""Pure vector-platformer rules for the Starjump PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class Star:
    x: float = 30.0
    y: float = 174.0
    vx: float = 0.0
    vy: float = 0.0
    grounded: bool = True


@dataclass
class Platform:
    x: float
    y: float
    w: float
    color: str = "white"
    breakable: bool = False
    active: bool = True


class StarjumpCore:
    ground_y = 188
    cannon_x = 196.0
    cannon_y = 168.0
    goal_x = 218.0
    goal_y = 156.0
    final_stage = 4

    def __init__(self, seed: int = 1) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.player = Star()
        self.stage = 1
        self.timer = 0
        self.wobble = 1.0
        self.show_timer = True
        self.solid_color = "white"
        self.air_jumps = 0
        self.finished = False
        self.launching = 0
        self.message = "starjump"
        self.platforms: list[Platform] = []
        self._build_stage()

    def grant_jump_charge(self) -> None:
        self.air_jumps = min(2, self.air_jumps + 1)
        self.message = f"jump x{self.air_jumps + 1}"

    def jump(self) -> bool:
        if self.finished:
            return False
        if self.player.grounded:
            self.player.vy = -5.0
            self.player.grounded = False
            self.message = "jump"
            return True
        if self.air_jumps > 0:
            self.air_jumps -= 1
            self.player.vy = -4.6
            self.message = "double jump" if self.air_jumps == 1 else "triple jump"
            return True
        self.message = "no jump"
        return False

    def toggle_color(self) -> None:
        self.solid_color = "pink" if self.solid_color == "white" else "white"
        self.message = f"{self.solid_color} solid"

    def use_cannon(self) -> bool:
        if abs(self.player.x - self.cannon_x) > 18 or abs(self.player.y - self.cannon_y) > 28:
            self.message = "find cannon"
            return False
        self.launching = 14
        self.player.vx = 3.2
        self.player.vy = -4.8
        self.player.grounded = False
        self.message = "red balloon"
        return True

    def tick(self, *, move: int = 0) -> None:
        if self.finished:
            self.timer += 1
            return
        self.timer += 1
        p = self.player
        if self.launching > 0:
            self.launching -= 1
            p.vx = max(p.vx, 2.4)
        else:
            p.vx += max(-1, min(1, move)) * 0.32
        p.vx *= 0.9
        p.vy += 0.28
        p.vx = max(-2.4, min(2.8, p.vx))
        p.vy = min(5.0, p.vy)
        p.x = max(8.0, min(232.0, p.x + p.vx))
        p.y += p.vy
        self._platform_collision()
        if p.y >= self.ground_y:
            p.y = self.ground_y
            p.vy = 0.0
            p.grounded = True
            self.air_jumps = max(self.air_jumps, 1 if self.stage >= 2 else 0)
        if self.launching == 0 and p.x >= 224 and self.stage < self.final_stage:
            self.advance_stage()
        if self.stage >= self.final_stage and abs(p.x - self.goal_x) < 16 and abs(p.y - self.goal_y) < 42:
            self.finished = True
            self.message = "back to the beginning"

    def advance_stage(self) -> None:
        self.stage += 1
        self.player.x = 24.0
        self.player.y = 174.0
        self.player.vx = 0.0
        self.player.vy = 0.0
        self.player.grounded = True
        self.air_jumps = min(2, self.stage - 1)
        self._build_stage()
        self.message = f"stage {self.stage}"

    def _build_stage(self) -> None:
        self.platforms = [
            Platform(50, 164, 54, "white"),
            Platform(104, 144, 36, "white", breakable=True),
            Platform(150, 124, 44, "white"),
            Platform(196, 168, 32, "pink"),
        ]
        if self.stage >= 3:
            self.platforms.append(Platform(76, 116, 28, "pink", breakable=True))
            self.platforms.append(Platform(132, 94, 34, "white"))
        if self.stage >= self.final_stage:
            self.platforms.append(Platform(self.goal_x, self.goal_y + 18, 40, self.solid_color))

    def _platform_collision(self) -> None:
        p = self.player
        if p.vy < 0:
            return
        for platform in self.platforms:
            if not platform.active or platform.color != self.solid_color:
                continue
            if abs(p.x - platform.x) <= platform.w / 2 and platform.y - 4 <= p.y <= platform.y + 8:
                p.y = platform.y - 4
                p.vy = -4.2 if platform.breakable else 0.0
                p.grounded = not platform.breakable
                self.air_jumps = max(self.air_jumps, 2 if self.stage >= 3 else 1 if self.stage >= 2 else 0)
                if platform.breakable:
                    platform.active = False
                    self.message = "break jump"
                else:
                    self.message = "land"
                return

    def restart(self) -> None:
        self.__init__(self.seed)

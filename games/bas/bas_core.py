"""Pure endless wall-jump rules for the BAS PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass, field
import random


@dataclass
class Saw:
    tile: int
    right_wall: bool


@dataclass
class Player:
    tile_pos: int = 20
    y: float = 20.0
    x: float = 188.0
    right_wall: bool = True
    target_right_wall: bool = True
    jumping: bool = False
    jump_t: int = 0
    jump_duration: int = 10
    start_x: float = 188.0
    target_x: float = 36.0


@dataclass
class Columns:
    saws: list[Saw] = field(default_factory=list)
    next_spawn_tile: int = 17


class BasCore:
    left_x = 36.0
    right_x = 188.0
    tile_height = 18

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.player = Player(y=20 * self.tile_height)
        self.columns = Columns()
        self.state = "initial"
        self.score = 0
        self.highscore = 0
        self.camera_y = self.player.y - 132
        self.trap_y = self.player.y + 180
        self.message = "jump left or right"

    def jump(self, right_wall: bool) -> bool:
        if self.state == "dead":
            return False
        if self.state == "initial":
            self.state = "playing"
        self.player.start_x = self.player.x
        self.player.target_x = self.right_x if right_wall else self.left_x
        self.player.target_right_wall = right_wall
        self.player.jumping = True
        self.player.jump_t = 0
        if self.will_collide(right_wall):
            self.state = "will_die"
        self.message = "jump right" if right_wall else "jump left"
        return True

    def tick(self, frames: int = 1) -> None:
        for _ in range(frames):
            if self.state == "dead":
                return
            if self.trap_y <= self.player.y:
                self.die()
                return
            self._update_player()
            self._update_camera_and_trap()
            self._spawn_saws()
            if self._collides() or self.trap_y <= self.player.y:
                self.die()
                return

    def will_collide(self, right_wall: bool) -> bool:
        target_tile = self.player.tile_pos - 1
        return any(saw.tile == target_tile and saw.right_wall == right_wall for saw in self.columns.saws)

    def die(self) -> None:
        if self.score > self.highscore:
            self.highscore = self.score
        self.state = "dead"
        self.message = "game over"

    def restart(self) -> None:
        highscore = self.highscore
        seed = self.rng.randint(0, 999_999)
        self.__init__(seed=seed)
        self.highscore = highscore

    def _update_player(self) -> None:
        if self.player.jumping:
            self.player.jump_t += 1
            t = min(1.0, self.player.jump_t / self.player.jump_duration)
            ease = 1 - (1 - t) ** 3
            self.player.x = self.player.start_x + (self.player.target_x - self.player.start_x) * ease
            self.player.y -= self.tile_height / self.player.jump_duration
            if self.player.jump_t >= self.player.jump_duration:
                self.player.jumping = False
                self.player.right_wall = self.player.target_right_wall
                self.player.tile_pos -= 1
                self.player.y = self.player.tile_pos * self.tile_height
                if self.state != "will_die":
                    self.score += 1
                self.message = "score"

    def _update_camera_and_trap(self) -> None:
        target_camera = self.player.y - 132
        self.camera_y += (target_camera - self.camera_y) * 0.16
        self.trap_y -= 0.45 + min(2.2, self.score * 0.015)

    def _spawn_saws(self) -> None:
        while self.columns.next_spawn_tile > self.player.tile_pos - 20:
            tile = self.columns.next_spawn_tile
            if tile < self.player.tile_pos - 2:
                self.columns.saws.append(Saw(tile=tile, right_wall=self.rng.random() < 0.5))
            self.columns.next_spawn_tile -= self.rng.randint(2, 4)
        self.columns.saws = [saw for saw in self.columns.saws if saw.tile > self.player.tile_pos - 26]

    def _collides(self) -> bool:
        if self.player.jumping:
            return False
        return any(saw.tile == self.player.tile_pos and saw.right_wall == self.player.right_wall for saw in self.columns.saws)

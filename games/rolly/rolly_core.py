"""Pure precision-platformer rules for the Rolly PyxelPico port."""

from __future__ import annotations

import random


TILE = 16


class RollyCore:
    width = 15
    height = 12

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.spawn = (2, 10)
        self.checkpoint = self.spawn
        self.solid: set[tuple[int, int]] = set()
        self.bouncy: set[tuple[int, int]] = set()
        self.breakable: set[tuple[int, int]] = set()
        self.spikes: set[tuple[int, int]] = set()
        self.orbs: set[tuple[int, int]] = set()
        self.friends: set[tuple[int, int]] = set()
        self.exit = (13, 8)
        self._build_level()
        self.x = self.spawn[0] * TILE + TILE / 2
        self.y = self.spawn[1] * TILE + TILE / 2
        self.vx = 0.0
        self.vy = 0.0
        self.facing = 1
        self.on_ground = True
        self.can_hop = True
        self.exit_open = False
        self.level_clear = False
        self.deaths = 0
        self.friends_rescued = 0
        self.message = "jump roll hop dive"

    def _build_level(self) -> None:
        for x in range(self.width):
            self.solid.add((x, self.height - 1))
        for x in range(5, 10):
            self.solid.add((x, 9))
        for x in range(11, 14):
            self.solid.add((x, 7))
        self.solid.update({(0, y) for y in range(self.height)})
        self.solid.update({(self.width - 1, y) for y in range(self.height)})
        self.bouncy.update({(7, 8), (12, 6)})
        self.breakable.update({(9, 8)})
        self.spikes.update({(4, 10), (10, 10), (12, 10)})
        self.orbs.update({(6, 7), (11, 5)})
        self.friends.update({(13, 6)})
        self.solid.add(self.exit)

    def tick(self, *, left: bool = False, right: bool = False) -> None:
        if self.level_clear:
            return
        accel = 0.35
        if left:
            self.vx -= accel
            self.facing = -1
        if right:
            self.vx += accel
            self.facing = 1
        if not (left or right):
            self.vx *= 0.82
        self.vx = max(-4.0, min(4.0, self.vx))
        self.vy = min(7.0, self.vy + 0.35)
        self._move_axis(self.vx, 0)
        self.on_ground = False
        self._move_axis(0, self.vy)
        self._check_tile_events()

    def jump(self) -> bool:
        if not self.on_ground and not self._standing_on_floor():
            self.message = "need ground"
            return False
        self.vy = -6.2
        self.on_ground = False
        self.message = "jump"
        return True

    def roll(self, direction: int | None = None) -> bool:
        if not self.can_hop:
            self.message = "need orb"
            return False
        if direction:
            self.facing = 1 if direction > 0 else -1
        self.vx += 4.2 * self.facing
        self.vy = min(self.vy, -2.2)
        self.can_hop = False
        self.message = "roll"
        return True

    def _move_axis(self, dx: float, dy: float) -> None:
        steps = int(max(1, abs(dx), abs(dy)) + 1)
        for _ in range(steps):
            nx = self.x + dx / steps
            ny = self.y + dy / steps
            tile = self.tile_at_pixel(nx, ny)
            if self.is_solid(tile):
                if dy > 0:
                    self.on_ground = True
                    self.can_hop = True
                if tile in self.bouncy and dy >= 0:
                    self.vy = -7.4
                    self.message = "bounce"
                elif tile in self.breakable and abs(self.vx) > 3.2:
                    self.breakable.remove(tile)
                    self.solid.discard(tile)
                    self.message = "wall broke"
                else:
                    if dx:
                        self.vx = 0
                    if dy:
                        self.vy = 0
                return
            self.x, self.y = nx, ny

    def _standing_on_floor(self) -> bool:
        return self.is_solid(self.tile_at_pixel(self.x, self.y + TILE / 2 + 1))

    def _check_tile_events(self) -> None:
        tile = self.tile_at_pixel(self.x, self.y)
        if tile in self.spikes or self.y > self.height * TILE:
            self.respawn()
            return
        if tile in self.orbs:
            self.orbs.remove(tile)
            self.can_hop = True
            self.message = "hop recharged"
        if tile in self.friends:
            self.friends.remove(tile)
            self.friends_rescued += 1
            self.exit_open = True
            self.solid.discard(self.exit)
            self.message = "friend rescued"
        if tile == self.exit and self.exit_open:
            self.level_clear = True
            self.message = "friends saved"

    def respawn(self) -> None:
        self.deaths += 1
        self.x = self.checkpoint[0] * TILE + TILE / 2
        self.y = self.checkpoint[1] * TILE + TILE / 2
        self.vx = 0.0
        self.vy = 0.0
        self.can_hop = True
        self.on_ground = False
        self.message = "try again"

    def is_solid(self, tile: tuple[int, int]) -> bool:
        return tile in self.solid or tile in self.bouncy or tile in self.breakable

    def tile_at_pixel(self, x: float, y: float) -> tuple[int, int]:
        return int(x // TILE), int(y // TILE)

    def player_pos(self) -> tuple[int, int]:
        return self.tile_at_pixel(self.x, self.y)

    def move_to_tile(self, x: int, y: int) -> None:
        self.x = x * TILE + TILE / 2
        self.y = y * TILE + TILE / 2
        self.vx = 0.0
        self.vy = 0.0

    def restart(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

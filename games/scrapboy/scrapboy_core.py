"""Pure action-platformer rules for the Scrap Boy PyxelPico port."""

from __future__ import annotations

import random


TILE = 16


class ScrapBoyCore:
    width = 15
    height = 12

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.spawn = (2, 9)
        self.spawn_x = self.spawn[0] * TILE + TILE / 2
        self.spawn_y = self.spawn[1] * TILE + TILE / 2
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.vx = 0.0
        self.vy = 0.0
        self.facing = 1
        self.on_ground = True
        self.weapon = "laser"
        self.hp = 3
        self.scrap = 0
        self.score = 0
        self.level_clear = False
        self.game_over = False
        self.message = "scrap boy"
        self.solid: set[tuple[int, int]] = set()
        self.platforms: set[tuple[int, int]] = set()
        self.spikes: set[tuple[int, int]] = {(10, 10), (11, 10)}
        self.scraps: set[tuple[int, int]] = {(4, 8), (9, 7), (12, 9)}
        self.powerups: dict[tuple[int, int], str] = {(5, 9): "bomb", (9, 6): "magnet"}
        self.enemies: dict[tuple[int, int], int] = {(6, 9): 1, (11, 8): 2}
        self.doors: set[tuple[int, int]] = {(7, 9)}
        self.exit = (13, 9)
        self._build_level()

    def _build_level(self) -> None:
        for x in range(self.width):
            self.solid.add((x, self.height - 1))
        for y in range(self.height):
            self.solid.add((0, y))
            self.solid.add((self.width - 1, y))
        self.solid.update({(4, 10), (5, 10), (6, 10), (7, 10), (8, 10)})
        self.platforms.update({(8, 7), (9, 7), (10, 7), (12, 8)})

    def tick(self, *, left: bool = False, right: bool = False, jump_held: bool = False) -> None:
        if self.level_clear or self.game_over:
            return
        move = int(right) - int(left)
        if move:
            self.vx += move * 0.4
            self.facing = move
        else:
            self.vx *= 0.78 if self.on_ground else 0.9
        self.vx = max(-3.2, min(3.2, self.vx))
        if jump_held and self.vy < -1.0:
            self.vy -= 0.12
        self.vy = min(6.5, self.vy + 0.35)
        self._move_axis(self.vx, 0)
        self.on_ground = False
        self._move_axis(0, self.vy)
        self._check_tile_events()

    def jump(self) -> bool:
        if not self.on_ground:
            self.message = "need ground"
            return False
        self.vy = -6.0
        self.on_ground = False
        self.message = "jump"
        return True

    def wall_jump(self, direction: int) -> bool:
        if self.weapon != "magnet":
            self.message = "need magnet"
            return False
        wall_tile = self.tile_at_pixel(self.x - TILE / 2 - 1, self.y) if direction > 0 else self.tile_at_pixel(self.x + TILE / 2 + 1, self.y)
        if wall_tile not in self.solid:
            self.message = "no wall"
            return False
        self.vx = 4.2 * (1 if direction > 0 else -1)
        self.vy = -6.4
        self.on_ground = False
        self.message = "magnet jump"
        return True

    def shoot(self, dx: int, dy: int) -> bool:
        if self.game_over or self.level_clear:
            return False
        dx = 1 if dx > 0 else -1 if dx < 0 else self.facing
        dy = 1 if dy > 0 else -1 if dy < 0 else 0
        origin = self.player_pos()
        if self.weapon == "bomb":
            return self._bomb(origin, dx, dy)
        if self.weapon == "magnet":
            return self._magnet(origin, dx, dy)
        return self._laser(origin, dx, dy)

    def move_to_tile(self, x: int, y: int) -> None:
        self.x = x * TILE + TILE / 2
        self.y = y * TILE + TILE / 2
        self.vx = 0.0
        self.vy = 0.0

    def restart(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

    def _laser(self, origin: tuple[int, int], dx: int, dy: int) -> bool:
        for step in range(1, 8):
            tile = (origin[0] + dx * step, origin[1] + dy * step)
            if tile in self.solid or tile in self.doors:
                break
            if tile in self.enemies:
                self.enemies[tile] -= 1
                if self.enemies[tile] <= 0:
                    del self.enemies[tile]
                    self.score += 100
                    self.message = "enemy recycled"
                return True
        self.message = "laser"
        return True

    def _bomb(self, origin: tuple[int, int], dx: int, dy: int) -> bool:
        target = (origin[0] + dx * 4, origin[1] + dy * 2)
        affected = {target, (target[0] - 1, target[1]), (target[0] + 1, target[1]), (target[0], target[1] - 1), (target[0], target[1] + 1)}
        opened = False
        for tile in list(self.doors):
            if tile in affected or origin[0] < tile[0] <= target[0] + 1:
                self.doors.remove(tile)
                opened = True
        for tile in list(self.enemies):
            if tile in affected:
                del self.enemies[tile]
                self.score += 120
        self.message = "bomb door" if opened else "bomb"
        return True

    def _magnet(self, origin: tuple[int, int], dx: int, dy: int) -> bool:
        for step in range(1, 5):
            tile = (origin[0] + dx * step, origin[1] + dy * step)
            if tile in self.enemies:
                new_tile = (max(1, min(self.width - 2, tile[0] - dx * 2)), tile[1])
                hp = self.enemies.pop(tile)
                self.enemies[new_tile] = hp
                self.message = "magnet pull"
                return True
        self.message = "magnet"
        return True

    def _move_axis(self, dx: float, dy: float) -> None:
        steps = int(max(1, abs(dx), abs(dy)) + 1)
        for _ in range(steps):
            nx = self.x + dx / steps
            ny = self.y + dy / steps
            tile = self.tile_at_pixel(nx, ny)
            if tile in self.doors or tile in self.solid or (dy > 0 and tile in self.platforms):
                if dy > 0:
                    self.on_ground = True
                if dx:
                    self.vx = 0
                if dy:
                    self.vy = 0
                return
            self.x, self.y = nx, ny

    def _check_tile_events(self) -> None:
        tile = self.player_pos()
        if tile in self.scraps:
            self.scraps.remove(tile)
            self.scrap += 1
            self.score += 25
            self.message = "scrap"
        if tile in self.powerups:
            self.weapon = self.powerups.pop(tile)
            self.message = self.weapon
        if tile in self.spikes and self.weapon != "bomb":
            self.hp -= 1
            self.message = "spikes"
            if self.hp <= 0:
                self.game_over = True
        if tile == self.exit and not self.scraps:
            self.level_clear = True
            self.message = "level clear"

    def tile_at_pixel(self, x: float, y: float) -> tuple[int, int]:
        return int(x // TILE), int(y // TILE)

    def player_pos(self) -> tuple[int, int]:
        return self.tile_at_pixel(self.x, self.y)

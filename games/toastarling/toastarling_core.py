"""Pure platform-adventure rules for the To a Starling PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class Player:
    x: float
    y: float
    dx: float = 0.0
    dy: float = 0.0
    on_ground: bool = False
    coyote: int = 0
    jump_buffer: int = 0
    facing: int = 1
    skill: int = 0


class ToAStarlingCore:
    tile = 12
    player_w = 8
    player_h = 8
    width = 20
    height = 12
    gravity = 0.32
    friction = 0.82
    acceleration = 0.34
    max_dx = 2.35
    jump_speed = -4.6
    max_fall = 4.4
    glide_speed = 1.65

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.tiles: list[list[str]] = []
        self.spawn_x = self.tile
        self.spawn_y = self.tile
        self.goal_x = self.width - 2
        self.goal_y = 1
        self.player = Player(self.spawn_x, self.spawn_y)
        self.berries = 0
        self.keys = 0
        self.deaths = 0
        self.bridge_active = False
        self.cleared = False
        self.message = "to a starling"
        self.set_test_room([
            "####################",
            "#..................#",
            "#@....b.....k.....G#",
            "####################",
            "#.....s....D.......#",
            "#..........B.......#",
            "#..................#",
            "#.........c....^...#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "####################",
        ])

    def reset(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

    def set_test_room(self, rows: list[str]) -> None:
        self.height = len(rows)
        self.width = len(rows[0])
        self.tiles = []
        self.berries = 0
        self.keys = 0
        self.deaths = 0
        self.bridge_active = False
        self.cleared = False
        for y, row in enumerate(rows):
            out = []
            for x, char in enumerate(row):
                if char == "@":
                    self.spawn_x = x * self.tile
                    self.spawn_y = y * self.tile
                    out.append(".")
                elif char == "G":
                    self.goal_x = x
                    self.goal_y = y
                    out.append("G")
                else:
                    out.append(char)
            self.tiles.append(out)
        self.player = Player(self.spawn_x, self.spawn_y, on_ground=True, coyote=8)
        self.message = "find the starling"

    def tick(
        self,
        *,
        left: bool = False,
        right: bool = False,
        jump: bool = False,
        glide: bool = False,
    ) -> None:
        if self.cleared:
            return
        p = self.player
        move = int(right) - int(left)
        if move:
            p.dx += move * self.acceleration
            p.dx = max(-self.max_dx, min(self.max_dx, p.dx))
            p.facing = move
        else:
            p.dx *= self.friction
            if abs(p.dx) < 0.03:
                p.dx = 0

        if jump:
            p.jump_buffer = 6
        elif p.jump_buffer > 0:
            p.jump_buffer -= 1
        if p.on_ground:
            p.coyote = 8
        elif p.coyote > 0:
            p.coyote -= 1
        if p.jump_buffer > 0 and (p.on_ground or p.coyote > 0):
            p.dy = self.jump_speed
            p.on_ground = False
            p.coyote = 0
            p.jump_buffer = 0
            self.message = "jump"

        p.dy += self.gravity
        if glide and p.skill > 0 and p.dy > self.glide_speed:
            p.dy = self.glide_speed
            self.message = "glide"
        p.dy = min(p.dy, self.max_fall)

        self._move_x(p.dx)
        self._move_y(p.dy)
        self._collect_or_trigger()

    def _move_x(self, dx: float) -> None:
        p = self.player
        p.x += dx
        if self._blocked_at_player():
            if dx > 0:
                p.x = (int((p.x + self.tile - 1) // self.tile) * self.tile) - self.tile
            elif dx < 0:
                p.x = (int(p.x // self.tile) + 1) * self.tile
            p.dx = 0

    def _move_y(self, dy: float) -> None:
        p = self.player
        p.y += dy
        p.on_ground = False
        if self._blocked_at_player():
            if dy > 0:
                p.y = (int((p.y + self.tile - 1) // self.tile) * self.tile) - self.tile
                p.on_ground = True
            elif dy < 0:
                p.y = (int(p.y // self.tile) + 1) * self.tile
            p.dy = 0

    def _collect_or_trigger(self) -> None:
        tx, ty = self.player_tile()
        tile = self.tile_at(tx, ty)
        if tile == "b":
            self.berries += 1
            self._set_tile(tx, ty, ".")
            self.message = "berry"
        elif tile == "k":
            self.keys += 1
            self._set_tile(tx, ty, ".")
            self.message = "key"
        elif tile == "D" and self.keys > 0:
            self.keys -= 1
            self._set_tile(tx, ty, ".")
            self.message = "door open"
        elif tile == "s":
            self.bridge_active = not self.bridge_active
            self.message = "bridge on" if self.bridge_active else "bridge off"
        elif tile == "c":
            self.spawn_x = tx * self.tile
            self.spawn_y = ty * self.tile
            self.message = "checkpoint"
        elif tile == "^":
            self._respawn()
        elif tile == "G":
            self.cleared = True
            self.message = "starling reached"
        if self.player.y > self.height * self.tile:
            self._respawn()

    def _respawn(self) -> None:
        self.deaths += 1
        self.player.x = self.spawn_x
        self.player.y = self.spawn_y
        self.player.dx = 0
        self.player.dy = 0
        self.player.on_ground = True
        self.player.coyote = 8
        self.message = "try again"

    def _blocked_at_player(self) -> bool:
        p = self.player
        inset_x = (self.tile - self.player_w) / 2
        inset_y = self.tile - self.player_h
        points = [
            (p.x + inset_x, p.y + inset_y),
            (p.x + inset_x + self.player_w - 1, p.y + inset_y),
            (p.x + inset_x, p.y + inset_y + self.player_h - 1),
            (p.x + inset_x + self.player_w - 1, p.y + inset_y + self.player_h - 1),
        ]
        return any(self.solid_at_pixel(x, y) for x, y in points)

    def solid_at_pixel(self, x: float, y: float) -> bool:
        tx = int(x // self.tile)
        ty = int(y // self.tile)
        tile = self.tile_at(tx, ty)
        if tile == "D" and self.keys > 0:
            self.keys -= 1
            self._set_tile(tx, ty, ".")
            self.message = "door open"
            return False
        return tile == "#" or tile == "D" or (tile == "B" and not self.bridge_active)

    def tile_at(self, x: int, y: int) -> str:
        if x < 0 or y < 0 or y >= self.height or x >= self.width:
            return "#"
        return self.tiles[y][x]

    def player_tile(self) -> tuple[int, int]:
        return int((self.player.x + self.tile / 2) // self.tile), int((self.player.y + self.tile - 2) // self.tile)

    def _set_tile(self, x: int, y: int, value: str) -> None:
        self.tiles[y][x] = value

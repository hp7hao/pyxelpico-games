"""Pure platform-delivery rules for the Air Delivery PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class Player:
    x: float
    y: float
    dx: float = 0.0
    dy: float = 0.0
    facing: int = 1
    on_ground: bool = False
    on_ladder: bool = False
    coyote: int = 0
    jump_buffer: int = 0
    has_glider: bool = False
    has_drill: bool = False


class AirDeliveryCore:
    tile = 12
    player_w = 8
    player_h = 11
    gravity = 0.30
    accel = 0.28
    friction = 0.78
    max_dx = 2.0
    jump_speed = -4.4
    max_fall = 4.2
    glide_fall_speed = 1.25
    climb_speed = 1.55

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.tiles: list[list[str]] = []
        self.spawn_x = self.tile
        self.spawn_y = self.tile
        self.airship_x = 0
        self.airship_y = 0
        self.letters = 0
        self.found_letters = 0
        self.delivered = 0
        self.total_recipients = 0
        self.deaths = 0
        self.cleared = False
        self.message = "deliver the mail"
        self.set_test_room([
            "########################",
            "#......................#",
            "#@..L....H....R....A...#",
            "#........H.............#",
            "#........H......D......#",
            "#............^.........#",
            "########################",
        ])

    def set_test_room(self, rows: list[str]) -> None:
        self.height = len(rows)
        self.width = len(rows[0])
        self.tiles = []
        self.letters = 0
        self.found_letters = 0
        self.delivered = 0
        self.total_recipients = 0
        self.deaths = 0
        self.cleared = False
        self.message = "deliver the mail"
        for y, row in enumerate(rows):
            out = []
            for x, char in enumerate(row):
                if char == "@":
                    self.spawn_x = x * self.tile
                    self.spawn_y = y * self.tile
                    out.append(".")
                elif char == "R":
                    self.total_recipients += 1
                    out.append("R")
                elif char == "A":
                    self.airship_x = x
                    self.airship_y = y
                    out.append("A")
                else:
                    out.append(char)
            self.tiles.append(out)
        self.player = Player(self.spawn_x, self.spawn_y, on_ground=True, coyote=8)

    def tick(
        self,
        *,
        left: bool = False,
        right: bool = False,
        up: bool = False,
        down: bool = False,
        jump: bool = False,
        interact: bool = False,
    ) -> None:
        if self.cleared:
            return
        self._update_player(left=left, right=right, up=up, down=down, jump=jump, glide=interact)
        self._collect_or_trigger(interact=interact)

    def _update_player(self, *, left: bool, right: bool, up: bool, down: bool, jump: bool, glide: bool) -> None:
        p = self.player
        tile = self.tile_at(*self.player_tile())
        p.on_ladder = tile == "H"

        move = int(right) - int(left)
        if move:
            p.dx += move * self.accel
            p.dx = max(-self.max_dx, min(self.max_dx, p.dx))
            p.facing = move
        else:
            p.dx *= self.friction
            if abs(p.dx) < 0.04:
                p.dx = 0.0

        if p.on_ladder and (up or down):
            p.dy = (int(down) - int(up)) * self.climb_speed
            p.on_ground = False
            self.message = "climb"
        else:
            if jump:
                p.jump_buffer = 5
            elif p.jump_buffer > 0:
                p.jump_buffer -= 1
            if p.on_ground:
                p.coyote = 7
            elif p.coyote > 0:
                p.coyote -= 1
            if p.jump_buffer > 0 and (p.on_ground or p.coyote > 0):
                p.dy = self.jump_speed
                p.on_ground = False
                p.coyote = 0
                p.jump_buffer = 0
                self.message = "jump"
            else:
                p.dy = min(p.dy + self.gravity, self.max_fall)
            if glide and p.has_glider and p.dy > self.glide_fall_speed:
                p.dy = self.glide_fall_speed
                self.message = "glide"

        self._move_x(p.dx)
        self._move_y(p.dy)

    def _move_x(self, dx: float) -> None:
        p = self.player
        p.x += dx
        if self._blocked_at_player():
            if dx > 0:
                p.x = int((p.x + self.tile - 1) // self.tile) * self.tile - self.tile
            elif dx < 0:
                p.x = (int(p.x // self.tile) + 1) * self.tile
            p.dx = 0.0

    def _move_y(self, dy: float) -> None:
        p = self.player
        p.y += dy
        p.on_ground = False
        if self._blocked_at_player():
            if dy > 0:
                p.y = int((p.y + self.tile - 1) // self.tile) * self.tile - self.tile
                p.on_ground = True
            elif dy < 0:
                p.y = (int(p.y // self.tile) + 1) * self.tile
            p.dy = 0.0

    def _collect_or_trigger(self, *, interact: bool) -> None:
        tx, ty = self.player_tile()
        tile = self.tile_at(tx, ty)
        if tile == "L":
            self.letters += 1
            self.found_letters += 1
            self._set_tile(tx, ty, ".")
            self.message = "letter found"
        elif tile == "^":
            self._respawn()
        elif interact and self.letters > 0 and (target := self._near_tile("R", 4)) is not None:
            tx, ty = target
            self.letters -= 1
            self.delivered += 1
            if self.delivered == 1:
                self.player.has_glider = True
            if self.delivered >= 2 or self.total_recipients <= 1:
                self.player.has_drill = True
            self._set_tile(tx, ty, "r")
            self.message = "letter delivered"
        elif interact and self.player.has_drill and (target := self._near_tile("D", 3)) is not None:
            tx, ty = target
            self._set_tile(tx, ty, ".")
            self.message = "secret passage"
        elif interact and self._near_tile("A") is not None:
            if self.delivered >= self.total_recipients:
                self.cleared = True
                self.message = "airship ready"
            else:
                self.message = "mail remains"
        if self.player.y > self.height * self.tile:
            self._respawn()

    def _respawn(self) -> None:
        self.deaths += 1
        self.player.x = self.spawn_x
        self.player.y = self.spawn_y
        self.player.dx = 0.0
        self.player.dy = 0.0
        self.player.on_ground = True
        self.player.coyote = 8
        self.message = "try again"

    def _blocked_at_player(self) -> bool:
        p = self.player
        points = [
            (p.x + 2, p.y + 1),
            (p.x + self.player_w - 2, p.y + 1),
            (p.x + 2, p.y + self.player_h - 1),
            (p.x + self.player_w - 2, p.y + self.player_h - 1),
        ]
        return any(self.solid_at_pixel(x, y) for x, y in points)

    def solid_at_pixel(self, x: float, y: float) -> bool:
        tile = self.tile_at(int(x // self.tile), int(y // self.tile))
        return tile == "#" or tile == "D"

    def player_tile(self) -> tuple[int, int]:
        return int((self.player.x + self.player_w / 2) // self.tile), int((self.player.y + self.player_h - 2) // self.tile)

    def tile_at(self, x: int, y: int) -> str:
        if x < 0 or y < 0 or y >= self.height or x >= self.width:
            return "#"
        return self.tiles[y][x]

    def _near_tile(self, value: str, radius: int = 1) -> tuple[int, int] | None:
        px, py = self.player_tile()
        for y in range(py - radius, py + radius + 1):
            for x in range(px - radius, px + radius + 1):
                if self.tile_at(x, y) == value:
                    return x, y
        return None

    def _set_tile(self, x: int, y: int, value: str) -> None:
        self.tiles[y][x] = value

    def restart(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

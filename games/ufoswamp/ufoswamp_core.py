"""Pure gameplay rules for the UFO Swamp Odyssey PyxelPico port."""

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
    jump_buffer: int = 0
    coyote: int = 0


@dataclass
class Enemy:
    x: float
    y: float
    anchor_x: float
    stunned: int = 0
    alive: bool = True
    drift: float = 0.0


class UfoSwampCore:
    tile = 12
    player_w = 8
    player_h = 12
    gravity = 0.28
    water_lift = 0.18
    accel = 0.28
    friction = 0.78
    max_dx = 2.1
    jump_speed = -4.2
    max_fall = 4.0
    shoot_range = 72
    core_charge_ticks = 24

    gun_order = ("emp", "portal", "grapple")

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.tiles: list[list[str]] = []
        self.spawn_x = self.tile
        self.spawn_y = self.tile
        self.water_y = 9 * self.tile
        self.score = 0
        self.unlocked_guns = 0
        self.gun = "emp"
        self.enemies: list[Enemy] = []
        self.portals: dict[int, tuple[int, int]] = {}
        self.hooks: list[tuple[int, int]] = []
        self.core_x = 0.0
        self.core_y = 0.0
        self.core_charge = 0
        self.cleared = False
        self.message = "ufo swamp odyssey"
        self.set_test_room([
            "####################",
            "#..................#",
            "#@..s..E....1......#",
            "#......e.......H...#",
            "#......p....2......#",
            "#........g.........#",
            "#..............C...#",
            "#..................#",
            "#..................#",
            "####################",
        ])

    def set_test_room(self, rows: list[str]) -> None:
        self.height = len(rows)
        self.width = len(rows[0])
        self.tiles = []
        self.enemies = []
        self.portals = {}
        self.hooks = []
        self.score = 0
        self.unlocked_guns = 0
        self.gun = "emp"
        self.core_charge = 0
        self.cleared = False
        self.message = "disable the emp cannon"
        for y, row in enumerate(rows):
            out = []
            for x, char in enumerate(row):
                if char == "@":
                    self.spawn_x = x * self.tile
                    self.spawn_y = y * self.tile
                    out.append(".")
                elif char == "e":
                    self.enemies.append(Enemy(x * self.tile, y * self.tile, x * self.tile))
                    out.append(".")
                elif char in "12":
                    self.portals[int(char)] = (x, y)
                    out.append(char)
                elif char == "H":
                    self.hooks.append((x, y))
                    out.append("H")
                elif char == "C":
                    self.core_x = x * self.tile
                    self.core_y = y * self.tile
                    out.append("C")
                else:
                    out.append(char)
            self.tiles.append(out)
        self.player = Player(self.spawn_x, self.spawn_y, on_ground=True, coyote=8)
        self.water_y = max(0, self.height - 2) * self.tile

    def tick(
        self,
        *,
        left: bool = False,
        right: bool = False,
        jump: bool = False,
        shoot: bool = False,
        cycle_next: bool = False,
        cycle_prev: bool = False,
    ) -> None:
        if self.cleared:
            return
        if cycle_next:
            self.cycle_gun(1)
        elif cycle_prev:
            self.cycle_gun(-1)

        self._update_player(left=left, right=right, jump=jump)
        self._collect_or_trigger()
        self._update_enemies()
        if shoot:
            self._shoot()
        elif self.core_charge > 0:
            self.core_charge = max(0, self.core_charge - 2)

    def _update_player(self, *, left: bool, right: bool, jump: bool) -> None:
        p = self.player
        move = int(right) - int(left)
        if move:
            p.dx += move * self.accel
            p.dx = max(-self.max_dx, min(self.max_dx, p.dx))
            p.facing = move
        else:
            p.dx *= self.friction
            if abs(p.dx) < 0.04:
                p.dx = 0.0

        if jump:
            p.jump_buffer = 5
        elif p.jump_buffer > 0:
            p.jump_buffer -= 1
        if p.on_ground:
            p.coyote = 7
        elif p.coyote > 0:
            p.coyote -= 1
        if p.jump_buffer > 0 and (p.on_ground or p.coyote > 0 or p.y >= self.water_y):
            p.dy = self.jump_speed if p.on_ground or p.coyote > 0 else self.jump_speed * 0.75
            p.on_ground = False
            p.coyote = 0
            p.jump_buffer = 0
            self.message = "jump"

        if p.y >= self.water_y:
            p.dy = min(p.dy, 1.6) - self.water_lift
            self.message = "swamp bounce"
        else:
            p.dy = min(p.dy + self.gravity, self.max_fall)

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

    def _collect_or_trigger(self) -> None:
        tx, ty = self.player_tile()
        tile = self.tile_at(tx, ty)
        if tile == "s":
            self.score += 10
            self._set_tile(tx, ty, ".")
            self.message = "+10 score"
        elif tile == "E":
            self._unlock_gun("emp")
            self._set_tile(tx, ty, ".")
        elif tile == "p":
            self._unlock_gun("portal")
            self._set_tile(tx, ty, ".")
        elif tile == "g":
            self._unlock_gun("grapple")
            self._set_tile(tx, ty, ".")

    def _unlock_gun(self, gun: str) -> None:
        self.unlocked_guns = max(self.unlocked_guns, self.gun_order.index(gun) + 1)
        self.gun = gun
        self.message = f"{gun} zapper"

    def cycle_gun(self, direction: int) -> None:
        if self.unlocked_guns == 0:
            return
        available = list(self.gun_order[: self.unlocked_guns])
        index = available.index(self.gun) if self.gun in available else 0
        self.gun = available[(index + direction) % len(available)]
        self.message = f"{self.gun} zapper"

    def select_gun(self, gun: str) -> None:
        if gun not in self.gun_order:
            raise ValueError(f"unknown gun: {gun}")
        self.unlocked_guns = max(self.unlocked_guns, self.gun_order.index(gun) + 1)
        self.gun = gun

    def _update_enemies(self) -> None:
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            if enemy.stunned > 0:
                enemy.stunned -= 1
                continue
            enemy.drift += 0.08
            target = enemy.anchor_x + self.rng.choice((-1, 1)) * 0.08
            if abs(self.player.x - enemy.x) < 60 and abs(self.player.y - enemy.y) < 28:
                target = self.player.x
            enemy.x += max(-0.55, min(0.55, (target - enemy.x) * 0.035))
            if abs(enemy.x - self.player.x) < 8 and abs(enemy.y - self.player.y) < 12:
                self.player.dx = -1.8 if self.player.x < enemy.x else 1.8
                self.player.dy = min(self.player.dy, -1.2)
                self.message = "bumped by eyebot"

    def _shoot(self) -> None:
        if self.unlocked_guns == 0:
            self.message = "need zapper fuel"
            return
        if self.gun == "emp":
            if self._try_core_zap():
                return
            for enemy in self.enemies:
                if enemy.alive and self._in_front(enemy.x, enemy.y, y_margin=18):
                    enemy.stunned = 90
                    self.message = "eyebot stunned"
                    return
            self.message = "emp spark"
        elif self.gun == "portal":
            if len(self.portals) >= 2:
                first, second = self.portals[1], self.portals[2]
                target = second if self._in_front(first[0] * self.tile, first[1] * self.tile, y_margin=28) else None
                if target is None and self._in_front(second[0] * self.tile, second[1] * self.tile, y_margin=28):
                    target = first
                if target is not None:
                    self.player.x = target[0] * self.tile
                    self.player.y = target[1] * self.tile
                    self.player.dy = 0.0
                    self.message = "portal jump"
                    return
            self.message = "portal fizz"
        elif self.gun == "grapple":
            for hx, hy in self.hooks:
                hook_x = hx * self.tile
                hook_y = hy * self.tile
                if self._in_front(hook_x, hook_y, y_margin=36, range_px=96):
                    self.player.dx = 3.0 if hook_x > self.player.x else -3.0
                    self.player.dy = min(-2.4, (hook_y - self.player.y) * 0.08)
                    self.player.x += self.player.dx
                    self.player.y += self.player.dy
                    self.message = "grapple"
                    return
            self.message = "grapple miss"

    def _try_core_zap(self) -> bool:
        if not self.core_x and not self.core_y:
            return False
        if not self._in_front(self.core_x, self.core_y, y_margin=20, range_px=96):
            self.core_charge = 0
            return False
        self.core_charge += 1
        self.message = "charging core"
        if self.core_charge >= self.core_charge_ticks:
            self.cleared = True
            self.message = "emp cannon disabled"
        return True

    def _in_front(self, x: float, y: float, *, y_margin: float, range_px: float | None = None) -> bool:
        p = self.player
        range_px = self.shoot_range if range_px is None else range_px
        dx = x - p.x
        return (dx * p.facing) >= 0 and abs(dx) <= range_px and abs(y - p.y) <= y_margin

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
        return self.tile_at(int(x // self.tile), int(y // self.tile)) == "#"

    def tile_at(self, x: int, y: int) -> str:
        if x < 0 or y < 0 or y >= self.height or x >= self.width:
            return "#"
        return self.tiles[y][x]

    def player_tile(self) -> tuple[int, int]:
        return int((self.player.x + self.player_w / 2) // self.tile), int((self.player.y + self.player_h - 2) // self.tile)

    def _set_tile(self, x: int, y: int, value: str) -> None:
        self.tiles[y][x] = value

    def restart(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

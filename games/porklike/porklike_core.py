"""Pure turn-based dungeon rules for the Porklike PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import random


class Tile(Enum):
    WALL = "#"
    FLOOR = "."
    EXIT = ">"


class MoveResult(Enum):
    BLOCKED = "blocked"
    MOVED = "moved"
    ATTACKED = "attacked"
    ITEM = "item"
    EXIT = "exit"


@dataclass
class Enemy:
    x: int
    y: int
    hp: int
    damage: int = 1
    dead: bool = False


@dataclass
class Item:
    x: int
    y: int
    kind: str


class PorklikeCore:
    width = 15
    height = 15

    def __init__(self, seed: int = 1) -> None:
        self.base_seed = seed
        self.rng = random.Random(seed)
        self.level = 1
        self.max_hp = 8
        self.player_hp = self.max_hp
        self.player_x = 1
        self.player_y = 1
        self.exit_x = self.width - 2
        self.exit_y = self.height - 2
        self.turn = 0
        self.score = 0
        self.lost = False
        self.won = False
        self.message = "find the stairs"
        self.tiles: list[list[Tile]] = []
        self.enemies: list[Enemy] = []
        self.items: list[Item] = []
        self._generate_level()

    def reset(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

    def tile_at(self, x: int, y: int) -> Tile:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return Tile.WALL
        return self.tiles[y][x]

    def floor_count(self) -> int:
        return sum(tile is not Tile.WALL for row in self.tiles for tile in row)

    def move_player(self, dx: int, dy: int) -> MoveResult:
        if self.lost or self.won:
            return MoveResult.BLOCKED

        nx = self.player_x + dx
        ny = self.player_y + dy
        if dx == 0 and dy == 0:
            self._after_player_turn()
            return MoveResult.MOVED

        enemy = self.enemy_at(nx, ny)
        if enemy is not None:
            self._attack_enemy(enemy)
            self._after_player_turn()
            return MoveResult.ATTACKED

        tile = self.tile_at(nx, ny)
        if tile is Tile.WALL:
            self.message = "wall"
            return MoveResult.BLOCKED

        self.player_x = nx
        self.player_y = ny
        item = self.item_at(nx, ny)
        if item is not None:
            self._collect(item)
            self._after_player_turn()
            return MoveResult.ITEM
        if tile is Tile.EXIT:
            self._advance_level()
            return MoveResult.EXIT

        self.message = "step"
        self._after_player_turn()
        return MoveResult.MOVED

    def enemy_at(self, x: int, y: int) -> Enemy | None:
        for enemy in self.enemies:
            if not enemy.dead and enemy.x == x and enemy.y == y:
                return enemy
        return None

    def item_at(self, x: int, y: int) -> Item | None:
        for item in self.items:
            if item.x == x and item.y == y:
                return item
        return None

    def set_test_map(self, rows: list[str]) -> None:
        self.height = len(rows)
        self.width = len(rows[0])
        self.tiles = []
        self.enemies = []
        self.items = []
        self.exit_x = self.exit_y = 0
        for y, row in enumerate(rows):
            out_row = []
            for x, char in enumerate(row):
                if char == "#":
                    out_row.append(Tile.WALL)
                elif char == ">":
                    out_row.append(Tile.EXIT)
                    self.exit_x, self.exit_y = x, y
                else:
                    out_row.append(Tile.FLOOR)
                if char == "@":
                    self.player_x, self.player_y = x, y
                elif char == "e":
                    self.enemies.append(Enemy(x, y, hp=3))
                elif char == "f":
                    self.items.append(Item(x, y, "food"))
            self.tiles.append(out_row)
        self.turn = 0
        self.lost = False
        self.won = False

    def _generate_level(self) -> None:
        self.width = 15
        self.height = 15
        self.tiles = [[Tile.WALL for _ in range(self.width)] for _ in range(self.height)]
        rooms: list[tuple[int, int, int, int]] = []
        attempts = 26
        for _ in range(attempts):
            w = self.rng.randint(3, 5)
            h = self.rng.randint(3, 5)
            x = self.rng.randint(1, self.width - w - 1)
            y = self.rng.randint(1, self.height - h - 1)
            room = (x, y, w, h)
            if any(self._overlaps(room, other) for other in rooms):
                continue
            rooms.append(room)
            self._carve_room(room)
            if len(rooms) > 1:
                self._connect(self._center(rooms[-2]), self._center(room))

        if not rooms:
            rooms = [(1, 1, self.width - 2, self.height - 2)]
            self._carve_room(rooms[0])

        if self.floor_count() <= 45:
            self._carve_room((5, 5, 5, 5))
            self._connect(self._center(rooms[0]), (7, 7))
            rooms.append((5, 5, 5, 5))

        self.player_x, self.player_y = self._center(rooms[0])
        self.exit_x, self.exit_y = self._center(rooms[-1])
        if (self.player_x, self.player_y) == (self.exit_x, self.exit_y):
            self.exit_x, self.exit_y = self.width - 2, self.height - 2
            self.tiles[self.exit_y][self.exit_x] = Tile.FLOOR
        self.tiles[self.exit_y][self.exit_x] = Tile.EXIT
        self._populate()

    def _populate(self) -> None:
        self.enemies = []
        self.items = []
        floors = [
            (x, y)
            for y in range(1, self.height - 1)
            for x in range(1, self.width - 1)
            if self.tiles[y][x] is Tile.FLOOR and (x, y) != (self.player_x, self.player_y)
        ]
        self.rng.shuffle(floors)
        enemy_count = min(3 + self.level, len(floors) // 4)
        for x, y in floors[:enemy_count]:
            self.enemies.append(Enemy(x, y, hp=2 + self.level // 2))
        for x, y in floors[enemy_count : enemy_count + 3]:
            self.items.append(Item(x, y, "food"))

    def _after_player_turn(self) -> None:
        self.turn += 1
        self._enemy_turn()
        self.enemies = [enemy for enemy in self.enemies if not enemy.dead]

    def _attack_enemy(self, enemy: Enemy) -> None:
        enemy.hp -= 2
        self.message = "bonk"
        if enemy.hp <= 0:
            enemy.dead = True
            self.score += 10
            self.message = "enemy down"
            if self.rng.random() < 0.75:
                self.items.append(Item(enemy.x, enemy.y, "food"))

    def _enemy_turn(self) -> None:
        for enemy in self.enemies:
            if enemy.dead:
                continue
            if abs(enemy.x - self.player_x) + abs(enemy.y - self.player_y) == 1:
                self._damage_player(enemy.damage)
                continue
            dx = self._sign(self.player_x - enemy.x)
            dy = self._sign(self.player_y - enemy.y)
            choices = [(dx, 0), (0, dy)] if abs(self.player_x - enemy.x) >= abs(self.player_y - enemy.y) else [(0, dy), (dx, 0)]
            for mx, my in choices:
                nx, ny = enemy.x + mx, enemy.y + my
                if (mx or my) and self.tile_at(nx, ny) is not Tile.WALL and self.enemy_at(nx, ny) is None and (nx, ny) != (self.player_x, self.player_y):
                    enemy.x, enemy.y = nx, ny
                    break

    def _damage_player(self, amount: int) -> None:
        self.player_hp = max(0, self.player_hp - amount)
        self.message = "ouch"
        if self.player_hp <= 0:
            self.lost = True
            self.message = "pork chopped"

    def _collect(self, item: Item) -> None:
        self.items.remove(item)
        if item.kind == "food":
            self.player_hp = min(self.max_hp, self.player_hp + 2)
            self.score += 3
            self.message = "snack"

    def _advance_level(self) -> None:
        self.level += 1
        self.score += 25
        self.player_hp = min(self.max_hp, self.player_hp + 1)
        if self.level > 5:
            self.won = True
            self.message = "escaped"
            return
        self.rng.seed(self.base_seed + self.level * 997 + self.score)
        self.message = f"floor {self.level}"
        self._generate_level()

    def _carve_room(self, room: tuple[int, int, int, int]) -> None:
        x, y, w, h = room
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.tiles[yy][xx] = Tile.FLOOR

    def _connect(self, a: tuple[int, int], b: tuple[int, int]) -> None:
        ax, ay = a
        bx, by = b
        for x in range(min(ax, bx), max(ax, bx) + 1):
            self.tiles[ay][x] = Tile.FLOOR
        for y in range(min(ay, by), max(ay, by) + 1):
            self.tiles[y][bx] = Tile.FLOOR

    @staticmethod
    def _overlaps(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> bool:
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return ax <= bx + bw and ax + aw >= bx and ay <= by + bh and ay + ah >= by

    @staticmethod
    def _center(room: tuple[int, int, int, int]) -> tuple[int, int]:
        x, y, w, h = room
        return x + w // 2, y + h // 2

    @staticmethod
    def _sign(value: int) -> int:
        return (value > 0) - (value < 0)

"""Pure turn-based dungeon rules for the Into Ruins PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import random


class Tile(Enum):
    WALL = "#"
    FLOOR = "."
    PIT = " "
    EXIT = ">"


@dataclass
class Enemy:
    x: int
    y: int
    kind: str
    hp: int
    attack: int
    ranged: bool = False
    flying: bool = False
    dead: bool = False
    statuses: dict[str, int] = field(default_factory=dict)


class IntoRuinsCore:
    width = 21
    height = 17
    final_depth = 16
    vision_radius = 5

    def __init__(self, seed: int = 1) -> None:
        self.base_seed = seed
        self.rng = random.Random(seed)
        self.max_hp = 14
        self.player_hp = self.max_hp
        self.player_x = 10
        self.player_y = 10
        self.depth = 1
        self.light = 5
        self.turn = 0
        self.score = 0
        self.mode = "play"
        self.message = "reach depth 16"
        self.statuses: dict[str, int] = {}
        self.tiles: list[list[Tile]] = []
        self.enemies: list[Enemy] = []
        self.items: dict[tuple[int, int], str] = {}
        self.exit_pos = (self.width - 3, self.height - 3)
        self.explored: set[tuple[int, int]] = set()
        self.visible: set[tuple[int, int]] = set()
        self._generate_level()
        self._update_visibility()

    @property
    def won(self) -> bool:
        return self.mode == "won"

    @property
    def lost(self) -> bool:
        return self.mode == "lost"

    def reset(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

    def tile_at(self, x: int, y: int) -> Tile:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return Tile.WALL
        return self.tiles[y][x]

    def enemy_at(self, x: int, y: int) -> Enemy | None:
        for enemy in self.enemies:
            if not enemy.dead and enemy.x == x and enemy.y == y:
                return enemy
        return None

    def step(self, dx: int, dy: int) -> str:
        if self.mode != "play":
            return "blocked"
        if self.statuses.get("freeze", 0) > 0:
            self.message = "frozen"
            self._after_player_turn()
            return "blocked"
        if dx == 0 and dy == 0:
            if (self.player_x, self.player_y) in self.items:
                self._collect(self.player_x, self.player_y)
            self._after_player_turn()
            return "wait"

        nx = self.player_x + dx
        ny = self.player_y + dy
        enemy = self.enemy_at(nx, ny)
        if enemy is not None:
            self._attack(enemy)
            self._after_player_turn()
            return "attack"
        tile = self.tile_at(nx, ny)
        if tile in {Tile.WALL, Tile.PIT}:
            self.message = "blocked"
            return "blocked"

        self.player_x = nx
        self.player_y = ny
        if tile is Tile.EXIT:
            self.descend()
            return "exit"
        if (nx, ny) in self.items:
            self._collect(nx, ny)
            result = "item"
        else:
            self.message = "step"
            result = "move"
        self._after_player_turn()
        return result

    def wait_turn(self) -> str:
        return self.step(0, 0)

    def descend(self) -> None:
        if self.depth >= self.final_depth:
            self.mode = "won"
            self.message = "wings of yendor"
            self.score += 500
            return
        self.depth += 1
        self.light = max(4, self.light - 1)
        self.message = f"depth {self.depth}"
        self._generate_level()
        self._update_visibility()

    def _generate_level(self) -> None:
        self.tiles = [[Tile.WALL for _ in range(self.width)] for _ in range(self.height)]
        rooms: list[tuple[int, int, int, int]] = []
        for _ in range(20):
            w = self.rng.randint(4, 7)
            h = self.rng.randint(3, 5)
            x = self.rng.randrange(1, self.width - w - 1, 2)
            y = self.rng.randint(1, self.height - h - 1)
            room = (x, y, w, h)
            if any(self._overlaps(room, other) for other in rooms):
                continue
            rooms.append(room)
            self._carve_room(room)
            if len(rooms) > 1:
                self._connect(self._center(rooms[-2]), self._center(room))
        if len(rooms) < 2:
            rooms = [(2, 3, 7, 5), (12, 9, 7, 5)]
            self.tiles = [[Tile.WALL for _ in range(self.width)] for _ in range(self.height)]
            for room in rooms:
                self._carve_room(room)
            self._connect(self._center(rooms[0]), self._center(rooms[1]))

        self.player_x, self.player_y = 10, 10
        for y in range(8, 13):
            self.tiles[y][10] = Tile.FLOOR
        for x in range(7, 15):
            self.tiles[10][x] = Tile.FLOOR
        self.exit_pos = self._center(rooms[-1])
        ex, ey = self.exit_pos
        self.tiles[ey][ex] = Tile.EXIT
        self._cut_pits()
        self._populate()

    def _populate(self) -> None:
        self.enemies = []
        self.items = {}
        floors = [
            (x, y)
            for y in range(1, self.height - 1)
            for x in range(1, self.width - 1)
            if self.tiles[y][x] is Tile.FLOOR and (x, y) != (self.player_x, self.player_y)
        ]
        self.rng.shuffle(floors)
        enemy_kinds = [
            ("goblin", 3, 1, False),
            ("bat", 2, 1, False),
            ("mystic", 3, 1, True),
            ("ogre", 5, 2, False),
        ]
        for x, y in floors[: min(3 + self.depth // 2, 8)]:
            kind, hp, attack, ranged = self.rng.choice(enemy_kinds)
            self.enemies.append(Enemy(x, y, kind, hp + self.depth // 5, attack, ranged=ranged, flying=kind == "bat"))
        for pos, kind in zip(floors[8:14], ["potion", "torch", "frost", "fire", "potion", "torch"]):
            self.items[pos] = kind

    def _after_player_turn(self) -> None:
        self.turn += 1
        self._tick_statuses()
        if self.mode != "play":
            return
        self._enemy_turn()
        self.enemies = [enemy for enemy in self.enemies if not enemy.dead]
        self._update_visibility()

    def _tick_statuses(self) -> None:
        if self.statuses.get("burn", 0) > 0:
            self._damage_player(1, "burning")
        self._decrement(self.statuses)
        for enemy in self.enemies:
            if enemy.dead:
                continue
            if enemy.statuses.get("burn", 0) > 0:
                enemy.hp -= 1
                if enemy.hp <= 0:
                    enemy.dead = True
                    self.score += 10
            self._decrement(enemy.statuses)

    def _enemy_turn(self) -> None:
        for enemy in self.enemies:
            if enemy.dead or enemy.statuses.get("freeze", 0) > 0:
                continue
            distance = abs(enemy.x - self.player_x) + abs(enemy.y - self.player_y)
            if distance == 1:
                self._damage_player(enemy.attack, f"{enemy.kind} hits")
                continue
            if enemy.ranged and self._line_clear(enemy.x, enemy.y, self.player_x, self.player_y):
                self._damage_player(enemy.attack, f"{enemy.kind} casts")
                continue
            if distance <= 7:
                self._move_enemy_toward(enemy)

    def _move_enemy_toward(self, enemy: Enemy) -> None:
        dx = self._sign(self.player_x - enemy.x)
        dy = self._sign(self.player_y - enemy.y)
        choices = [(dx, 0), (0, dy)] if abs(self.player_x - enemy.x) >= abs(self.player_y - enemy.y) else [(0, dy), (dx, 0)]
        for mx, my in choices:
            nx, ny = enemy.x + mx, enemy.y + my
            if (nx, ny) == (self.player_x, self.player_y):
                continue
            if self.enemy_at(nx, ny) is None and self.tile_at(nx, ny) in {Tile.FLOOR, Tile.EXIT}:
                enemy.x, enemy.y = nx, ny
                return

    def _attack(self, enemy: Enemy) -> None:
        damage = 2 + (1 if self.light >= 6 else 0)
        enemy.hp -= damage
        self.message = f"hit {enemy.kind}"
        if enemy.hp <= 0:
            enemy.dead = True
            self.score += 20
            self.message = f"{enemy.kind} falls"
            if self.rng.random() < 0.35:
                self.items[(enemy.x, enemy.y)] = self.rng.choice(["potion", "torch", "frost"])

    def _collect(self, x: int, y: int) -> None:
        kind = self.items.pop((x, y))
        if kind == "potion":
            self.player_hp = min(self.max_hp, self.player_hp + 5)
            self.message = "orb of life"
        elif kind == "torch":
            self.light = min(9, self.light + 3)
            self.message = "torch lit"
        elif kind == "frost":
            for enemy in self.enemies:
                if abs(enemy.x - x) + abs(enemy.y - y) <= 3:
                    enemy.statuses["freeze"] = 2
            self.message = "ice blooms"
        elif kind == "fire":
            for enemy in self.enemies:
                if abs(enemy.x - x) + abs(enemy.y - y) <= 2:
                    enemy.statuses["burn"] = 3
            self.message = "fire orb"

    def _damage_player(self, amount: int, message: str) -> None:
        self.player_hp = max(0, self.player_hp - amount)
        self.message = message
        if self.player_hp <= 0:
            self.mode = "lost"
            self.message = "lost in ruins"

    def _update_visibility(self) -> None:
        radius = max(self.vision_radius, self.light)
        self.visible = set()
        for y in range(self.height):
            for x in range(self.width):
                if abs(x - self.player_x) + abs(y - self.player_y) <= radius:
                    self.visible.add((x, y))
        self.explored.update(self.visible)

    def _line_clear(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        if x1 != x2 and y1 != y2:
            return False
        steps = max(abs(x2 - x1), abs(y2 - y1))
        if steps > 6:
            return False
        dx = self._sign(x2 - x1)
        dy = self._sign(y2 - y1)
        for i in range(1, steps):
            if self.tile_at(x1 + dx * i, y1 + dy * i) is Tile.WALL:
                return False
        return True

    def _cut_pits(self) -> None:
        for _ in range(8):
            x = self.rng.randint(2, self.width - 3)
            y = self.rng.randint(2, self.height - 3)
            if (x, y) not in {(self.player_x, self.player_y), self.exit_pos} and self.tiles[y][x] is Tile.FLOOR:
                self.tiles[y][x] = Tile.PIT

    def _carve_room(self, room: tuple[int, int, int, int]) -> None:
        x, y, w, h = room
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.tiles[yy][xx] = Tile.FLOOR

    def _connect(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        x, y = start
        ex, ey = end
        while x != ex:
            self.tiles[y][x] = Tile.FLOOR
            x += self._sign(ex - x)
        while y != ey:
            self.tiles[y][x] = Tile.FLOOR
            y += self._sign(ey - y)
        self.tiles[y][x] = Tile.FLOOR

    @staticmethod
    def _overlaps(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> bool:
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return ax <= bx + bw and bx <= ax + aw and ay <= by + bh and by <= ay + ah

    @staticmethod
    def _center(room: tuple[int, int, int, int]) -> tuple[int, int]:
        x, y, w, h = room
        return x + w // 2, y + h // 2

    @staticmethod
    def _sign(value: int) -> int:
        return (value > 0) - (value < 0)

    @staticmethod
    def _decrement(statuses: dict[str, int]) -> None:
        for key in list(statuses):
            statuses[key] -= 1
            if statuses[key] <= 0:
                del statuses[key]

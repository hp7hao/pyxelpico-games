"""Pure turn-based tactics rules for the Guncho PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class Enemy:
    core: "GunchoCore"
    pos: tuple[int, int]
    kind: str
    hp: int = 1
    stun: int = 0
    killed: bool = False

    def kill(self) -> None:
        if not self.killed:
            self.killed = True
            self.core.bandits_killed += 1
            self.core.message = f"{self.kind} down"


@dataclass
class Dynamite:
    pos: tuple[int, int]
    timer: int = 3
    exploded: bool = False


class GunchoCore:
    directions = ((1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1))
    max_level = 5

    def __init__(self, seed: int = 1) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.level = 1
        self.radius = 3
        self.cells = self._make_cells(self.radius)
        self.player = (0, 0)
        self.aim = 0
        self.bullets = [True] * 6
        self.enemies: list[Enemy] = []
        self.dynamites: list[Dynamite] = []
        self.bandits_killed = 0
        self.enemy_turn_pending = False
        self.player_killed = False
        self.won = False
        self.message = "draw"
        self._populate_level()

    @staticmethod
    def _make_cells(radius: int) -> set[tuple[int, int]]:
        cells = set()
        for q in range(-radius, radius + 1):
            for r in range(-radius, radius + 1):
                if -radius <= q + r <= radius:
                    cells.add((q, r))
        return cells

    def _populate_level(self) -> None:
        self.enemies.clear()
        self.dynamites.clear()
        self.player = (0, 0)
        kinds = ["axe", "gun", "trapper", "tnt"]
        if self.level >= self.max_level:
            kinds.append("boss")
        count = min(2 + self.level, 7)
        candidates = [cell for cell in sorted(self.cells) if self.distance((0, 0), cell) >= 2]
        self.rng.shuffle(candidates)
        for index in range(count):
            kind = kinds[index % len(kinds)]
            enemy = self.add_enemy(candidates[index], kind=kind)
            if kind == "boss":
                enemy.hp = 2

    def move(self, direction: int) -> bool:
        target = self.neighbor(self.player, direction)
        if not self.is_free(target):
            self.message = "can't move"
            return False
        self.player = target
        self.aim = self.rotated_after(direction)
        self.enemy_turn_pending = True
        self.message = "moved"
        return True

    def shoot(self, direction: int) -> bool:
        direction %= 6
        self.aim = direction
        if not self.bullets[direction]:
            self.bullets[direction] = True
            self.enemy_turn_pending = True
            self.message = "reloaded"
            return True
        target = self.first_target(direction)
        if target is None:
            self.message = "no target"
            return False
        self.bullets[direction] = False
        target.hp -= 1
        if target.hp <= 0:
            target.kill()
        else:
            self.message = "boss hit"
        self.aim = self.rotated_after(direction)
        self.enemy_turn_pending = True
        return True

    def punch(self, direction: int) -> bool:
        target_pos = self.neighbor(self.player, direction)
        enemy = self.enemy_at(target_pos)
        if enemy is None:
            self.message = "nothing to punch"
            return False
        push_to = self.neighbor(target_pos, direction)
        if self.is_free(push_to):
            enemy.pos = push_to
        enemy.stun = 1
        self.enemy_turn_pending = True
        self.message = "pushed"
        return True

    def bullet_hail(self) -> bool:
        if not any(self.bullets):
            self.message = "empty"
            return False
        for direction, loaded in enumerate(list(self.bullets)):
            if loaded:
                target = self.first_target(direction)
                if target is not None:
                    target.kill()
                self.bullets[direction] = False
        self.bullets = [True] * 6
        self.enemy_turn_pending = True
        self.message = "bullet hail"
        return True

    def perform_enemy_turn(self) -> None:
        for dynamite in list(self.dynamites):
            if dynamite.exploded:
                continue
            dynamite.timer -= 1
            if dynamite.timer <= 0:
                self.explode(dynamite)
        for enemy in list(self.enemies):
            if enemy.killed:
                continue
            if enemy.stun > 0:
                enemy.stun -= 1
                continue
            if enemy.kind in {"gun", "boss"} and self.can_see(enemy.pos, self.player):
                self.player_killed = True
                self.message = "shot down"
                return
            if enemy.kind == "tnt" and self.distance(enemy.pos, self.player) == 1:
                spot = self.first_free_neighbor(enemy.pos)
                if spot is not None:
                    self.add_dynamite(spot)
                    self.message = "dynamite"
                    continue
            step = self.step_toward(enemy.pos, self.player)
            if step is not None and self.is_free(step):
                enemy.pos = step
            if self.distance(enemy.pos, self.player) == 1 and enemy.kind in {"axe", "boss"}:
                self.player_killed = True
                self.message = "cut down"
                return
        self.enemy_turn_pending = False

    def explode(self, dynamite: Dynamite) -> None:
        dynamite.exploded = True
        self.message = "kaboom"
        if self.distance(dynamite.pos, self.player) <= 1:
            self.player_killed = True
        for enemy in self.enemies:
            if not enemy.killed and self.distance(dynamite.pos, enemy.pos) <= 1:
                enemy.kill()

    def check_level_clear(self) -> bool:
        clear = all(enemy.killed for enemy in self.enemies)
        if clear:
            self.message = "camp clear"
            if self.level >= self.max_level:
                self.won = True
        return clear

    def advance_level(self) -> int:
        if not self.check_level_clear():
            return self.level
        if self.won:
            return self.level
        self.level += 1
        self.bullets = [True] * 6
        self.aim = 0
        self.enemy_turn_pending = False
        self._populate_level()
        self.message = f"camp {self.level}"
        return self.level

    def first_target(self, direction: int) -> Enemy | None:
        for cell in self.ray_cells(self.player, direction):
            enemy = self.enemy_at(cell)
            if enemy is not None and not enemy.killed:
                return enemy
        return None

    def can_see(self, start: tuple[int, int], target: tuple[int, int]) -> bool:
        for direction in range(6):
            if target in self.ray_cells(start, direction):
                return True
        return False

    def ray_cells(self, start: tuple[int, int], direction: int) -> list[tuple[int, int]]:
        cells = []
        current = start
        while True:
            current = self.neighbor(current, direction)
            if current not in self.cells:
                return cells
            cells.append(current)

    def neighbor(self, pos: tuple[int, int], direction: int) -> tuple[int, int]:
        dq, dr = self.directions[direction % 6]
        return pos[0] + dq, pos[1] + dr

    def rotated_after(self, direction: int) -> int:
        return (direction + (1 if direction in (0, 1, 5) else -1)) % 6

    def first_free_direction(self) -> int:
        for direction in range(6):
            if self.is_free(self.neighbor(self.player, direction)):
                return direction
        raise ValueError("no free direction")

    def first_free_neighbor(self, pos: tuple[int, int]) -> tuple[int, int] | None:
        for direction in range(6):
            target = self.neighbor(pos, direction)
            if self.is_free(target):
                return target
        return None

    def is_free(self, pos: tuple[int, int]) -> bool:
        return pos in self.cells and pos != self.player and self.enemy_at(pos) is None and self.dynamite_at(pos) is None

    def add_enemy(self, pos: tuple[int, int], *, kind: str) -> Enemy:
        enemy = Enemy(self, pos, kind)
        self.enemies.append(enemy)
        return enemy

    def add_dynamite(self, pos: tuple[int, int]) -> Dynamite:
        dynamite = Dynamite(pos)
        self.dynamites.append(dynamite)
        return dynamite

    def enemy_at(self, pos: tuple[int, int]) -> Enemy | None:
        for enemy in self.enemies:
            if enemy.pos == pos and not enemy.killed:
                return enemy
        return None

    def dynamite_at(self, pos: tuple[int, int]) -> Dynamite | None:
        for dynamite in self.dynamites:
            if dynamite.pos == pos and not dynamite.exploded:
                return dynamite
        return None

    def step_toward(self, start: tuple[int, int], goal: tuple[int, int]) -> tuple[int, int] | None:
        options = [self.neighbor(start, direction) for direction in range(6)]
        options = [pos for pos in options if pos in self.cells]
        if not options:
            return None
        return min(options, key=lambda pos: self.distance(pos, goal))

    @staticmethod
    def distance(a: tuple[int, int], b: tuple[int, int]) -> int:
        aq, ar = a
        bq, br = b
        return max(abs(aq - bq), abs(ar - br), abs((aq + ar) - (bq + br)))

    def restart(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

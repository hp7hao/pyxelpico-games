"""Pure turn-based campaign rules for the Shadows of Dunwich PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


Pos = tuple[int, int]


@dataclass
class Soldier:
    name: str
    pos: Pos
    level: int = 1
    hp: int = 3
    ap: int = 2
    xp: int = 0
    skill_points: int = 0
    alive: bool = True


@dataclass
class Enemy:
    pos: Pos
    kind: str
    hp: int = 1
    dead: bool = False


class ShadowsOfDunwichCore:
    width = 10
    height = 8
    max_campaign_level = 16

    def __init__(self, seed: int = 1) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.campaign_level = 1
        self.battle = 1
        self.turn = "soldiers"
        self.selected = 0
        self.victory = False
        self.defeat = False
        self.message = "enter dunwich"
        self.walls: set[Pos] = set()
        self.soldiers = [
            Soldier("Ada", (1, 5)),
            Soldier("Boone", (1, 6)),
            Soldier("Cora", (2, 6)),
        ]
        self.enemies: list[Enemy] = []
        self._build_map()
        self._spawn_enemies()

    def _build_map(self) -> None:
        self.walls = {(4, 1), (4, 2), (4, 5), (7, 3)}
        for x in range(self.width):
            self.walls.add((x, -1))
            self.walls.add((x, self.height))
        for y in range(self.height):
            self.walls.add((-1, y))
            self.walls.add((self.width, y))

    def _spawn_enemies(self) -> None:
        self.enemies.clear()
        self.add_enemy((7, 1), "cultist", 1)
        self.add_enemy((8, 4), "thrall", 1)
        if self.campaign_level >= 4:
            self.add_enemy((6, 6), "splitter", 2)
        if self.campaign_level >= 8:
            self.add_enemy((8, 6), "seer", 2)

    def add_enemy(self, pos: Pos, kind: str = "cultist", hp: int = 1) -> Enemy:
        enemy = Enemy(pos=pos, kind=kind, hp=hp)
        self.enemies.append(enemy)
        return enemy

    def living_soldiers(self) -> list[Soldier]:
        return [soldier for soldier in self.soldiers if soldier.alive]

    def living_enemies(self) -> list[Enemy]:
        return [enemy for enemy in self.enemies if not enemy.dead]

    def begin_turn(self) -> None:
        for soldier in self.living_soldiers():
            soldier.ap = 2 + (1 if soldier.level >= 3 else 0)
        self.turn = "soldiers"
        self.message = "squad ready"

    def move_soldier(self, index: int, target: Pos) -> bool:
        soldier = self.soldiers[index]
        if not soldier.alive or soldier.ap <= 0:
            self.message = "no action"
            return False
        distance = self.distance(soldier.pos, target)
        if distance < 1 or distance > 5 or not self.is_free(target):
            self.message = "bad move"
            return False
        soldier.pos = target
        soldier.ap -= 1
        self.selected = index
        self.message = f"{soldier.name} moves"
        return True

    def shoot(self, index: int, target: Pos) -> bool:
        soldier = self.soldiers[index]
        enemy = self.enemy_at(target)
        if enemy is None or not soldier.alive or soldier.ap <= 0:
            self.message = "no shot"
            return False
        if self.distance(soldier.pos, target) > self.shoot_range(soldier):
            self.message = "out of range"
            return False
        soldier.ap -= 1
        self.damage_enemy(enemy, 1 + (1 if soldier.level >= 4 else 0), soldier)
        return True

    def grenade(self, index: int, target: Pos) -> bool:
        soldier = self.soldiers[index]
        if not soldier.alive or soldier.ap < 2:
            self.message = "need two ap"
            return False
        if self.distance(soldier.pos, target) > 6:
            self.message = "too far"
            return False
        soldier.ap -= 2
        hit = False
        for enemy in list(self.living_enemies()):
            if self.distance(enemy.pos, target) <= 1:
                self.damage_enemy(enemy, 2, soldier)
                hit = True
        self.message = "grenade" if hit else "missed blast"
        return True

    def overwatch(self, index: int) -> bool:
        soldier = self.soldiers[index]
        if not soldier.alive or soldier.ap <= 0:
            self.message = "no action"
            return False
        soldier.ap = 0
        self.message = f"{soldier.name} watches"
        return True

    def damage_enemy(self, enemy: Enemy, amount: int, soldier: Soldier) -> None:
        enemy.hp -= amount
        if enemy.hp > 0:
            self.message = f"{enemy.kind} hit"
            return
        enemy.dead = True
        soldier.xp += 1
        self.message = f"{enemy.kind} banished"
        if enemy.kind == "splitter":
            self._split(enemy.pos)

    def _split(self, pos: Pos) -> None:
        spawned = 0
        for tile in self.neighbors(pos):
            if self.is_free(tile):
                self.add_enemy(tile, "spawn", 1)
                spawned += 1
            if spawned == 2:
                break

    def enemy_turn(self) -> None:
        self.turn = "enemy"
        for enemy in self.living_enemies():
            target = self.closest_soldier(enemy.pos)
            if target is None:
                break
            if self.distance(enemy.pos, target.pos) <= 1:
                target.hp -= 1 if enemy.kind != "seer" else 2
                if target.hp <= 0:
                    target.alive = False
                    self.message = f"{target.name} fell"
            else:
                step = self.step_toward(enemy.pos, target.pos)
                if step is not None and self.is_free(step):
                    enemy.pos = step
        if not self.living_soldiers():
            self.defeat = True
            self.message = "squad lost"
        else:
            self.begin_turn()

    def complete_battle(self) -> bool:
        if self.living_enemies():
            self.message = "threat remains"
            return False
        for soldier in self.soldiers:
            if soldier.alive:
                self._promote(soldier)
            else:
                self._replace(soldier)
        if self.campaign_level >= self.max_campaign_level:
            self.victory = True
            self.message = "dunwich sealed"
            return True
        self.battle += 1
        self.campaign_level = min(self.max_campaign_level, self.campaign_level + len(self.living_soldiers()))
        self.begin_turn()
        self._spawn_enemies()
        self.message = f"level {self.campaign_level}"
        return True

    def _promote(self, soldier: Soldier) -> None:
        if soldier.xp >= soldier.level:
            soldier.xp = 0
            soldier.level += 1
            soldier.skill_points += 1
            soldier.hp = min(5, soldier.hp + 1)

    def _replace(self, soldier: Soldier) -> None:
        index = self.soldiers.index(soldier) + 1
        recruit_level = max(1, self.campaign_level // 4)
        soldier.name = f"Recruit {index}"
        soldier.level = recruit_level
        soldier.hp = 3
        soldier.ap = 2
        soldier.xp = 0
        soldier.skill_points = recruit_level
        soldier.alive = True
        soldier.pos = [(1, 5), (1, 6), (2, 6)][index - 1]

    def is_free(self, pos: Pos) -> bool:
        if pos in self.walls:
            return False
        if not (0 <= pos[0] < self.width and 0 <= pos[1] < self.height):
            return False
        if any(soldier.alive and soldier.pos == pos for soldier in self.soldiers):
            return False
        return self.enemy_at(pos) is None

    def enemy_at(self, pos: Pos) -> Enemy | None:
        for enemy in self.enemies:
            if not enemy.dead and enemy.pos == pos:
                return enemy
        return None

    def closest_soldier(self, pos: Pos) -> Soldier | None:
        soldiers = self.living_soldiers()
        if not soldiers:
            return None
        return min(soldiers, key=lambda soldier: self.distance(pos, soldier.pos))

    def step_toward(self, start: Pos, target: Pos) -> Pos | None:
        options = sorted(self.neighbors(start), key=lambda tile: self.distance(tile, target))
        for tile in options:
            if self.is_free(tile):
                return tile
        return None

    def shoot_range(self, soldier: Soldier) -> int:
        return 5 + (1 if soldier.level >= 2 else 0)

    @staticmethod
    def distance(a: Pos, b: Pos) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def neighbors(pos: Pos) -> list[Pos]:
        x, y = pos
        return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    def restart(self) -> None:
        self.__init__(self.seed)

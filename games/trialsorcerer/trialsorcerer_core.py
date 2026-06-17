"""Pure dungeon-FPS rules for the Trial of the Sorcerer PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))


@dataclass
class Monster:
    x: int
    y: int
    hp: int
    kind: str = "servant"
    alive: bool = True


class TrialSorcererCore:
    width = 11
    height = 9
    final_level = 3

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.level = 1
        self.staff_power = 1
        self.max_hp = 8
        self.hp = self.max_hp
        self.keys = 0
        self.loot = 0
        self.cleared = False
        self.message = "enter the demon realm"
        self._build_level()

    def _build_level(self) -> None:
        self.start_tile = (1, 1)
        self.key_tile = (2, 3)
        self.crystal_tile = (5, 1)
        self.door_tile = (6, 3)
        self.exit_tile = (9, 7)
        self.grid = [list(row) for row in self._base_rows()]
        if self.level >= self.final_level:
            self.grid[self.exit_tile[1]][self.exit_tile[0]] = "."
        self.x, self.y = self.start_tile
        self.facing = 0
        self.pickups: dict[tuple[int, int], str] = {
            self.key_tile: "key",
            self.crystal_tile: "crystal",
            (8, 1): "potion",
        }
        self.monsters = self._spawn_monsters()
        self.message = "find keys and crystals"

    def _base_rows(self) -> tuple[str, ...]:
        return (
            "###########",
            "#....C..p.#",
            "#...#.###.#",
            "#.k...D...#",
            "#.#.#.###.#",
            "#...#.....#",
            "###.#.###.#",
            "#........E#",
            "###########",
        )

    def _spawn_monsters(self) -> list[Monster]:
        if self.level >= self.final_level:
            return [Monster(8, 1, 6 + self.level, "bahmott")]
        base_hp = 1 + self.level
        monsters = [
            Monster(4, 3, base_hp, "imp"),
            Monster(8, 5, base_hp + 1, "spider"),
        ]
        if self.level > 1:
            monsters.append(Monster(7, 7, base_hp + 1, "shade"))
        return monsters

    def tick(
        self,
        *,
        forward: bool = False,
        backward: bool = False,
        turn_left: bool = False,
        turn_right: bool = False,
        strafe: bool = False,
        shoot: bool = False,
    ) -> None:
        if self.cleared:
            return

        if shoot:
            self._shoot_staff()
        elif strafe and turn_left:
            self._try_move((self.facing - 1) % 4)
        elif strafe and turn_right:
            self._try_move((self.facing + 1) % 4)
        else:
            if turn_left:
                self.facing = (self.facing - 1) % 4
                self.message = "turn left"
            if turn_right:
                self.facing = (self.facing + 1) % 4
                self.message = "turn right"
            if forward:
                self._try_move(self.facing)
            if backward:
                self._try_move((self.facing + 2) % 4)

        self._collect_pickup()
        self._check_exit()
        self._monster_pressure()

    def _try_move(self, direction: int) -> bool:
        dx, dy = DIRS[direction]
        nx, ny = self.x + dx, self.y + dy
        tile = self.tile_at(nx, ny)
        if tile == "#":
            self.message = "stone blocks the way"
            return False
        if tile == "D":
            if self.keys <= 0:
                self.message = "need a matching key"
                return False
            self.keys -= 1
            self.grid[ny][nx] = "."
            self.message = "door unlocked"
        self.x, self.y = nx, ny
        return True

    def _shoot_staff(self) -> None:
        target = self._first_monster_in_sight()
        if target is None:
            self.message = "spell fades"
            return
        target.hp -= self.staff_power
        if target.hp <= 0:
            target.alive = False
            self.loot += 1
            if target.kind == "bahmott":
                self.cleared = True
                self.message = "bahmott defeated"
            else:
                self.message = "monster banished"
        else:
            self.message = "spell hits"

    def _first_monster_in_sight(self) -> Monster | None:
        dx, dy = DIRS[self.facing]
        x, y = self.x, self.y
        for _ in range(6):
            x += dx
            y += dy
            if self.tile_at(x, y) in ("#", "D"):
                return None
            for monster in self.monsters:
                if monster.alive and (monster.x, monster.y) == (x, y):
                    return monster
        return None

    def _collect_pickup(self) -> None:
        kind = self.pickups.pop((self.x, self.y), None)
        if kind == "key":
            self.keys += 1
            self.message = "key found"
        elif kind == "crystal":
            self.staff_power += 1
            self.message = "staff power up"
        elif kind == "potion":
            self.hp = min(self.max_hp, self.hp + 3)
            self.message = "potion restored"

    def _check_exit(self) -> None:
        if self.cleared or (self.x, self.y) != self.exit_tile:
            return
        if self.level >= self.final_level:
            return
        self.level += 1
        self._build_level()
        self.message = "deeper into the realm"

    def _monster_pressure(self) -> None:
        if self.cleared:
            return
        for monster in self.monsters:
            if not monster.alive:
                continue
            dist = abs(monster.x - self.x) + abs(monster.y - self.y)
            if dist == 1:
                self.hp = max(0, self.hp - (2 if monster.kind == "bahmott" else 1))
                self.message = f"{monster.kind} strikes"
                if self.hp == 0:
                    self._respawn()
                return

    def _respawn(self) -> None:
        self.hp = max(1, self.max_hp // 2)
        self.x, self.y = self.start_tile
        self.message = "spellbound back to start"

    def visible_ray(self, offset: int) -> tuple[int, str]:
        direction = self._ray_direction(offset)
        x, y = self.x, self.y
        for dist in range(1, 7):
            x += direction[0]
            y += direction[1]
            tile = self.tile_at(x, y)
            if tile in ("#", "D"):
                return dist, tile
        return 6, "."

    def _ray_direction(self, offset: int) -> tuple[int, int]:
        left = DIRS[(self.facing - 1) % 4]
        fwd = DIRS[self.facing]
        if offset < 0:
            return (fwd[0] + left[0], fwd[1] + left[1])
        if offset > 0:
            return (fwd[0] - left[0], fwd[1] - left[1])
        return fwd

    def player_tile(self) -> tuple[int, int]:
        return self.x, self.y

    def tile_at(self, x: int, y: int) -> str:
        if x < 0 or y < 0 or y >= len(self.grid) or x >= len(self.grid[y]):
            return "#"
        return self.grid[y][x]

    def restart(self) -> None:
        seed = self.rng.randint(0, 999_999)
        self.__init__(seed=seed)

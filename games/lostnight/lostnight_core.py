"""Pure overworld and battle rules for The Lost Night PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class Actor:
    x: float
    y: float


@dataclass
class Bullet:
    x: float
    y: float
    dx: float
    dy: float
    friendly: bool = False


@dataclass
class Enemy:
    name: str
    hp: int
    attack: int
    candy: int
    timer: int = 0


class LostNightCore:
    room_w = 96
    room_h = 80
    encounter_rooms = ((1, 0), (1, 1), (0, 1), (2, 1))

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.mode = "overworld"
        self.room = (0, 0)
        self.player = Actor(42, 42)
        self.hp = 8
        self.max_hp = 8
        self.tea = 1
        self.candy = 0
        self.power_level = 1
        self.speed_level = 1
        self.rate_level = 1
        self.cleared_rooms: set[tuple[int, int]] = set()
        self.enemy = Enemy("", 0, 0, 0)
        self.enemy_bullets: list[Bullet] = []
        self.player_bullets: list[Bullet] = []
        self.message = "find the lost night"

    def tick_overworld(
        self,
        *,
        left: bool = False,
        right: bool = False,
        up: bool = False,
        down: bool = False,
    ) -> None:
        if self.mode != "overworld":
            return
        speed = 2.0 + 0.25 * (self.speed_level - 1)
        self.player.x += (int(right) - int(left)) * speed
        self.player.y += (int(down) - int(up)) * speed
        self._wrap_room_edges()
        if self.room in self.encounter_rooms and self.room not in self.cleared_rooms:
            self.start_battle("night shape")
            self.message = "night shape appears"

    def _wrap_room_edges(self) -> None:
        rx, ry = self.room
        if self.player.x >= self.room_w:
            self.player.x = 1
            rx += 1
        elif self.player.x < 0:
            self.player.x = self.room_w - 2
            rx -= 1
        if self.player.y >= self.room_h:
            self.player.y = 1
            ry += 1
        elif self.player.y < 0:
            self.player.y = self.room_h - 2
            ry -= 1
        self.room = (max(0, min(2, rx)), max(0, min(1, ry)))

    def start_battle(self, name: str) -> None:
        self.mode = "battle"
        is_boss = name == "boss" or self.room == self.encounter_rooms[-1]
        self.enemy = Enemy("night core" if is_boss else name, 18 if is_boss else 10, 3 if is_boss else 2, 8 if is_boss else 4)
        self.player = Actor(48, 60)
        self.player_bullets = []
        self.enemy_bullets = [Bullet(48, 58, 0, 0.7)]
        self.message = f"{self.enemy.name} appears"

    def tick_battle(
        self,
        *,
        left: bool = False,
        right: bool = False,
        up: bool = False,
        down: bool = False,
    ) -> None:
        if self.mode != "battle":
            return
        speed = 1.7 + 0.2 * (self.speed_level - 1)
        self.player.x = max(12, min(84, self.player.x + (int(right) - int(left)) * speed))
        self.player.y = max(38, min(72, self.player.y + (int(down) - int(up)) * speed))
        self._update_player_bullets()
        self._update_enemy_bullets()
        self.enemy.timer += 1
        if self.enemy.timer % max(14, 30 - self.rate_level * 3) == 0:
            self._spawn_enemy_bullet()
        if self.enemy.hp <= 0:
            self._win_battle()

    def fire(self) -> None:
        if self.mode != "battle":
            return
        self.player_bullets.append(Bullet(self.player.x, self.player.y - 5, 0, -4.2, True))

    def drink_tea(self) -> None:
        if self.tea <= 0:
            self.message = "no tea left"
            return
        self.tea -= 1
        self.hp = min(self.max_hp, self.hp + 5)
        self.message = "warm tea +5hp"

    def buy_upgrade(self, stat: str) -> None:
        if self.candy < 4:
            self.message = "need more candy"
            return
        self.candy -= 4
        if stat == "power":
            self.power_level += 1
            self.message = "power up"
        elif stat == "speed":
            self.speed_level += 1
            self.message = "speed up"
        elif stat == "rate":
            self.rate_level += 1
            self.message = "rate up"
        elif stat == "hp":
            self.max_hp += 2
            self.hp = self.max_hp
            self.message = "max hp up"

    def _update_player_bullets(self) -> None:
        kept = []
        for bullet in self.player_bullets:
            bullet.x += bullet.dx
            bullet.y += bullet.dy
            if 28 <= bullet.y <= 42 and abs(bullet.x - 48) < 18:
                self.enemy.hp = max(0, self.enemy.hp - (2 + self.power_level))
                self.message = "spark lands"
            elif bullet.y > -4:
                kept.append(bullet)
        self.player_bullets = kept

    def _update_enemy_bullets(self) -> None:
        kept = []
        for bullet in self.enemy_bullets:
            bullet.x += bullet.dx
            bullet.y += bullet.dy
            if abs(bullet.x - self.player.x) < 5 and abs(bullet.y - self.player.y) < 5:
                self.hp = max(0, self.hp - self.enemy.attack)
                self.message = "hit by a spark"
            elif bullet.y < 82 and bullet.x > 6 and bullet.x < 90:
                kept.append(bullet)
        self.enemy_bullets = kept
        if self.hp <= 0:
            self._lose_battle()

    def _spawn_enemy_bullet(self) -> None:
        angle = self.enemy.timer / 7.0
        dx = 0.8 if int(angle) % 2 == 0 else -0.8
        self.enemy_bullets.append(Bullet(48, 38, dx, 1.3))

    def _win_battle(self) -> None:
        self.candy += self.enemy.candy
        self.cleared_rooms.add(self.room)
        self.player_bullets = []
        self.enemy_bullets = []
        if all(room in self.cleared_rooms for room in self.encounter_rooms):
            self.mode = "clear"
            self.message = "dawn returns"
        else:
            self.mode = "overworld"
            self.message = f"found {self.enemy.candy} candy"

    def _lose_battle(self) -> None:
        self.hp = max(1, self.max_hp // 2)
        self.tea = min(2, self.tea + 1)
        self.mode = "overworld"
        self.player_bullets = []
        self.enemy_bullets = []
        self.message = "wake up at dusk"

    def restart(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

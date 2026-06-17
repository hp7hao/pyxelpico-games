"""Pure relaxing city-builder rules for the Villager PyxelPico port."""

from __future__ import annotations

import random


BUILD_COSTS = {
    "house": {"wood": 8, "stone": 2},
    "farm": {"wood": 6, "stone": 4},
    "workshop": {"wood": 10, "stone": 8},
    "tavern": {"wood": 12, "stone": 10, "food": 4},
}


class VillagerCore:
    width = 16
    height = 12
    arrival_delay = 8
    production_interval = 10

    def __init__(self, seed: int = 1) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.cursor = (self.width // 2, self.height // 2)
        self.world: dict[tuple[int, int], str] = {}
        self.buildings: dict[tuple[int, int], str] = {}
        self.resources = {"wood": 5, "stone": 5, "food": 5}
        self.population = 0
        self.happiness = 70
        self.pending_arrivals = 0
        self.tick_count = 0
        self.message = "welcome, villager"
        self._generate_world()

    def move_cursor(self, dx: int, dy: int) -> None:
        x, y = self.cursor
        self.cursor = (max(0, min(self.width - 1, x + dx)), max(0, min(self.height - 1, y + dy)))

    def gather(self) -> str | None:
        tile = self.world.get(self.cursor, "grass")
        if tile == "tree":
            self.resources["wood"] += 4
            gained = "wood"
        elif tile == "boulder":
            self.resources["stone"] += 3
            gained = "stone"
        elif tile in ("berry", "mushroom"):
            self.resources["food"] += 3
            gained = "food"
        else:
            self.message = "nothing to gather"
            return None
        self.world[self.cursor] = "grass"
        self.message = f"gathered {gained}"
        return gained

    def build(self, kind: str) -> bool:
        if self.cursor in self.buildings:
            self.message = "space occupied"
            return False
        costs = BUILD_COSTS.get(kind)
        if costs is None:
            self.message = "unknown plan"
            return False
        if any(self.resources.get(res, 0) < amount for res, amount in costs.items()):
            self.message = "need resources"
            return False
        for res, amount in costs.items():
            self.resources[res] -= amount
        self.buildings[self.cursor] = kind
        if kind == "house":
            self.pending_arrivals += 1
            self.message = "someone may move in"
        elif kind == "tavern":
            self.happiness = min(100, self.happiness + 12)
            self.message = "cheers"
        else:
            self.message = f"built {kind}"
        return True

    def tick(self) -> None:
        self.tick_count += 1
        if self.pending_arrivals and self.tick_count % self.arrival_delay == 0:
            self.pending_arrivals -= 1
            self.population += 1
            self.message = "new peep arrived"
        if self.tick_count % self.production_interval == 0:
            self._produce()
            self._consume_food()

    def cycle_building(self, current: str, direction: int) -> str:
        order = list(BUILD_COSTS)
        index = order.index(current) if current in order else 0
        return order[(index + direction) % len(order)]

    def _produce(self) -> None:
        if self.population <= 0:
            self.message = "build a house"
            return
        multiplier = 2 if self.happiness >= 70 else 1
        for kind in self.buildings.values():
            if kind == "farm":
                self.resources["food"] += 4 * multiplier
            elif kind == "workshop":
                self.resources["wood"] += 2 * multiplier
                self.resources["stone"] += multiplier
            elif kind == "tavern":
                self.happiness = min(100, self.happiness + 2)
        self.message = "village hums"

    def _consume_food(self) -> None:
        if self.population <= 0:
            return
        if self.resources["food"] >= self.population:
            self.resources["food"] -= self.population
            self.happiness = min(100, self.happiness + 1)
        else:
            self.resources["food"] = 0
            self.happiness = max(0, self.happiness - 15)
        if self.happiness < 25 and self.population > 0:
            self.population -= 1
            self.message = "somebody left"

    def _generate_world(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                roll = self.rng.random()
                if roll < 0.12:
                    tile = "tree"
                elif roll < 0.18:
                    tile = "boulder"
                elif roll < 0.24:
                    tile = "berry"
                elif roll < 0.28:
                    tile = "mushroom"
                else:
                    tile = "grass"
                self.world[(x, y)] = tile
        self.world[self.cursor] = "grass"

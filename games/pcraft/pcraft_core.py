"""Pure island survival and crafting rules for the P.Craft PyxelPico port."""

from __future__ import annotations

from collections import Counter
import random


class PCraftCore:
    width = 12
    height = 10

    recipes = {
        "axe": {"wood": 4, "stone": 2},
        "sword": {"wood": 2, "stone": 1},
        "boat": {"wood": 8, "fiber": 3, "crystal": 1},
    }

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.spawn = (2, 2)
        self.workbench = (5, 3)
        self.cave = (9, 7)
        self.boat_site = (1, 8)
        self.inventory: Counter[str] = Counter()
        self.tools: set[str] = {"hands"}
        self.equipped = "hands"
        self.cave_cleared = False
        self.escaped = False
        self.message = "survive the island"
        self._build_island()
        self.x, self.y = self.spawn

    def _build_island(self) -> None:
        rows = [
            "~~~~~~~~~~~~",
            "~ggtgggttgg~",
            "~g@ggsggggg~",
            "~gttgWggfgg~",
            "~ggggggsggg~",
            "~gfgttggggg~",
            "~ggggggggsg~",
            "~ggfgggsgCg~",
            "~Sggggggggg~",
            "~~~~~~~~~~~~",
        ]
        mapping = {
            "~": "water",
            "g": "grass",
            "t": "tree",
            "s": "stone",
            "f": "fiber",
            "W": "workbench",
            "C": "cave",
            "S": "shore",
            "@": "grass",
        }
        self.tiles = [[mapping[ch] for ch in row] for row in rows]

    def tick(
        self,
        *,
        left: bool = False,
        right: bool = False,
        up: bool = False,
        down: bool = False,
        use: bool = False,
    ) -> None:
        if self.escaped:
            return
        if left:
            self.try_move(-1, 0)
        elif right:
            self.try_move(1, 0)
        elif up:
            self.try_move(0, -1)
        elif down:
            self.try_move(0, 1)
        if use:
            self.use_equipped()

    def try_move(self, dx: int, dy: int) -> bool:
        nx, ny = self.x + dx, self.y + dy
        tile = self.tile_at(nx, ny)
        if tile == "water":
            self.message = "too far from shore"
            return False
        self.x, self.y = nx, ny
        if tile == "workbench":
            self.message = "workbench"
        elif tile == "cave":
            self.message = "dark cave"
        elif tile == "shore":
            self.message = "build a boat"
        return True

    def use_equipped(self) -> bool:
        tile = self.tile_at(self.x, self.y)
        if tile == "tree":
            self.inventory["wood"] += 4 if "axe" in self.tools else 2
            self._set_tile(self.x, self.y, "grass")
            self.message = "gathered wood"
            return True
        if tile == "stone":
            self.inventory["stone"] += 1
            self._set_tile(self.x, self.y, "grass")
            self.message = "gathered stone"
            return True
        if tile == "fiber":
            self.inventory["fiber"] += 2
            self._set_tile(self.x, self.y, "grass")
            self.message = "gathered fiber"
            return True
        if tile == "cave":
            return self.explore_cave()
        if tile == "shore" and "boat" in self.tools:
            self.escaped = True
            self.message = "escaped the island"
            return True
        self.message = "nothing useful here"
        return False

    def craft(self, item: str) -> bool:
        if self.tile_at(self.x, self.y) != "workbench":
            self.message = "need workbench"
            return False
        recipe = self.recipes.get(item)
        if recipe is None:
            self.message = "unknown recipe"
            return False
        missing = [name for name, amount in recipe.items() if self.inventory[name] < amount]
        if missing:
            self.message = f"need {missing[0]}"
            return False
        for name, amount in recipe.items():
            self.inventory[name] -= amount
        self.tools.add(item)
        self.equipped = item
        self.message = f"crafted {item}"
        return True

    def explore_cave(self) -> bool:
        if "sword" not in self.tools:
            self.message = "need a sword"
            return False
        if not self.cave_cleared:
            self.inventory["crystal"] += 1
            self.cave_cleared = True
            self.message = "cave crystal found"
        else:
            self.message = "cave is quiet"
        return True

    def player_pos(self) -> tuple[int, int]:
        return self.x, self.y

    def move_to(self, x: int, y: int) -> None:
        self.x, self.y = x, y

    def tile_at(self, x: int, y: int) -> str:
        if y < 0 or x < 0 or y >= self.height or x >= self.width:
            return "water"
        return self.tiles[y][x]

    def _set_tile(self, x: int, y: int, tile: str) -> None:
        self.tiles[y][x] = tile

    def count_tiles(self, tile: str) -> int:
        return sum(1 for row in self.tiles for value in row if value == tile)

    def find_tile(self, tile: str) -> tuple[int, int]:
        for y, row in enumerate(self.tiles):
            for x, value in enumerate(row):
                if value == tile:
                    return x, y
        raise ValueError(f"missing tile: {tile}")

    def restart(self) -> None:
        seed = self.rng.randint(0, 999_999)
        self.__init__(seed=seed)

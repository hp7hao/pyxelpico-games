"""Pure RPG rules for the Freezing Knights PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class Knight:
    name: str
    max_hp: int
    attack: int
    stamina: int = 2
    hp: int = 0
    defense: int = 1

    def __post_init__(self) -> None:
        if self.hp == 0:
            self.hp = self.max_hp

    @property
    def alive(self) -> bool:
        return self.hp > 0


@dataclass
class Enemy:
    name: str
    max_hp: int
    attack: int
    gold: int
    hp: int = 0

    def __post_init__(self) -> None:
        if self.hp == 0:
            self.hp = self.max_hp

    @property
    def alive(self) -> bool:
        return self.hp > 0


@dataclass(frozen=True)
class MapNode:
    name: str
    kind: str
    next_indices: tuple[int, ...]
    enemies: tuple[tuple[str, int, int, int], ...] = ()


class FreezingKnightsCore:
    upgrade_cost = 6

    nodes = (
        MapNode("base camp", "safe", (1, 2)),
        MapNode("pine pass", "battle", (3, 4), (("snow scout", 9, 3, 4), ("ice archer", 7, 2, 3))),
        MapNode("hot spring", "rest", (1, 4)),
        MapNode("ridge bridge", "battle", (5,), (("shield guard", 12, 4, 6),)),
        MapNode("white chapel", "rest", (5,)),
        MapNode("corruption core", "boss", (6,), (("winter core", 22, 5, 10),)),
        MapNode("summit", "finish", ()),
    )

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.party = [Knight("frost", 22, 5), Knight("ember", 18, 4)]
        self.gold = 0
        self.potions = 3
        self.max_potions = 5
        self.current_node_index = 0
        self.last_safe_node = 0
        self.mode = "map"
        self.enemies: list[Enemy] = []
        self.turn = 1
        self.guard_quality = ""
        self.message = "choose a snowy path"

    @property
    def current_node(self) -> MapNode:
        return self.nodes[self.current_node_index]

    def available_paths(self) -> tuple[int, ...]:
        return self.current_node.next_indices

    def choose_path(self, option_index: int) -> None:
        paths = self.available_paths()
        if not paths:
            self.message = "the summit is quiet"
            return
        option_index = max(0, min(option_index, len(paths) - 1))
        self.current_node_index = paths[option_index]
        node = self.current_node
        if node.kind in {"battle", "boss"}:
            self._start_battle(node)
        elif node.kind == "rest":
            self.mode = "rest"
            self.message = f"rest at {node.name}"
        elif node.kind == "finish":
            self.mode = "clear"
            self.message = "the summit is saved"
        else:
            self.mode = "map"
            self.message = f"safe at {node.name}"

    def _start_battle(self, node: MapNode) -> None:
        self.mode = "battle"
        self.turn = 1
        self.guard_quality = ""
        self.enemies = [Enemy(name, hp, attack, gold) for name, hp, attack, gold in node.enemies]
        self._refresh_stamina()
        self.message = f"ambush at {node.name}"

    def knight_action(self, knight_index: int, action: str, target_index: int = 0) -> None:
        if self.mode != "battle":
            return
        knight = self.party[knight_index]
        if not knight.alive:
            self.message = f"{knight.name} is down"
            return
        if action == "potion":
            self.use_potion(knight_index)
            return
        if knight.stamina <= 0:
            self.message = f"{knight.name} needs a breath"
            return

        target = self._living_enemy(target_index)
        if target is None:
            self._win_battle()
            return
        damage = knight.attack + (1 if action == "strike" else 0)
        target.hp = max(0, target.hp - damage)
        knight.stamina -= 1
        self.message = f"{knight.name} hits {target.name}"
        if not target.alive:
            self.gold += target.gold
            self.message = f"{target.name} falls, {knight.name} wins {target.gold}g"
        if not any(enemy.alive for enemy in self.enemies):
            self._win_battle()

    def enemy_turn(self, defense_timing: float = 0.0) -> None:
        if self.mode != "battle":
            return
        living_party = [knight for knight in self.party if knight.alive]
        living_enemies = [enemy for enemy in self.enemies if enemy.alive]
        if not living_enemies:
            self._win_battle()
            return
        if not living_party:
            self._wipe()
            return

        guard = self._guard_value(defense_timing)
        total_damage = 0
        for index, enemy in enumerate(living_enemies):
            target = living_party[(self.turn + index) % len(living_party)]
            damage = max(1, enemy.attack - target.defense - guard)
            target.hp = max(0, target.hp - damage)
            total_damage += damage
        self.turn += 1
        self._refresh_stamina()
        if not any(knight.alive for knight in self.party):
            self._wipe()
        else:
            self.message = f"guard {self.guard_quality}: {total_damage} dmg"

    def _guard_value(self, timing: float) -> int:
        if timing >= 0.85:
            self.guard_quality = "great"
            return 3
        if timing >= 0.55:
            self.guard_quality = "good"
            return 1
        self.guard_quality = "miss"
        return 0

    def use_potion(self, knight_index: int) -> None:
        knight = self.party[knight_index]
        if self.potions <= 0:
            self.message = "no potions left"
            return
        self.potions -= 1
        knight.hp = min(knight.max_hp, knight.hp + 10)
        self.message = f"{knight.name} drinks a potion"

    def rest(self) -> None:
        if self.current_node.kind != "rest":
            return
        self.last_safe_node = self.current_node_index
        self.mode = "map"
        self.potions = min(self.max_potions, self.potions + 3)
        for knight in self.party:
            knight.hp = knight.max_hp
            knight.stamina = 2
        self.message = "warm meal, full hearts"

    def buy_upgrade(self, knight_index: int, stat: str) -> None:
        if self.mode != "rest" or self.gold < self.upgrade_cost:
            self.message = "not enough gold"
            return
        knight = self.party[knight_index]
        self.gold -= self.upgrade_cost
        if stat == "hp":
            knight.max_hp += 4
            knight.hp = knight.max_hp
            self.message = f"{knight.name} hp up"
        else:
            knight.attack += 1
            self.message = f"{knight.name} attack up"

    def _win_battle(self) -> None:
        self.enemies = []
        node = self.current_node
        if node.kind == "boss":
            self.mode = "clear"
            self.message = "the summit is saved"
        else:
            self.mode = "map"
            self.message = f"{node.name} cleared"

    def _wipe(self) -> None:
        self.current_node_index = self.last_safe_node
        self.mode = "map"
        self.potions = min(self.max_potions, self.potions + 2)
        for knight in self.party:
            knight.hp = max(1, knight.max_hp // 2)
            knight.stamina = 2
        self.enemies = []
        self.message = "rescued at last safe camp"

    def _living_enemy(self, preferred_index: int) -> Enemy | None:
        if not self.enemies:
            return None
        ordered = self.enemies[preferred_index:] + self.enemies[:preferred_index]
        for enemy in ordered:
            if enemy.alive:
                return enemy
        return None

    def _refresh_stamina(self) -> None:
        for knight in self.party:
            if knight.alive:
                knight.stamina = 2

    def restart(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

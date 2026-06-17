"""Pure state for the Two Hiking Cats PyxelPico port."""

from __future__ import annotations

import math
import random


class TwoHikingCatsCore:
    palettes = (
        (1, 13, 6, 7, "dawn"),
        (5, 6, 13, 7, "mist"),
        (2, 8, 9, 10, "sunset"),
        (0, 1, 5, 12, "moon"),
        (3, 11, 4, 15, "forest"),
    )
    default_speed = 1.0
    min_speed = 0.25
    max_speed = 3.0
    meow_interval = 36

    def __init__(self, seed: int = 1) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.speed = self.default_speed
        self.scroll = 0.0
        self.palette_index = 0
        self.frame = 0
        self.active_cat = 0
        self.current_meow = "meow"
        self.manual_meow_timer = 0
        self.message = "left/right speed"

    @property
    def palette(self) -> tuple[int, int, int, int]:
        return self.palettes[self.palette_index][:4]

    @property
    def palette_name(self) -> str:
        return str(self.palettes[self.palette_index][4])

    def adjust_speed(self, direction: int) -> None:
        self.speed = max(self.min_speed, min(self.max_speed, self.speed + direction * 0.25))
        self.message = f"speed {self.speed:.2f}"

    def randomize_palette(self) -> int:
        old = self.palette_index
        choices = [index for index in range(len(self.palettes)) if index != old]
        self.palette_index = self.rng.choice(choices)
        self.message = self.palette_name
        return self.palette_index

    def reset_view(self) -> None:
        self.speed = self.default_speed
        self.palette_index = 0
        self.message = "reset"

    def meow(self, cat: int) -> None:
        self.active_cat = max(0, min(1, cat))
        self.current_meow = "MEOW!" if self.active_cat == 0 else "meow?"
        self.manual_meow_timer = 18
        self.message = self.current_meow.lower()

    def tick(self) -> None:
        self.frame += 1
        self.scroll += self.speed
        if self.manual_meow_timer > 0:
            self.manual_meow_timer -= 1
        elif self.frame % self.meow_interval == 0:
            self.active_cat = 1 - self.active_cat
            self.current_meow = "meow" if self.active_cat == 0 else "meow?"

    def cat_positions(self) -> tuple[tuple[int, int], tuple[int, int]]:
        stride = self.frame * 0.25 * self.speed
        bob_a = int(math.sin(stride) * 3)
        bob_b = int(math.sin(stride + math.pi) * 3)
        return (82, 158 + bob_a), (126, 158 + bob_b)

    def hill_points(self, layer: int, width: int = 240) -> list[tuple[int, int]]:
        points = []
        step = 12
        base = 122 + layer * 22
        amp = 9 + layer * 4
        for x in range(-step, width + step, step):
            world = x + self.scroll * (0.15 + layer * 0.12)
            y = int(base + math.sin(world * 0.035 + layer) * amp)
            points.append((x, y))
        return points

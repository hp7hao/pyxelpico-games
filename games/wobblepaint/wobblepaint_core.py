"""Pure drawing-toy rules for the Wobblepaint PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
import math
import random


@dataclass
class Stroke:
    x: int
    y: int
    color: int
    group: int
    phase: float


class WobblepaintCore:
    width = 128
    height = 128

    def __init__(self, seed: int = 1) -> None:
        self.seed = seed
        self.rng = random.Random(seed)
        self.cursor = (64, 64)
        self.brush_size = 1
        self.color = 10
        self.background = 1
        self.strokes: list[Stroke] = []
        self.group = 0
        self.message = "wobblepaint"

    def move_cursor(self, dx: int, dy: int) -> None:
        x, y = self.cursor
        self.cursor = (max(0, min(self.width - 1, x + dx)), max(0, min(self.height - 1, y + dy)))

    def paint(self) -> int:
        self.group += 1
        before = len(self.strokes)
        cx, cy = self.cursor
        radius = self.brush_size
        for y in range(cy - radius, cy + radius + 1):
            for x in range(cx - radius, cx + radius + 1):
                if 0 <= x < self.width and 0 <= y < self.height and abs(x - cx) + abs(y - cy) <= radius:
                    self.strokes.append(Stroke(x, y, self.color, self.group, self.rng.random() * math.tau))
        self.message = "paint"
        return len(self.strokes) - before

    def undo(self) -> bool:
        if not self.strokes:
            self.message = "nothing to undo"
            return False
        group = self.strokes[-1].group
        self.strokes = [stroke for stroke in self.strokes if stroke.group != group]
        self.message = "undo"
        return True

    def clear(self) -> None:
        self.strokes.clear()
        self.group = 0
        self.message = "clear"

    def adjust_brush(self, delta: int) -> None:
        self.brush_size = max(1, min(6, self.brush_size + delta))
        self.message = f"brush {self.brush_size}"

    def cycle_color(self, delta: int) -> None:
        palette = [10, 11, 12, 8, 9, 14, 7, 6, 13]
        index = palette.index(self.color) if self.color in palette else 0
        self.color = palette[(index + delta) % len(palette)]
        self.message = f"color {self.color}"

    def animated_points(self, frame: int) -> list[tuple[int, int, int]]:
        points = []
        for stroke in self.strokes:
            wobble_x = int(round(math.sin(frame * 0.17 + stroke.phase) * 1.5))
            wobble_y = int(round(math.cos(frame * 0.13 + stroke.phase) * 1.5))
            points.append((stroke.x + wobble_x, stroke.y + wobble_y, stroke.color))
        return points

    def restart(self) -> None:
        self.__init__(self.seed)

"""Pure microgame-rush rules for the PICOWARE PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import random


class RoundState(Enum):
    TITLE = "title"
    PLAYING = "playing"
    RESULT = "result"
    GAME_OVER = "game_over"


class MicroKind(Enum):
    TAP_TARGET = "tap_target"
    DODGE = "dodge"
    MASH = "mash"


@dataclass
class Microgame:
    kind: MicroKind
    prompt: str
    target: str
    duration: int
    progress: int = 0
    goal: int = 1


class PicowareCore:
    result_delay = 24
    buttons = ("up", "down", "left", "right", "a", "b")

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.state = RoundState.TITLE
        self.lives = 4
        self.score = 0
        self.round_index = 0
        self.time_left = 0
        self.result_timer = 0
        self.success = False
        self.current: Microgame | None = None

    def start(self) -> None:
        self.lives = 4
        self.score = 0
        self.round_index = 0
        self._next_microgame()

    def force_microgame(self, kind: MicroKind, target: str, duration: int = 45) -> None:
        prompt = self._prompt_for(kind, target)
        goal = 5 if kind is MicroKind.MASH else 1
        self.current = Microgame(kind=kind, prompt=prompt, target=target, duration=duration, goal=goal)
        self.time_left = duration
        self.result_timer = 0
        self.success = False
        self.state = RoundState.PLAYING
        if self.round_index == 0:
            self.round_index = 1

    def input_press(self, button: str) -> None:
        if self.state is not RoundState.PLAYING or self.current is None:
            return
        micro = self.current
        if micro.kind is MicroKind.TAP_TARGET:
            if button == micro.target:
                self._finish(True)
        elif micro.kind is MicroKind.DODGE:
            if button == micro.target:
                self._finish(False)
        elif micro.kind is MicroKind.MASH and button == micro.target:
            micro.progress += 1
            if micro.progress >= micro.goal:
                self._finish(True)

    def tick(self) -> None:
        if self.state is RoundState.PLAYING:
            self.time_left -= 1
            if self.time_left <= 0:
                self._finish(self.current is not None and self.current.kind is MicroKind.DODGE)
        elif self.state is RoundState.RESULT:
            self.result_timer -= 1
            if self.result_timer <= 0:
                if self.lives <= 0:
                    self.state = RoundState.GAME_OVER
                else:
                    self._next_microgame()

    def _finish(self, success: bool) -> None:
        if self.state is not RoundState.PLAYING:
            return
        self.success = success
        if success:
            self.score += 1
        else:
            self.lives -= 1
        self.result_timer = self.result_delay
        self.state = RoundState.RESULT

    def _next_microgame(self) -> None:
        self.round_index += 1
        duration = max(24, 54 - self.score * 2)
        kind = self.rng.choice(tuple(MicroKind))
        target = self.rng.choice(self.buttons)
        self.force_microgame(kind, target, duration=duration)

    @staticmethod
    def _prompt_for(kind: MicroKind, target: str) -> str:
        if kind is MicroKind.TAP_TARGET:
            return f"press {target.upper()}"
        if kind is MicroKind.DODGE:
            return f"avoid {target.upper()}"
        return f"mash {target.upper()}"

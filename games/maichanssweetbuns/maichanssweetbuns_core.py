"""Pure bakery order rules for the Mai-Chan's Sweet Buns PyxelPico port."""

from __future__ import annotations

from enum import Enum
import random


class BunKind(Enum):
    PLAIN = "plain"
    JAM = "jam"
    CHOCOLATE = "chocolate"
    TEA = "tea"


class OrderState(Enum):
    PLAYING = "playing"
    READY = "ready"
    GAME_OVER = "game_over"


class BakeryCore:
    max_patience = 5

    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.day = 1
        self.score = 0
        self.patience = self.max_patience
        self.timer = 45
        self.state = OrderState.PLAYING
        self.order: list[BunKind] = []
        self.tray: list[BunKind] = []
        self.message = "make buns"
        self._new_order()

    def reset(self) -> None:
        self.__init__(seed=self.rng.randint(0, 999_999))

    def set_order(self, order: list[BunKind]) -> None:
        self.order = list(order)
        self.tray = []
        self.timer = 45
        self.patience = self.max_patience
        self.state = OrderState.PLAYING
        self.message = "order up"

    def choose(self, bun: BunKind) -> None:
        if self.state is not OrderState.PLAYING:
            return
        expected = self.order[len(self.tray)] if len(self.tray) < len(self.order) else None
        if bun is not expected:
            self.patience -= 1
            self.tray = []
            self.message = "wrong bun"
            if self.patience <= 0:
                self.state = OrderState.GAME_OVER
            return
        self.tray.append(bun)
        self.message = "sweet"
        if len(self.tray) == len(self.order):
            self.state = OrderState.READY
            self.message = "serve it"

    def serve(self) -> None:
        if self.state is not OrderState.READY:
            return
        self.score += 10
        self.day += 1
        self.patience = min(self.max_patience, self.patience + 1)
        self._new_order()

    def tick(self) -> None:
        if self.state is not OrderState.PLAYING:
            return
        self.timer -= 1
        if self.timer <= 0:
            self.patience -= 1
            self.tray = []
            if self.patience <= 0:
                self.state = OrderState.GAME_OVER
                self.message = "closed"
            else:
                self.timer = 45
                self.message = "too slow"

    def _new_order(self) -> None:
        length = 1 + min(3, self.day // 3)
        kinds = tuple(BunKind)
        self.order = [self.rng.choice(kinds) for _ in range(length)]
        self.tray = []
        self.timer = max(24, 48 - self.day)
        self.state = OrderState.PLAYING
        self.message = "order up"

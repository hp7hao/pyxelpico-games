"""Pure game rules for the High Stakes PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import random


class Result(Enum):
    CONTINUE = "continue"
    WON = "won"
    LOST = "lost"


@dataclass
class Card:
    pos: int
    value: int
    hidden: bool = True
    marks: list[str] = field(default_factory=list)

    @property
    def is_vampire(self) -> bool:
        return self.value == 10


class HighStakesCore:
    def __init__(self, seed: int = 1) -> None:
        self.rng = random.Random(seed)
        self.round = 1
        self.max_rounds = 5
        self.multiplier = 1
        self.stakes = 0
        self.result = Result.CONTINUE
        self.hints_left = 2
        self.stabs_left = 1
        self.cards: list[Card] = []
        self.deal()

    def reset(self) -> None:
        seed = self.rng.randint(0, 999_999)
        self.__init__(seed=seed)

    def deal(self) -> None:
        values = list(range(2, 11))
        self.rng.shuffle(values)
        self.cards = [Card(pos=index + 1, value=value) for index, value in enumerate(values)]
        safe_cards = [card for card in self.cards if not card.is_vampire]
        self.rng.choice(safe_cards).hidden = False
        self.result = Result.CONTINUE
        self.stakes = 0

    def card_at(self, pos: int) -> Card:
        if not 1 <= pos <= 9:
            raise ValueError(f"card position out of range: {pos}")
        return self.cards[pos - 1]

    def flip(self, pos: int) -> Result:
        if self.result is not Result.CONTINUE:
            return self.result
        card = self.card_at(pos)
        if not card.hidden:
            return Result.CONTINUE
        card.hidden = False
        if card.is_vampire:
            self.result = Result.LOST
            return self.result
        self.stakes += card.value * self.multiplier
        if self._all_safe_cards_revealed():
            self.result = Result.WON
        return self.result

    def place_hint_token(self, threshold: int) -> list[int]:
        if self.hints_left <= 0:
            return []
        threshold = max(2, min(9, threshold))
        marked = []
        for card in self.cards:
            if card.hidden and card.value >= threshold:
                label = f">={threshold}"
                if label not in card.marks:
                    card.marks.append(label)
                marked.append(card.pos)
        self.hints_left -= 1
        return marked

    def stab(self, pos: int) -> Result:
        if self.result is not Result.CONTINUE:
            return self.result
        if self.stabs_left <= 0:
            return Result.CONTINUE
        self.stabs_left -= 1
        card = self.card_at(pos)
        card.hidden = False
        if card.is_vampire:
            self.stakes += self.hidden_safe_count() * 3 * self.multiplier
            self.result = Result.WON
        else:
            self.result = Result.LOST
        return self.result

    def pass_round(self) -> Result:
        if self.result is not Result.CONTINUE:
            return self.result
        vampire = next(card for card in self.cards if card.is_vampire)
        if vampire.hidden:
            self.stakes += max(1, self.hidden_safe_count()) * self.multiplier
            self.result = Result.WON
        else:
            self.result = Result.LOST
        return self.result

    def payout(self) -> int:
        if self.result is Result.WON:
            return max(1, self.stakes) * self.multiplier
        if self.result is Result.LOST:
            return -max(1, self.stakes or 5)
        return self.stakes

    def hidden_safe_count(self) -> int:
        return sum(1 for card in self.cards if card.hidden and not card.is_vampire)

    def _all_safe_cards_revealed(self) -> bool:
        return all(not card.hidden for card in self.cards if not card.is_vampire)

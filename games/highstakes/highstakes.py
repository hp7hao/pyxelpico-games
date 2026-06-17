"""High Stakes — PyxelPico port.

Adapted from the PICO-8 cart by Krystian Majewski / Lazy Devs (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=40099
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from highstakes_core import HighStakesCore, Result  # noqa: E402


SCREEN = 240
CARD_W = 42
CARD_H = 54
BOARD_X = 43
BOARD_Y = 38
GAP = 10
TOOLS = ("flip", "hint", "stab")


class HighStakes:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="High Stakes", fps=30)
        self.core = HighStakesCore()
        self.cursor = 1
        self.tool_index = 0
        self.mode = "title"
        self.message = ""
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3e3g3", "t", "6", "n", 8)
        pyxel.sound(1).set("g2c3", "s", "7", "f", 14)
        pyxel.sound(2).set("c2", "n", "7", "f", 18)

    def reset(self) -> None:
        self.core.reset()
        self.cursor = next(card.pos for card in self.core.cards if card.hidden)
        self.tool_index = 0
        self.mode = "play"
        self.message = "find the vampire"

    def update(self) -> None:
        if self.mode == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            return
        if self.mode in {"won", "lost"}:
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            elif ih.btnp_b() or ih.btnp_select():
                self.mode = "title"
            return

        old_cursor = self.cursor
        col = (self.cursor - 1) % 3
        row = (self.cursor - 1) // 3
        if ih.btnp_left():
            col = max(0, col - 1)
        elif ih.btnp_right():
            col = min(2, col + 1)
        elif ih.btnp_up():
            row = max(0, row - 1)
        elif ih.btnp_down():
            row = min(2, row + 1)
        self.cursor = row * 3 + col + 1
        if self.cursor != old_cursor:
            pyxel.play(3, 0)

        if ih.btnp_b() or ih.btnp_select():
            self.tool_index = (self.tool_index + 1) % len(TOOLS)
            pyxel.play(3, 0)
        if ih.btnp_start():
            self._finish(self.core.pass_round(), "passed")
        if ih.btnp_a():
            self._act()

    def _act(self) -> None:
        tool = TOOLS[self.tool_index]
        if tool == "flip":
            result = self.core.flip(self.cursor)
            self._finish(result, "flipped")
        elif tool == "hint":
            marked = self.core.place_hint_token(7)
            self.message = f"marked {len(marked)} high cards" if marked else "no hint tokens"
            pyxel.play(3, 0)
        else:
            self._finish(self.core.stab(self.cursor), "stabbed")

    def _finish(self, result: Result, verb: str) -> None:
        if result is Result.WON:
            self.mode = "won"
            self.message = f"{verb}: +{self.core.payout()} ml"
            pyxel.play(3, 0)
        elif result is Result.LOST:
            self.mode = "lost"
            self.message = f"{verb}: {self.core.payout()} ml"
            pyxel.play(3, 2)
        else:
            self.message = verb
            pyxel.play(3, 1)

    def draw(self) -> None:
        pyxel.cls(0)
        if self.mode == "title":
            self._draw_title()
            return
        self._draw_table()
        self._draw_hud()
        if self.mode == "won":
            self._panel("round won", self.message)
        elif self.mode == "lost":
            self._panel("vampire wins", self.message)

    def _draw_title(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        self._center("high stakes", 44, 8)
        self._center("krystman / lazy devs", 58, 6)
        for index, value in enumerate((10, 7, 4)):
            self._draw_card(58 + index * 44, 90, value, hidden=index != 0, selected=False, marks=[])
        self._center("flip cards, use hints", 166, 7)
        self._center("stab the vampire", 178, 7)
        if pyxel.frame_count % 30 < 22:
            self._center("press A", 204, 11)

    def _draw_table(self) -> None:
        pyxel.rect(0, 0, SCREEN, SCREEN, 1)
        pyxel.rect(25, 25, 190, 178, 5)
        pyxel.rectb(25, 25, 190, 178, 13)
        for card in self.core.cards:
            x, y = self._card_xy(card.pos)
            self._draw_card(x, y, card.value, card.hidden, self.cursor == card.pos, card.marks)

    def _draw_hud(self) -> None:
        tool = TOOLS[self.tool_index]
        pyxel.text(8, 8, f"tool {tool}", 7)
        pyxel.text(84, 8, f"stakes {self.core.stakes}ml", 7)
        pyxel.text(174, 8, f"hints {self.core.hints_left}", 7)
        pyxel.text(8, 215, "A act  B tool  START pass", 6)
        pyxel.text(8, 226, self.message[:54], 10)

    def _draw_card(self, x: int, y: int, value: int, hidden: bool, selected: bool, marks: list[str]) -> None:
        pyxel.rect(x + 2, y + 3, CARD_W, CARD_H, 1)
        pyxel.rect(x, y, CARD_W, CARD_H, 7 if not hidden else 2)
        pyxel.rectb(x, y, CARD_W, CARD_H, 0)
        if hidden:
            pyxel.rect(x + 5, y + 5, CARD_W - 10, CARD_H - 10, 8)
            pyxel.text(x + 13, y + 23, "?", 7)
        else:
            if value == 10:
                pyxel.text(x + 8, y + 14, "VAMP", 8)
                pyxel.circ(x + 21, y + 34, 8, 8)
                pyxel.pset(x + 18, y + 31, 0)
                pyxel.pset(x + 24, y + 31, 0)
            else:
                pyxel.text(x + 17, y + 22, str(value), 0)
        if marks:
            pyxel.text(x + 4, y + CARD_H - 9, ",".join(marks)[-8:], 10)
        if selected:
            pyxel.rectb(x - 2, y - 2, CARD_W + 4, CARD_H + 4, 10 if pyxel.frame_count % 20 < 14 else 9)

    def _panel(self, title: str, subtitle: str) -> None:
        pyxel.rect(30, 91, 180, 58, 0)
        pyxel.rectb(30, 91, 180, 58, 7)
        self._center(title, 108, 11)
        self._center(subtitle[:38], 128, 6)
        self._center("A retry  B title", 138, 6)

    @staticmethod
    def _card_xy(pos: int) -> tuple[int, int]:
        index = pos - 1
        return BOARD_X + (index % 3) * (CARD_W + GAP), BOARD_Y + (index // 3) * (CARD_H + GAP)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    HighStakes()

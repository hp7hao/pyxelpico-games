"""Pico Checkmate - PyxelPico port.

Adapted from the PICO-8 chess cart by Krystman (CC BY-NC-SA 4.0).
Original BBS thread: https://www.lexaloffle.com/bbs/?tid=31213
"""

from __future__ import annotations

import os
import sys

import pyxel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "lib"))
import input_helper as ih  # noqa: E402

from picocheckmate_core import BLACK, WHITE, PicoCheckmateCore  # noqa: E402


SCREEN = 240
BOARD = 176
CELL = BOARD // 8
BX = 32
BY = 40
PIECE_LABELS = {
    "K": "K",
    "Q": "Q",
    "R": "R",
    "B": "B",
    "N": "N",
    "P": "P",
    "k": "k",
    "q": "q",
    "r": "r",
    "b": "b",
    "n": "n",
    "p": "p",
}


class PicoCheckmate:
    def __init__(self) -> None:
        pyxel.init(SCREEN, SCREEN, title="Pico Checkmate", fps=30)
        self.core = PicoCheckmateCore()
        self.screen = "title"
        self.cursor = (4, 6)
        self.selected: tuple[int, int] | None = None
        self.flash = 0
        self.ai_delay = 0
        self._setup_audio()
        pyxel.run(self.update, self.draw)

    def _setup_audio(self) -> None:
        pyxel.sound(0).set("c3e3g3", "t", "5", "n", 8)
        pyxel.sound(1).set("c4g4", "p", "6", "f", 8)
        pyxel.sound(2).set("c2", "n", "7", "f", 8)
        pyxel.sound(3).set("g4e4c4", "s", "5", "n", 10)

    def reset(self) -> None:
        self.core.restart()
        self.cursor = (4, 6)
        self.selected = None
        self.screen = "play"
        self.ai_delay = 0

    def update(self) -> None:
        if self.flash > 0:
            self.flash -= 1
        if self.screen == "title":
            if ih.btnp_a() or ih.btnp_start():
                self.screen = "play"
                pyxel.play(3, 0)
            return
        if self.core.checkmate or self.core.stalemate:
            if ih.btnp_a() or ih.btnp_start():
                self.reset()
            elif ih.btnp_select():
                self.screen = "title"
            return
        if self.core.turn == BLACK:
            self._update_ai()
            return
        self._update_player()

    def _update_ai(self) -> None:
        self.ai_delay += 1
        if self.ai_delay < 16:
            return
        self.ai_delay = 0
        move = self.core.choose_ai_move()
        if move is not None:
            self.core.move(*move)
            self.cursor = move[1]
            self.flash = 3
            pyxel.play(3, 1)

    def _update_player(self) -> None:
        x, y = self.cursor
        if ih.btnp_left(8, 3):
            x = max(0, x - 1)
        if ih.btnp_right(8, 3):
            x = min(7, x + 1)
        if ih.btnp_up(8, 3):
            y = max(0, y - 1)
        if ih.btnp_down(8, 3):
            y = min(7, y + 1)
        self.cursor = (x, y)
        if ih.btnp_b():
            self.selected = None
            pyxel.play(3, 0)
        if ih.btnp_select():
            self.reset()
        if ih.btnp_a():
            if self.selected is None:
                piece = self.core.piece_at(self.cursor)
                if piece and piece.isupper():
                    self.selected = self.cursor
                    pyxel.play(3, 0)
            else:
                if self.core.move(self.selected, self.cursor):
                    self.selected = None
                    self.flash = 3
                    pyxel.play(3, 1)
                else:
                    pyxel.play(3, 2)

    def draw(self) -> None:
        pyxel.cls(5 if self.flash else 1)
        if self.screen == "title":
            self._draw_title()
        else:
            self._draw_play()

    def _draw_title(self) -> None:
        self._draw_board(32, 56, 22, decorative=True)
        self._center("pico checkmate", 34, 7)
        self._center("Krystman", 50, 13)
        self._center("A start", 212, 10 if pyxel.frame_count % 30 < 22 else 6)

    def _draw_play(self) -> None:
        self._draw_status()
        self._draw_board(BX, BY, CELL)
        self._draw_pieces()
        self._draw_cursor()
        pyxel.text(18, 224, "D-pad move  A select/move  B cancel  Select restart", 7)

    def _draw_status(self) -> None:
        pyxel.rect(0, 0, SCREEN, 34, 0)
        pyxel.text(8, 8, "Pico Checkmate", 7)
        pyxel.text(130, 8, "white: you", 10)
        pyxel.text(130, 20, "black: ai", 13)
        msg = self.core.message
        if self.core.checkmate:
            msg = f"checkmate - {self.core.winner} wins"
        elif self.core.stalemate:
            msg = "stalemate"
        pyxel.text(8, 22, msg[:29], 6 if self.core.turn == WHITE else 13)

    def _draw_board(self, x0: int, y0: int, cell: int, decorative: bool = False) -> None:
        for y in range(8):
            for x in range(8):
                color = 7 if (x + y) % 2 == 0 else 4
                pyxel.rect(x0 + x * cell, y0 + y * cell, cell, cell, color)
        pyxel.rectb(x0 - 1, y0 - 1, cell * 8 + 2, cell * 8 + 2, 0)
        if decorative:
            for x, y, piece in ((4, 7, "K"), (3, 0, "q"), (0, 6, "P"), (7, 1, "p"), (1, 7, "N"), (6, 0, "n")):
                self._draw_piece_at(piece, x0 + x * cell + cell // 2, y0 + y * cell + cell // 2, cell)

    def _draw_pieces(self) -> None:
        for y in range(8):
            for x in range(8):
                piece = self.core.piece_at((x, y))
                if piece:
                    self._draw_piece_at(piece, BX + x * CELL + CELL // 2, BY + y * CELL + CELL // 2, CELL)

    def _draw_piece_at(self, piece: str, cx: int, cy: int, cell: int) -> None:
        fill = 10 if piece.isupper() else 2
        ink = 0 if piece.isupper() else 7
        pyxel.circ(cx, cy, max(6, cell // 3), fill)
        pyxel.text(cx - 2, cy - 3, PIECE_LABELS[piece], ink)

    def _draw_cursor(self) -> None:
        x, y = self.cursor
        color = 10 if pyxel.frame_count % 20 < 14 else 7
        pyxel.rectb(BX + x * CELL, BY + y * CELL, CELL, CELL, color)
        if self.selected is not None:
            sx, sy = self.selected
            pyxel.rectb(BX + sx * CELL + 2, BY + sy * CELL + 2, CELL - 4, CELL - 4, 8)
            for move in self.core.legal_moves_for(self.selected):
                mx, my = move.dst
                pyxel.circ(BX + mx * CELL + CELL // 2, BY + my * CELL + CELL // 2, 3, 11)

    @staticmethod
    def _center(text: str, y: int, color: int) -> None:
        pyxel.text((SCREEN - len(text) * 4) // 2, y, text, color)


if __name__ == "__main__":
    PicoCheckmate()

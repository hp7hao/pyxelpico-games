"""Pure chess rules for the Pico Checkmate PyxelPico port."""

from __future__ import annotations

from dataclasses import dataclass


WHITE = "white"
BLACK = "black"
VALUES = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 99}


@dataclass(frozen=True)
class MoveInfo:
    src: tuple[int, int]
    dst: tuple[int, int]
    promotion: str | None = None
    castle: bool = False
    en_passant: bool = False


class PicoCheckmateCore:
    def __init__(self) -> None:
        self.board: list[list[str | None]] = [
            list("rnbqkbnr"),
            list("pppppppp"),
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            list("PPPPPPPP"),
            list("RNBQKBNR"),
        ]
        self.turn = WHITE
        self.castling = {WHITE: {"K": True, "Q": True}, BLACK: {"K": True, "Q": True}}
        self.en_passant_target: tuple[int, int] | None = None
        self.winner: str | None = None
        self.checkmate = False
        self.stalemate = False
        self.message = "white to move"

    @classmethod
    def empty(cls) -> "PicoCheckmateCore":
        core = cls()
        core.board = [[None] * 8 for _ in range(8)]
        core.castling = {WHITE: {"K": True, "Q": True}, BLACK: {"K": True, "Q": True}}
        core.en_passant_target = None
        core.turn = WHITE
        core.message = "white to move"
        return core

    def piece_at(self, pos: tuple[int, int]) -> str | None:
        x, y = pos
        if not self._inside(x, y):
            return None
        return self.board[y][x]

    def set_piece(self, pos: tuple[int, int], piece: str | None) -> None:
        x, y = pos
        self.board[y][x] = piece

    def move(self, src: tuple[int, int], dst: tuple[int, int]) -> bool:
        legal = self.legal_moves_for(src)
        selected = next((move for move in legal if move.dst == dst), None)
        if selected is None:
            if self.piece_at(src) and self._pseudo_move_for(src, dst) and self._would_check(selected or MoveInfo(src, dst)):
                self.message = "king would be in check"
            else:
                self.message = "illegal move"
            return False
        self._apply_move(selected)
        self.turn = self._other(self.turn)
        self._refresh_game_state()
        return True

    def legal_moves_for(self, src: tuple[int, int]) -> list[MoveInfo]:
        piece = self.piece_at(src)
        if piece is None or self._color(piece) != self.turn:
            return []
        moves = self._pseudo_moves(src)
        return [move for move in moves if not self._would_check(move)]

    def all_legal_moves(self, color: str | None = None) -> list[MoveInfo]:
        old_turn = self.turn
        if color is not None:
            self.turn = color
        moves: list[MoveInfo] = []
        for y in range(8):
            for x in range(8):
                moves.extend(self.legal_moves_for((x, y)))
        self.turn = old_turn
        return moves

    def choose_ai_move(self) -> tuple[tuple[int, int], tuple[int, int]] | None:
        moves = self.all_legal_moves(self.turn)
        if not moves:
            return None

        def score(move: MoveInfo) -> tuple[int, int]:
            captured = self.piece_at(move.dst)
            capture_score = VALUES.get(captured.lower(), 0) if captured else 0
            if move.en_passant:
                capture_score = VALUES["p"]
            center = 8 - abs(move.dst[0] - 3) - abs(move.dst[1] - 3)
            return capture_score, center

        best = max(moves, key=score)
        return best.src, best.dst

    def _pseudo_move_for(self, src: tuple[int, int], dst: tuple[int, int]) -> bool:
        return any(move.dst == dst for move in self._pseudo_moves(src))

    def _pseudo_moves(self, src: tuple[int, int]) -> list[MoveInfo]:
        piece = self.piece_at(src)
        if piece is None:
            return []
        kind = piece.lower()
        if kind == "p":
            return self._pawn_moves(src, piece)
        if kind == "n":
            return self._jump_moves(src, piece, ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)))
        if kind == "b":
            return self._slide_moves(src, piece, ((1, 1), (1, -1), (-1, -1), (-1, 1)))
        if kind == "r":
            return self._slide_moves(src, piece, ((1, 0), (0, 1), (-1, 0), (0, -1)))
        if kind == "q":
            return self._slide_moves(src, piece, ((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)))
        if kind == "k":
            return self._king_moves(src, piece)
        return []

    def _pawn_moves(self, src: tuple[int, int], piece: str) -> list[MoveInfo]:
        x, y = src
        color = self._color(piece)
        step = -1 if color == WHITE else 1
        start_y = 6 if color == WHITE else 1
        promote_y = 0 if color == WHITE else 7
        moves: list[MoveInfo] = []
        one = (x, y + step)
        if self._inside(*one) and self.piece_at(one) is None:
            moves.append(MoveInfo(src, one, "Q" if one[1] == promote_y and color == WHITE else "q" if one[1] == promote_y else None))
            two = (x, y + step * 2)
            if y == start_y and self.piece_at(two) is None:
                moves.append(MoveInfo(src, two))
        for dx in (-1, 1):
            dst = (x + dx, y + step)
            target = self.piece_at(dst)
            if target is not None and self._color(target) != color:
                moves.append(MoveInfo(src, dst, "Q" if dst[1] == promote_y and color == WHITE else "q" if dst[1] == promote_y else None))
            elif dst == self.en_passant_target:
                moves.append(MoveInfo(src, dst, en_passant=True))
        return moves

    def _jump_moves(self, src: tuple[int, int], piece: str, offsets: tuple[tuple[int, int], ...]) -> list[MoveInfo]:
        color = self._color(piece)
        moves = []
        for dx, dy in offsets:
            dst = (src[0] + dx, src[1] + dy)
            if self._inside(*dst) and self._can_land(dst, color):
                moves.append(MoveInfo(src, dst))
        return moves

    def _slide_moves(self, src: tuple[int, int], piece: str, dirs: tuple[tuple[int, int], ...]) -> list[MoveInfo]:
        color = self._color(piece)
        moves = []
        for dx, dy in dirs:
            x, y = src[0] + dx, src[1] + dy
            while self._inside(x, y):
                target = self.piece_at((x, y))
                if target is None:
                    moves.append(MoveInfo(src, (x, y)))
                else:
                    if self._color(target) != color:
                        moves.append(MoveInfo(src, (x, y)))
                    break
                x += dx
                y += dy
        return moves

    def _king_moves(self, src: tuple[int, int], piece: str) -> list[MoveInfo]:
        moves = self._jump_moves(src, piece, ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)))
        color = self._color(piece)
        y = 7 if color == WHITE else 0
        if src == (4, y) and not self.is_in_check(color):
            if self.castling[color]["K"] and self.piece_at((5, y)) is None and self.piece_at((6, y)) is None and self.piece_at((7, y)) in ("R", "r"):
                if not self._square_attacked((5, y), self._other(color)) and not self._square_attacked((6, y), self._other(color)):
                    moves.append(MoveInfo(src, (6, y), castle=True))
            if self.castling[color]["Q"] and self.piece_at((1, y)) is None and self.piece_at((2, y)) is None and self.piece_at((3, y)) is None and self.piece_at((0, y)) in ("R", "r"):
                if not self._square_attacked((3, y), self._other(color)) and not self._square_attacked((2, y), self._other(color)):
                    moves.append(MoveInfo(src, (2, y), castle=True))
        return moves

    def _apply_move(self, move: MoveInfo) -> None:
        piece = self.piece_at(move.src)
        assert piece is not None
        captured = self.piece_at(move.dst)
        self.set_piece(move.src, None)
        if move.en_passant:
            self.set_piece((move.dst[0], move.src[1]), None)
        self.set_piece(move.dst, move.promotion or piece)
        if move.castle:
            y = move.src[1]
            if move.dst[0] == 6:
                self.set_piece((5, y), self.piece_at((7, y)))
                self.set_piece((7, y), None)
            else:
                self.set_piece((3, y), self.piece_at((0, y)))
                self.set_piece((0, y), None)
        self._update_castling_rights(piece, move.src, captured, move.dst)
        self.en_passant_target = None
        if piece.lower() == "p" and abs(move.dst[1] - move.src[1]) == 2:
            self.en_passant_target = (move.src[0], (move.src[1] + move.dst[1]) // 2)

    def _update_castling_rights(self, piece: str, src: tuple[int, int], captured: str | None, dst: tuple[int, int]) -> None:
        color = self._color(piece)
        if piece.lower() == "k":
            self.castling[color]["K"] = False
            self.castling[color]["Q"] = False
        if piece.lower() == "r":
            self._clear_rook_right(src, color)
        if captured and captured.lower() == "r":
            self._clear_rook_right(dst, self._color(captured))

    def _clear_rook_right(self, pos: tuple[int, int], color: str) -> None:
        if pos == ((7, 7) if color == WHITE else (7, 0)):
            self.castling[color]["K"] = False
        if pos == ((0, 7) if color == WHITE else (0, 0)):
            self.castling[color]["Q"] = False

    def _would_check(self, move: MoveInfo) -> bool:
        snapshot = self._snapshot()
        self._apply_move(move)
        in_check = self.is_in_check(self._color(self.piece_at(move.dst) or "P"))
        self._restore(snapshot)
        return in_check

    def is_in_check(self, color: str) -> bool:
        king = "K" if color == WHITE else "k"
        for y in range(8):
            for x in range(8):
                if self.board[y][x] == king:
                    return self._square_attacked((x, y), self._other(color))
        return False

    def _square_attacked(self, square: tuple[int, int], by_color: str) -> bool:
        for y in range(8):
            for x in range(8):
                piece = self.piece_at((x, y))
                if piece is None or self._color(piece) != by_color:
                    continue
                for move in self._attacks_for((x, y), piece):
                    if move.dst == square:
                        return True
        return False

    def _attacks_for(self, src: tuple[int, int], piece: str) -> list[MoveInfo]:
        if piece.lower() == "k":
            return self._jump_moves(src, piece, ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)))
        if piece.lower() != "p":
            return self._pseudo_moves(src)
        x, y = src
        step = -1 if self._color(piece) == WHITE else 1
        return [MoveInfo(src, (x + dx, y + step)) for dx in (-1, 1) if self._inside(x + dx, y + step)]

    def _refresh_game_state(self) -> None:
        moves = self.all_legal_moves(self.turn)
        in_check = self.is_in_check(self.turn)
        self.checkmate = not moves and in_check
        self.stalemate = not moves and not in_check
        if self.checkmate:
            self.winner = self._other(self.turn)
            self.message = f"checkmate, {self.winner} wins"
        elif self.stalemate:
            self.winner = None
            self.message = "stalemate"
        elif in_check:
            self.message = f"{self.turn} in check"
        else:
            self.message = f"{self.turn} to move"

    def _snapshot(self) -> tuple[list[list[str | None]], dict[str, dict[str, bool]], tuple[int, int] | None]:
        return [row[:] for row in self.board], {WHITE: self.castling[WHITE].copy(), BLACK: self.castling[BLACK].copy()}, self.en_passant_target

    def _restore(self, snapshot: tuple[list[list[str | None]], dict[str, dict[str, bool]], tuple[int, int] | None]) -> None:
        self.board, self.castling, self.en_passant_target = snapshot

    def _can_land(self, dst: tuple[int, int], color: str) -> bool:
        target = self.piece_at(dst)
        return target is None or self._color(target) != color

    @staticmethod
    def _color(piece: str) -> str:
        return WHITE if piece.isupper() else BLACK

    @staticmethod
    def _other(color: str) -> str:
        return BLACK if color == WHITE else WHITE

    @staticmethod
    def _inside(x: int, y: int) -> bool:
        return 0 <= x < 8 and 0 <= y < 8

    def restart(self) -> None:
        self.__init__()

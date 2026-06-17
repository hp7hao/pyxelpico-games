from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "picocheckmate"
sys.path.insert(0, str(GAME_DIR))

from picocheckmate_core import PicoCheckmateCore  # noqa: E402


class PicoCheckmateCoreTest(unittest.TestCase):
    def test_pawn_double_step_and_capture(self):
        core = PicoCheckmateCore()

        self.assertTrue(core.move((4, 6), (4, 4)))
        self.assertTrue(core.move((3, 1), (3, 3)))
        self.assertTrue(core.move((4, 4), (3, 3)))

        self.assertEqual(core.piece_at((3, 3)), "P")
        self.assertEqual(core.turn, "black")

    def test_illegal_move_cannot_leave_king_in_check(self):
        core = PicoCheckmateCore.empty()
        core.set_piece((4, 7), "K")
        core.set_piece((4, 0), "r")
        core.set_piece((4, 6), "R")
        core.turn = "white"

        self.assertFalse(core.move((4, 6), (3, 6)))
        self.assertEqual(core.message, "king would be in check")

    def test_castling_moves_rook_and_king(self):
        core = PicoCheckmateCore.empty()
        core.set_piece((4, 7), "K")
        core.set_piece((7, 7), "R")
        core.set_piece((4, 0), "k")
        core.turn = "white"

        self.assertTrue(core.move((4, 7), (6, 7)))

        self.assertEqual(core.piece_at((6, 7)), "K")
        self.assertEqual(core.piece_at((5, 7)), "R")

    def test_en_passant_captures_adjacent_pawn(self):
        core = PicoCheckmateCore.empty()
        core.set_piece((4, 7), "K")
        core.set_piece((4, 0), "k")
        core.set_piece((4, 3), "P")
        core.set_piece((3, 1), "p")
        core.turn = "black"

        self.assertTrue(core.move((3, 1), (3, 3)))
        self.assertTrue(core.move((4, 3), (3, 2)))

        self.assertEqual(core.piece_at((3, 2)), "P")
        self.assertIsNone(core.piece_at((3, 3)))

    def test_pawn_promotes_to_queen(self):
        core = PicoCheckmateCore.empty()
        core.set_piece((4, 7), "K")
        core.set_piece((4, 0), "k")
        core.set_piece((0, 1), "P")
        core.turn = "white"

        self.assertTrue(core.move((0, 1), (0, 0)))

        self.assertEqual(core.piece_at((0, 0)), "Q")

    def test_fools_mate_detects_checkmate(self):
        core = PicoCheckmateCore()

        for src, dst in [((5, 6), (5, 5)), ((4, 1), (4, 3)), ((6, 6), (6, 4)), ((3, 0), (7, 4))]:
            self.assertTrue(core.move(src, dst))

        self.assertTrue(core.checkmate)
        self.assertEqual(core.winner, "black")

    def test_ai_prefers_capturing_high_value_piece(self):
        core = PicoCheckmateCore.empty()
        core.set_piece((4, 7), "K")
        core.set_piece((4, 0), "k")
        core.set_piece((3, 3), "q")
        core.set_piece((3, 6), "Q")
        core.set_piece((7, 6), "P")
        core.turn = "black"

        move = core.choose_ai_move()

        self.assertEqual(move, ((3, 3), (3, 6)))


if __name__ == "__main__":
    unittest.main()

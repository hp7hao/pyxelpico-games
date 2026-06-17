from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "woodworm"
sys.path.insert(0, str(GAME_DIR))

from woodworm_core import WoodwormCore  # noqa: E402


class WoodwormCoreTest(unittest.TestCase):
    def test_move_adds_new_head_and_keeps_three_segments(self):
        core = WoodwormCore(seed=1)
        core.set_test_level([
            "########",
            "#..G...#",
            "#..@...#",
            "########",
            "########",
        ])

        moved = core.move("right")

        self.assertTrue(moved)
        self.assertEqual(core.worm[0], (4, 2))
        self.assertEqual(len(core.worm), 3)
        self.assertEqual(core.moves, 1)

    def test_reverse_direction_is_blocked(self):
        core = WoodwormCore(seed=2)
        core.set_test_level([
            "########",
            "#......#",
            "#..@...#",
            "########",
            "########",
        ])

        core.move("right")
        moved = core.move("left")

        self.assertFalse(moved)
        self.assertEqual(core.worm[0], (4, 2))

    def test_eating_wood_removes_tile_and_scores(self):
        core = WoodwormCore(seed=3)
        core.set_test_level([
            "########",
            "#......#",
            "#..@wG.#",
            "########",
            "########",
        ])

        core.move("right")

        self.assertEqual(core.tile_at(4, 2), ".")
        self.assertEqual(core.wood_eaten, 1)
        self.assertGreater(core.score, 0)

    def test_undo_restores_worm_tiles_and_counters(self):
        core = WoodwormCore(seed=4)
        core.set_test_level([
            "########",
            "#......#",
            "#..@wG.#",
            "########",
            "########",
        ])
        original = core.snapshot()

        core.move("right")
        core.undo()

        self.assertEqual(core.snapshot(), original)

    def test_gravity_drops_unsupported_blocks_and_worm(self):
        core = WoodwormCore(seed=5)
        core.set_test_level([
            "########",
            "#......#",
            "#..b...#",
            "#..@...#",
            "#......#",
            "########",
        ])

        core.apply_gravity()

        self.assertEqual(core.tile_at(3, 4), "b")
        self.assertEqual(core.worm[0][1], 4)

    def test_reaching_goal_clears_level(self):
        core = WoodwormCore(seed=6)
        core.set_test_level([
            "########",
            "#......#",
            "#..@G..#",
            "########",
            "########",
        ])

        core.move("right")

        self.assertTrue(core.cleared)
        self.assertIn("cleared", core.message)


if __name__ == "__main__":
    unittest.main()

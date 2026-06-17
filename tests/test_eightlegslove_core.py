from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "eightlegslove"
sys.path.insert(0, str(GAME_DIR))

from eightlegslove_core import EightLegsCore  # noqa: E402


class EightLegsCoreTest(unittest.TestCase):
    def test_seeded_web_arena_has_spider_anchor_points_and_level_goal(self):
        core = EightLegsCore(seed=1)

        self.assertEqual(core.level, 1)
        self.assertEqual(core.spider_pos(), core.spawn)
        self.assertEqual(len(core.anchors), 8)
        self.assertGreater(core.goal_score, 0)
        self.assertGreater(core.time_left, 0)

    def test_spider_moves_within_arena_and_can_start_a_web_strand(self):
        core = EightLegsCore(seed=2)

        core.tick(right=True, down=True)
        moved = core.spider_pos()
        core.tick(spin=True)
        core.tick(right=True, spin=True)
        core.tick(place=True)

        self.assertNotEqual(moved, core.spawn)
        self.assertEqual(len(core.strands), 1)
        self.assertEqual(core.strands[0].start, moved)
        self.assertGreater(core.strands[0].length(), 0)

    def test_web_strand_catches_fly_and_scores_points(self):
        core = EightLegsCore(seed=3)
        core.add_strand((50, 120), (190, 120))
        core.spawn_bug(kind="fly", x=120, y=118, vx=0, vy=1)

        core.tick()

        self.assertEqual(core.score, 10)
        self.assertEqual(core.caught_counts["fly"], 1)
        self.assertEqual(len(core.bugs), 0)

    def test_beetle_chews_web_but_is_worth_more_points(self):
        core = EightLegsCore(seed=4)
        strand = core.add_strand((70, 132), (170, 132))
        core.spawn_bug(kind="beetle", x=120, y=130, vx=0, vy=1)

        core.tick()

        core.tick()

        self.assertEqual(core.score, 30)
        self.assertEqual(core.caught_counts["beetle"], 1)
        self.assertLess(strand.durability, strand.max_durability)

    def test_butterfly_is_rare_and_high_value(self):
        core = EightLegsCore(seed=5)
        core.add_strand((60, 90), (180, 90))
        core.spawn_bug(kind="butterfly", x=120, y=88, vx=0, vy=1)

        core.tick()

        self.assertEqual(core.score, 100)
        self.assertEqual(core.caught_counts["butterfly"], 1)

    def test_level_clears_after_goal_score_or_time_expires(self):
        core = EightLegsCore(seed=6)
        core.score = core.goal_score - 10
        core.add_strand((50, 120), (190, 120))
        core.spawn_bug(kind="fly", x=120, y=118, vx=0, vy=1)

        core.tick()

        self.assertTrue(core.level_clear)

        next_level = core.advance_level()
        self.assertEqual(next_level, 2)
        self.assertFalse(core.level_clear)
        self.assertGreater(core.goal_score, 0)


if __name__ == "__main__":
    unittest.main()

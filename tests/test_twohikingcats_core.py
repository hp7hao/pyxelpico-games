from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "twohikingcats"
sys.path.insert(0, str(GAME_DIR))

from twohikingcats_core import TwoHikingCatsCore  # noqa: E402


class TwoHikingCatsCoreTest(unittest.TestCase):
    def test_speed_changes_and_reset_restores_defaults(self):
        core = TwoHikingCatsCore(seed=1)

        core.adjust_speed(1)
        core.adjust_speed(1)
        self.assertGreater(core.speed, core.default_speed)
        core.adjust_speed(-1)
        self.assertGreaterEqual(core.speed, core.min_speed)

        core.reset_view()
        self.assertEqual(core.speed, core.default_speed)
        self.assertEqual(core.palette_index, 0)

    def test_palette_randomize_changes_palette_deterministically(self):
        core = TwoHikingCatsCore(seed=2)

        first = core.randomize_palette()
        second = core.randomize_palette()

        self.assertNotEqual(first, 0)
        self.assertNotEqual(second, first)
        self.assertIn(core.palette_name, {"dawn", "mist", "sunset", "moon", "forest"})

    def test_tick_scrolls_and_alternates_meows(self):
        core = TwoHikingCatsCore(seed=3)

        for _ in range(core.meow_interval):
            core.tick()

        self.assertGreater(core.scroll, 0.0)
        self.assertEqual(core.active_cat, 1)
        self.assertEqual(core.current_meow, "meow?")

    def test_cat_positions_bob_with_stride(self):
        core = TwoHikingCatsCore(seed=4)
        before = core.cat_positions()

        for _ in range(8):
            core.tick()
        after = core.cat_positions()

        self.assertNotEqual(before, after)
        self.assertEqual(len(after), 2)


if __name__ == "__main__":
    unittest.main()

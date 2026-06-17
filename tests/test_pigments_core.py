from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "pigments"
sys.path.insert(0, str(GAME_DIR))

from pigments_core import PigmentsCore  # noqa: E402


class PigmentsCoreTest(unittest.TestCase):
    def test_level_starts_with_droplets_discs_and_special_tiles(self):
        core = PigmentsCore(seed=1)

        self.assertEqual(core.player, core.spawn)
        self.assertGreaterEqual(core.pigment, 3)
        self.assertGreaterEqual(len(core.droplets), 2)
        self.assertGreaterEqual(len(core.discs), 1)
        self.assertGreaterEqual(len(core.grass), 1)
        self.assertGreaterEqual(len(core.water), 1)
        self.assertGreaterEqual(len(core.triggers), 1)

    def test_moving_paints_tiles_and_collects_droplets(self):
        core = PigmentsCore(seed=2)
        droplet = (core.spawn[0] + 1, core.spawn[1])
        core.droplets = {droplet}
        core.pigment = 1

        self.assertTrue(core.move(1, 0))

        self.assertEqual(core.player, droplet)
        self.assertIn(droplet, core.painted)
        self.assertNotIn(droplet, core.droplets)
        self.assertGreater(core.pigment, 1)

    def test_water_hides_player_from_discs_by_spending_pigment(self):
        core = PigmentsCore(seed=3)
        water = (core.spawn[0] + 1, core.spawn[1])
        core.water = {water}
        core.discs = [(water[0] + 2, water[1])]
        core.pigment = 2

        core.move(1, 0)
        core.tick_discs()

        self.assertEqual(core.player, water)
        self.assertEqual(core.pigment, 1)
        self.assertFalse(core.game_over)

    def test_trigger_makes_discs_dash_toward_player(self):
        core = PigmentsCore(seed=4)
        trigger = (core.spawn[0] + 1, core.spawn[1])
        core.triggers = {trigger}
        core.discs = [(trigger[0] + 4, trigger[1])]

        core.move(1, 0)

        self.assertLess(core.discs[0][0], trigger[0] + 4)
        self.assertIn("dash", core.message)

    def test_painting_all_safe_tiles_clears_level(self):
        core = PigmentsCore(seed=5)
        core.safe_tiles = {core.spawn, (core.spawn[0] + 1, core.spawn[1])}
        core.painted = {core.spawn}

        core.move(1, 0)

        self.assertTrue(core.level_clear)


if __name__ == "__main__":
    unittest.main()

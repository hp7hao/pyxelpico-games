from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "driftmania"
sys.path.insert(0, str(GAME_DIR))

from driftmania_core import DriftmaniaCore  # noqa: E402


class DriftmaniaCoreTest(unittest.TestCase):
    def test_accelerates_turns_and_drift_brake_rotates_faster(self):
        core = DriftmaniaCore(seed=1)
        core.tick(accel=True)
        self.assertGreater(core.speed, 0)

        heading = core.heading
        core.tick(accel=True, turn=1, drift=True)
        self.assertGreater(core.heading - heading, 0.05)
        self.assertLess(core.traction, 1.0)

    def test_grass_reduces_traction_without_killing_speed(self):
        core = DriftmaniaCore(seed=2)
        core.speed = 3.0
        core.x, core.y = core.grass_tiles[0]

        core.tick(accel=True)

        self.assertLess(core.traction, 0.8)
        self.assertGreater(core.speed, 2.0)

    def test_boost_tile_adds_speed_in_current_direction(self):
        core = DriftmaniaCore(seed=3)
        core.speed = 2.0
        core.x, core.y = core.boost_tiles[0]

        core.tick(accel=False)

        self.assertGreater(core.speed, 3.0)
        self.assertTrue(core.boost_timer > 0)

    def test_checkpoints_lap_and_medal(self):
        core = DriftmaniaCore(seed=4)
        core.elapsed = 30.0
        for gate in core.checkpoints:
            core.x, core.y = gate
            core.tick()

        self.assertTrue(core.finished)
        self.assertEqual(core.lap, 1)
        self.assertEqual(core.medal, "gold")


if __name__ == "__main__":
    unittest.main()

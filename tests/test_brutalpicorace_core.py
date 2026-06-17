from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "brutalpicorace"
sys.path.insert(0, str(GAME_DIR))

from brutalpicorace_core import BrutalPicoRaceCore  # noqa: E402


class BrutalPicoRaceCoreTest(unittest.TestCase):
    def test_ship_class_changes_acceleration_and_speed(self):
        heavy = BrutalPicoRaceCore(seed=1, ship_class="heavy")
        light = BrutalPicoRaceCore(seed=1, ship_class="light")

        for _ in range(30):
            heavy.tick(accel=True)
            light.tick(accel=True)

        self.assertGreater(light.speed, heavy.speed)
        self.assertGreater(heavy.health, light.health)

    def test_boost_consumes_meter_and_increases_speed(self):
        core = BrutalPicoRaceCore(seed=2)
        core.speed = 1.0
        boost_before = core.boost_meter

        core.tick(accel=True, boost=True)

        self.assertLess(core.boost_meter, boost_before)
        self.assertGreater(core.speed, 1.0)

    def test_lap_progress_and_finish(self):
        core = BrutalPicoRaceCore(seed=3)
        core.track_length = 10
        core.laps_required = 2

        for _ in range(80):
            core.tick(accel=True)

        self.assertTrue(core.finished)
        self.assertEqual(core.lap, 2)

    def test_off_track_and_collision_damage(self):
        core = BrutalPicoRaceCore(seed=4)
        core.position_x = 1.5
        health_before = core.health

        core.tick(accel=True)

        self.assertLess(core.health, health_before)
        self.assertEqual(core.message, "wall hit")


if __name__ == "__main__":
    unittest.main()

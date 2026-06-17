from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "picoworldrace"
sys.path.insert(0, str(GAME_DIR))

from picoworldrace_core import PicoWorldRaceCore  # noqa: E402


class PicoWorldRaceCoreTest(unittest.TestCase):
    def test_acceleration_and_steering_move_car_along_track(self):
        core = PicoWorldRaceCore(seed=1)
        for _ in range(20):
            core.input(accel=True, steer=1, drift=False)
            core.tick()

        self.assertGreater(core.speed, 0)
        self.assertGreater(core.progress, 0)
        self.assertGreater(core.lane, 0)

    def test_drift_allows_tighter_turning_but_reduces_speed(self):
        normal = PicoWorldRaceCore(seed=2)
        drift = PicoWorldRaceCore(seed=2)
        normal.speed = drift.speed = 3.0

        normal.input(accel=True, steer=1, drift=False)
        drift.input(accel=True, steer=1, drift=True)
        normal.tick()
        drift.tick()

        self.assertGreater(drift.lane, normal.lane)
        self.assertLess(drift.speed, normal.speed)

    def test_token_collection_scores_once_when_crossing_token_position(self):
        core = PicoWorldRaceCore(seed=3)
        core.tokens = [12.0]
        core.progress = 10.0
        core.speed = 3.0

        core.tick()
        core.tick()

        self.assertEqual(core.tokens_collected, 1)
        self.assertEqual(core.score, 5)
        core.tick()
        self.assertEqual(core.tokens_collected, 1)

    def test_lap_completion_advances_lap_and_finishes_after_final_lap(self):
        core = PicoWorldRaceCore(seed=4)
        core.progress = core.track_length - 1
        core.speed = 3.0

        core.tick()

        self.assertEqual(core.lap, 2)
        core.lap = core.total_laps
        core.progress = core.track_length - 1
        core.tick()
        self.assertTrue(core.finished)

    def test_off_track_penalty_and_opponent_position(self):
        core = PicoWorldRaceCore(seed=5)
        core.speed = 4.0
        core.lane = 2.0

        core.tick()

        self.assertLess(core.speed, 4.0)
        self.assertGreater(core.opponents[0], 0)


if __name__ == "__main__":
    unittest.main()

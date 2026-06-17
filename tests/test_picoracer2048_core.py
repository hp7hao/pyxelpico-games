from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "picoracer2048"
sys.path.insert(0, str(GAME_DIR))

from picoracer2048_core import Picoracer2048Core  # noqa: E402


class Picoracer2048CoreTest(unittest.TestCase):
    def test_accelerates_brakes_and_boosts_by_speed_class(self):
        core = Picoracer2048Core(seed=1)
        for _ in range(30):
            core.tick(accelerate=True)
        speed_after_accel = core.player.speed

        for _ in range(8):
            core.tick(brake=True)
        speed_after_brake = core.player.speed

        core.player.lane = 0.0
        core.boost_pads = {core.player.segment: 20}
        core.tick(accelerate=True)

        self.assertGreater(speed_after_accel, 1.0)
        self.assertLess(speed_after_brake, speed_after_accel)
        self.assertGreater(core.player.speed, speed_after_brake)

    def test_track_curve_pushes_car_and_steering_holds_line(self):
        core = Picoracer2048Core(seed=2)
        core.track = [(40, 0.45, 1.0)]
        core.rebuild_track()
        core.player.speed = 2.4
        core.tick(accelerate=True)
        drifted_lane = core.player.lane

        for _ in range(8):
            core.tick(accelerate=True, left=True)

        self.assertGreater(drifted_lane, 0.0)
        self.assertLess(core.player.lane, drifted_lane + 0.5)

    def test_off_track_hits_wall_and_slows_with_damage(self):
        core = Picoracer2048Core(seed=3)
        core.player.speed = 3.0
        core.player.lane = core.current_width() + 0.4

        core.tick(accelerate=True)

        self.assertGreater(core.wall_hits, 0)
        self.assertLess(core.player.speed, 3.0)
        self.assertEqual(core.message, "wall hit")

    def test_completes_three_laps_and_records_finish_time(self):
        core = Picoracer2048Core(seed=4)
        core.track = [(12, 0.0, 1.0)]
        core.rebuild_track()
        core.player.speed = 6.0

        for _ in range(80):
            core.tick(accelerate=True)
            if core.finished:
                break

        self.assertTrue(core.finished)
        self.assertEqual(core.lap, 3)
        self.assertGreater(core.finish_time, 0)

    def test_ai_racer_advances_and_creates_race_pressure(self):
        core = Picoracer2048Core(seed=5)
        start_segment = core.ai.segment

        for _ in range(40):
            core.tick(accelerate=True)

        self.assertGreater(core.ai.segment, start_segment)
        self.assertNotEqual(core.position, 0)


if __name__ == "__main__":
    unittest.main()

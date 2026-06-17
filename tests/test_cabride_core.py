from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "cabride"
sys.path.insert(0, str(GAME_DIR))

from cabride_core import CabRideCore  # noqa: E402


class CabRideCoreTest(unittest.TestCase):
    def test_throttle_and_brake_change_speed_slowly(self):
        core = CabRideCore(seed=1)

        for _ in range(20):
            core.tick(throttle=1)

        self.assertGreater(core.speed, 0.25)
        speed_before_brake = core.speed

        for _ in range(12):
            core.tick(throttle=-1)

        self.assertLess(core.speed, speed_before_brake)
        self.assertGreaterEqual(core.speed, 0.0)

    def test_station_stop_opens_doors_and_boards_passengers(self):
        core = CabRideCore(seed=2)
        core.distance_to_station = 0.02
        core.speed = 0.0
        waiting_before = core.waiting_passengers

        result = core.toggle_doors()

        self.assertEqual(result, "great stop")
        self.assertTrue(core.doors_open)
        self.assertGreater(core.passengers, 0)
        self.assertLess(core.waiting_passengers, waiting_before)
        self.assertGreater(core.total_score, 0)

    def test_opening_doors_while_moving_is_rejected(self):
        core = CabRideCore(seed=3)
        core.speed = 0.2
        core.distance_to_station = 0.01

        result = core.toggle_doors()

        self.assertEqual(result, "stop first")
        self.assertFalse(core.doors_open)

    def test_express_and_last_station_finish_journey(self):
        core = CabRideCore(seed=4)

        core.toggle_express()
        self.assertTrue(core.express_mode)
        core.announce_last_station()
        core.distance_to_station = 0.01
        core.speed = 0.0
        core.toggle_doors()

        self.assertTrue(core.journey_over)
        self.assertEqual(core.status, "journey complete")


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "whiplashtaxi"
sys.path.insert(0, str(GAME_DIR))

from whiplashtaxi_core import WhiplashTaxiCore  # noqa: E402


class WhiplashTaxiCoreTest(unittest.TestCase):
    def test_accelerates_steers_and_requires_stop_before_reverse(self):
        core = WhiplashTaxiCore(seed=1)
        core.tick(accel=True)
        self.assertGreater(core.speed, 0)

        before_heading = core.heading
        core.tick(accel=True, turn=1)
        self.assertGreater(core.heading, before_heading)

        core.speed = 1.2
        core.tick(reverse=True)
        self.assertEqual(core.speed, 0.0)
        core.tick(reverse=True)
        self.assertLess(core.speed, 0.0)

    def test_pickup_requires_stopping_next_to_passenger(self):
        core = WhiplashTaxiCore(seed=2)
        passenger = core.passengers[0]
        core.x, core.y = passenger.pickup
        core.speed = 1.0

        self.assertFalse(core.try_pickup())
        core.speed = 0.0
        self.assertTrue(core.try_pickup())
        self.assertIs(core.current_passenger, passenger)
        self.assertEqual(core.message, "passenger aboard")

    def test_delivery_awards_fare_and_spawns_next_passenger(self):
        core = WhiplashTaxiCore(seed=3)
        passenger = core.passengers[0]
        core.x, core.y = passenger.pickup
        core.speed = 0.0
        core.try_pickup()
        core.x, core.y = passenger.destination

        self.assertTrue(core.try_dropoff())
        self.assertGreater(core.money, 0)
        self.assertIsNone(core.current_passenger)
        self.assertTrue(passenger.delivered)

    def test_timer_ends_shift_after_five_minutes(self):
        core = WhiplashTaxiCore(seed=4)
        core.time_left = 0.01

        core.tick(accel=True)

        self.assertTrue(core.shift_over)
        self.assertEqual(core.message, "shift over")


if __name__ == "__main__":
    unittest.main()

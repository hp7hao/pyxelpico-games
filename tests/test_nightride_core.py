from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "nightride"
sys.path.insert(0, str(GAME_DIR))

from nightride_core import NightRideCore  # noqa: E402


class NightRideCoreTest(unittest.TestCase):
    def test_lane_changes_and_distance_advances_level(self):
        core = NightRideCore(seed=1)
        core.tick(turn=1)
        self.assertEqual(core.lane, 2)

        core.distance = core.level_distance - 1
        core.tick()
        self.assertEqual(core.level, 2)
        self.assertEqual(core.message, "level 2")

    def test_collision_with_traffic_costs_health(self):
        core = NightRideCore(seed=2)
        core.traffic = [{"lane": 1, "y": 0.93, "kind": "car"}]

        core.tick()

        self.assertEqual(core.hp, 2)
        self.assertEqual(core.message, "crash")

    def test_shooting_unlocks_and_defeats_enemy_vehicle(self):
        core = NightRideCore(seed=3)
        core.level = 3
        core.weapon_unlocked = True
        core.traffic = [{"lane": 1, "y": 0.5, "kind": "bike"}]

        self.assertTrue(core.shoot())
        for _ in range(10):
            core.tick()

        self.assertEqual(core.score, 100)
        self.assertFalse(core.traffic)

    def test_boss_defeat_wins_the_ride(self):
        core = NightRideCore(seed=4)
        core.level = core.boss_level
        core.start_boss()

        for _ in range(5):
            core.shoot()
            core.tick()

        self.assertTrue(core.victory)
        self.assertEqual(core.message, "sunrise")


if __name__ == "__main__":
    unittest.main()

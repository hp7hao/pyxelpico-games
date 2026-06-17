from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "haroldsbad"
sys.path.insert(0, str(GAME_DIR))

from haroldsbad_core import HaroldsBadCore  # noqa: E402


class HaroldsBadCoreTest(unittest.TestCase):
    def test_movement_jump_and_gravity(self):
        core = HaroldsBadCore(seed=1)

        core.tick(move=1, jump=True)

        self.assertGreater(core.player.vx, 0)
        self.assertLess(core.player.vy, 0)
        self.assertFalse(core.player.grounded)

    def test_death_spawns_corpse_and_consumes_life(self):
        core = HaroldsBadCore(seed=2)
        lives_before = core.lives

        core.kill_player("spikes")

        self.assertEqual(core.lives, lives_before - 1)
        self.assertEqual(len(core.corpses), 1)
        self.assertEqual(core.message, "spikes")

    def test_corpse_bridge_allows_crossing_gap(self):
        core = HaroldsBadCore(seed=3)
        core.player.x = 76
        core.player.y = 164

        core.kill_player("bridge")
        core.player.x = 76
        core.player.y = 148
        for _ in range(20):
            core.tick(move=1)

        self.assertGreater(core.player.x, 96)
        self.assertFalse(core.player.dead)

    def test_water_drowning_and_goal_scoring(self):
        core = HaroldsBadCore(seed=4)
        core.player.x = 118
        core.player.y = 182

        for _ in range(core.drown_frames + 1):
            core.tick()

        self.assertEqual(core.corpses[-1].reason, "drowned")
        self.assertEqual(core.message, "drowned")

        core.player.x = core.goal_x
        core.player.y = core.ground_y - 8
        core.player.dead = False
        core.check_goal()
        self.assertTrue(core.level_complete)
        self.assertGreaterEqual(core.harolds_saved, 0)


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "toastarling"
sys.path.insert(0, str(GAME_DIR))

from toastarling_core import ToAStarlingCore  # noqa: E402


class ToAStarlingCoreTest(unittest.TestCase):
    def test_run_accelerates_and_friction_slows_on_ground(self):
        core = ToAStarlingCore(seed=1)

        for _ in range(8):
            core.tick(right=True)
        moving_dx = core.player.dx
        for _ in range(12):
            core.tick()

        self.assertGreater(moving_dx, 0.8)
        self.assertLess(abs(core.player.dx), abs(moving_dx))

    def test_jump_and_coyote_jump_push_player_upward(self):
        core = ToAStarlingCore(seed=2)
        core.player.on_ground = True
        core.tick(jump=True)
        self.assertLess(core.player.dy, 0)

        core = ToAStarlingCore(seed=3)
        core.player.on_ground = False
        core.player.coyote = 4
        core.tick(jump=True)
        self.assertLess(core.player.dy, 0)

    def test_glide_limits_fall_speed_after_skill_unlock(self):
        core = ToAStarlingCore(seed=4)
        core.player.skill = 1
        core.player.on_ground = False
        core.player.dy = 4.0

        core.tick(glide=True)

        self.assertLessEqual(core.player.dy, core.glide_speed)

    def test_collects_berries_keys_and_opens_locked_door(self):
        core = ToAStarlingCore(seed=5)
        core.set_test_room([
            "################",
            "#..............#",
            "#@..b.k.D....G#",
            "################",
            "################",
        ])

        for _ in range(80):
            core.tick(right=True)

        self.assertEqual(core.berries, 1)
        self.assertEqual(core.keys, 0)
        self.assertTrue(core.cleared)

    def test_switch_toggles_bridge_to_reach_goal(self):
        core = ToAStarlingCore(seed=6)
        core.set_test_room([
            "################",
            "#..............#",
            "#@..s.....G....#",
            "################",
            "################",
        ])

        for _ in range(20):
            core.tick(right=True)

        self.assertTrue(core.bridge_active)
        self.assertIn("bridge", core.message)

    def test_hazard_respawns_at_checkpoint_and_goal_clears(self):
        core = ToAStarlingCore(seed=7)
        core.set_test_room([
            "################",
            "#..............#",
            "#@..c..^....G..#",
            "################",
            "################",
        ])
        for _ in range(40):
            core.tick(right=True)
        self.assertEqual(core.deaths, 1)
        self.assertGreaterEqual(core.player.x, core.spawn_x)

        core.player.x = core.goal_x * core.tile
        core.player.y = core.goal_y * core.tile
        core.tick()
        self.assertTrue(core.cleared)


if __name__ == "__main__":
    unittest.main()

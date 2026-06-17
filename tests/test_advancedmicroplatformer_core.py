from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "advancedmicroplatformer"
sys.path.insert(0, str(GAME_DIR))

from advancedmicroplatformer_core import AdvancedMicroPlatformerCore  # noqa: E402


class AdvancedMicroPlatformerCoreTest(unittest.TestCase):
    def test_player_runs_jumps_and_uses_variable_jump_height(self):
        held = AdvancedMicroPlatformerCore(seed=1)
        tapped = AdvancedMicroPlatformerCore(seed=1)

        held.press_jump()
        tapped.press_jump()
        for _ in range(10):
            held.tick(right=True, jump_held=True)
            tapped.tick(right=True, jump_held=False)

        self.assertGreater(held.player_x, held.spawn_x)
        self.assertLess(held.player_y, tapped.player_y)

    def test_coyote_jump_allows_late_jump_after_leaving_platform(self):
        core = AdvancedMicroPlatformerCore(seed=2)
        core.player_x = 95
        core.player_y = 88
        core.on_ground = True

        for _ in range(4):
            core.tick(right=True)
        jumped = core.press_jump()

        self.assertTrue(jumped)
        self.assertLess(core.vy, 0)

    def test_buffered_jump_fires_on_landing(self):
        core = AdvancedMicroPlatformerCore(seed=3)
        core.player_y = 126
        core.vy = 3
        core.on_ground = False
        core.coyote_timer = 0

        core.press_jump()
        jumped_after_landing = False
        for _ in range(20):
            core.tick()
            if core.vy < 0 and not core.on_ground:
                jumped_after_landing = True
                break

        self.assertTrue(jumped_after_landing)

    def test_one_way_platform_blocks_from_above_but_not_below(self):
        core = AdvancedMicroPlatformerCore(seed=4)
        core.player_x = 140
        core.player_y = 88
        core.vy = 3
        core.on_ground = False

        for _ in range(20):
            core.tick()

        self.assertTrue(core.on_ground)
        self.assertAlmostEqual(core.player_y, 98)

        core.player_y = 124
        core.vy = -4
        core.on_ground = False
        for _ in range(6):
            core.tick(jump_held=True)

        self.assertLess(core.player_y, 112)

    def test_camera_follows_after_threshold_and_goal_clears_demo(self):
        core = AdvancedMicroPlatformerCore(seed=5)

        for _ in range(120):
            core.tick(right=True)

        self.assertGreater(core.camera_x, 0)

        core.player_x = core.goal_x
        core.player_y = core.goal_y
        core.tick()
        self.assertTrue(core.level_clear)


if __name__ == "__main__":
    unittest.main()

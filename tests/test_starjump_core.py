from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "starjump"
sys.path.insert(0, str(GAME_DIR))

from starjump_core import StarjumpCore  # noqa: E402


class StarjumpCoreTest(unittest.TestCase):
    def test_jump_chain_consumes_double_and_triple_jumps(self):
        core = StarjumpCore(seed=1)
        core.grant_jump_charge()
        core.grant_jump_charge()

        self.assertTrue(core.jump())
        core.player.grounded = False
        self.assertTrue(core.jump())
        self.assertTrue(core.jump())
        self.assertFalse(core.jump())

        self.assertEqual(core.air_jumps, 0)
        self.assertEqual(core.message, "no jump")

    def test_breakable_platform_collapses_after_bounce(self):
        core = StarjumpCore(seed=2)
        platform = core.platforms[1]
        core.player.x = platform.x
        core.player.y = platform.y - 1
        core.player.vy = 1.5

        core.tick()

        self.assertFalse(platform.active)
        self.assertLess(core.player.vy, 0)
        self.assertEqual(core.message, "break jump")

    def test_toggle_switch_changes_solid_color(self):
        core = StarjumpCore(seed=3)
        self.assertEqual(core.solid_color, "white")

        core.toggle_color()

        self.assertEqual(core.solid_color, "pink")
        self.assertEqual(core.message, "pink solid")

    def test_cannon_launches_star_and_advances_stage(self):
        core = StarjumpCore(seed=4)
        core.player.x = core.cannon_x
        core.player.y = core.cannon_y

        launched = core.use_cannon()
        for _ in range(18):
            core.tick()

        self.assertTrue(launched)
        self.assertGreater(core.stage, 1)
        self.assertEqual(core.message, "stage 2")

    def test_timer_and_finish_state(self):
        core = StarjumpCore(seed=5)
        core.stage = core.final_stage
        core.player.x = core.goal_x
        core.player.y = core.goal_y
        for _ in range(7):
            core.tick()

        self.assertTrue(core.finished)
        self.assertEqual(core.timer, 7)
        self.assertEqual(core.message, "back to the beginning")


if __name__ == "__main__":
    unittest.main()

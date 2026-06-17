from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "marballs2"
sys.path.insert(0, str(GAME_DIR))

from marballs2_core import Marballs2Core  # noqa: E402


class Marballs2CoreTest(unittest.TestCase):
    def test_roll_accelerates_and_friction_slows_ball(self):
        core = Marballs2Core(seed=1)
        start_x = core.ball.x
        for _ in range(12):
            core.tick(right=True)
        moving_dx = core.ball.dx
        for _ in range(20):
            core.tick()

        self.assertGreater(core.ball.x, start_x + 5)
        self.assertGreater(moving_dx, 0.5)
        self.assertLess(abs(core.ball.dx), abs(moving_dx))

    def test_jump_pad_launches_ball_upward(self):
        core = Marballs2Core(seed=2)
        core.set_test_level([
            "############",
            "#@...J....G#",
            "#..........#",
            "############",
        ])
        for _ in range(35):
            core.tick(right=True)

        self.assertLess(core.ball.dz, 0)
        self.assertEqual(core.message, "jump pad")

    def test_collects_orbs_before_exit_opens(self):
        core = Marballs2Core(seed=3)
        core.set_test_level([
            "###############",
            "#@..o.....G...#",
            "###############",
        ])
        for _ in range(22):
            core.tick(right=True)
        self.assertEqual(core.orbs, 1)
        self.assertFalse(core.cleared)

        for _ in range(45):
            core.tick(right=True)
            if core.cleared:
                break

        self.assertTrue(core.cleared)
        self.assertEqual(core.message, "goal")

    def test_wall_collision_bounces_and_can_increase_speed(self):
        core = Marballs2Core(seed=4)
        core.ball.x = (core.width - 1) * core.tile - 5
        core.ball.dx = 2.4
        core.ball.dy = -0.8

        core.tick(right=True)

        self.assertLess(core.ball.dx, 0)
        self.assertGreater(core.wall_hits, 0)
        self.assertEqual(core.message, "wall bounce")

    def test_rotated_controls_map_right_to_diagonal_roll(self):
        core = Marballs2Core(seed=5)
        core.rotated_controls = True
        core.tick(right=True)

        self.assertGreater(core.ball.dx, 0)
        self.assertGreater(core.ball.dy, 0)


if __name__ == "__main__":
    unittest.main()

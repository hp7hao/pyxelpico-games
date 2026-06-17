from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "combopool"
sys.path.insert(0, str(GAME_DIR))

from combopool_core import Ball, ComboPoolCore  # noqa: E402


class ComboPoolCoreTest(unittest.TestCase):
    def test_aim_and_shoot_adds_moving_ball(self):
        core = ComboPoolCore(seed=1)
        core.balls = []
        core.aim = 0.0

        core.shoot()

        self.assertEqual(len(core.balls), 1)
        self.assertGreater(core.balls[0].vx, 0)
        self.assertGreater(core.cooldown, 0)

    def test_same_color_collision_merges_to_next_color_and_scores_combo(self):
        core = ComboPoolCore(seed=2)
        core.balls = [Ball(90, 120, 1, vx=1), Ball(102, 120, 1, vx=-1)]

        core.tick()

        living = [ball for ball in core.balls if not ball.dead]
        self.assertEqual(len(living), 1)
        self.assertEqual(living[0].level, 2)
        self.assertGreaterEqual(core.score, 20)
        self.assertEqual(core.combo, 1)

    def test_wall_bounce_increases_rebound_count(self):
        core = ComboPoolCore(seed=3)
        core.balls = [Ball(10, 120, 1, vx=-2)]

        core.tick()

        self.assertGreater(core.balls[0].vx, 0)
        self.assertEqual(core.balls[0].rebounds, 1)

    def test_life_pressure_increases_with_many_dark_balls(self):
        core = ComboPoolCore(seed=4)
        core.balls = [Ball(40 + i * 12, 120, 5) for i in range(7)]
        core.life = 3

        core.tick()

        self.assertLess(core.life, 3)

    def test_reaching_pink_merge_wins_and_empty_life_loses(self):
        core = ComboPoolCore(seed=5)
        core.balls = [Ball(90, 120, core.final_level, vx=1), Ball(102, 120, core.final_level, vx=-1)]
        core.tick()
        self.assertTrue(core.won)

        core = ComboPoolCore(seed=6)
        core.life = 1
        core.balls = [Ball(40 + i * 12, 120, 5) for i in range(8)]
        core.tick()
        self.assertTrue(core.lost)


if __name__ == "__main__":
    unittest.main()

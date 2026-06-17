from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "picotennis"
sys.path.insert(0, str(GAME_DIR))

from picotennis_core import PicoTennisCore  # noqa: E402


class PicoTennisCoreTest(unittest.TestCase):
    def test_serve_starts_rally_and_return_angle_depends_on_offset(self):
        core = PicoTennisCore(seed=1)

        self.assertTrue(core.serve())
        self.assertEqual(core.server, 0)
        self.assertEqual(core.ball.owner, 0)
        self.assertEqual(core.ball.vy, -3.0)

        core.ball.x = core.player_x + 18
        core.ball.y = core.player_y
        self.assertTrue(core.hit(player=0, power=False))

        self.assertEqual(core.ball.owner, 0)
        self.assertLess(core.ball.vx, 0)
        self.assertGreater(core.power[0], 0)

    def test_power_shot_spends_meter_and_increases_speed(self):
        core = PicoTennisCore(seed=2)
        core.serve()
        core.power[0] = 4
        core.ball.x = core.player_x - 12
        core.ball.y = core.player_y

        self.assertTrue(core.hit(player=0, power=True))

        self.assertEqual(core.power[0], 0)
        self.assertLess(core.ball.vy, -5.0)
        self.assertGreater(core.ball.vx, 0)

    def test_fault_on_over_angled_serve_awards_receiver_after_second_fault(self):
        core = PicoTennisCore(seed=3)
        core.player_x = core.center_x - 42

        self.assertTrue(core.serve())
        self.assertEqual(core.faults, 1)
        self.assertEqual(core.points, [0, 0])

        self.assertTrue(core.serve())
        self.assertEqual(core.points, [0, 1])
        self.assertEqual(core.faults, 0)
        self.assertEqual(core.message, "double fault")

    def test_out_ball_awards_point_and_game_progresses(self):
        core = PicoTennisCore(seed=4)
        core.award_point(0)
        core.award_point(0)
        core.award_point(0)

        self.assertEqual(core.points, [3, 0])
        core.award_point(0)

        self.assertEqual(core.games, [1, 0])
        self.assertEqual(core.points, [0, 0])
        self.assertEqual(core.server, 1)


if __name__ == "__main__":
    unittest.main()

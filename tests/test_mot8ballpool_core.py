from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "mot8ballpool"
sys.path.insert(0, str(GAME_DIR))

from mot8ballpool_core import Mot8BallPoolCore  # noqa: E402


class Mot8BallPoolCoreTest(unittest.TestCase):
    def test_aim_power_and_shot_move_cue_ball(self):
        core = Mot8BallPoolCore(seed=1)
        core.adjust_aim(1)
        core.adjust_power(3)

        self.assertTrue(core.shoot())
        for _ in range(8):
            core.tick()

        self.assertNotEqual(core.cue_ball["x"], core.cue_start_x)
        self.assertEqual(core.mode, "sim")

    def test_first_sunk_ball_assigns_player_color(self):
        core = Mot8BallPoolCore(seed=2)

        core.resolve_pocket("solid")

        self.assertEqual(core.players[0]["color"], "solid")
        self.assertEqual(core.players[1]["color"], "stripe")
        self.assertEqual(core.players[0]["sunk"], 1)

    def test_foul_awards_free_ball_to_other_player(self):
        core = Mot8BallPoolCore(seed=3)

        core.commit_foul("white sunk")

        self.assertEqual(core.current_player, 1)
        self.assertTrue(core.players[1]["free_ball"])
        self.assertEqual(core.message, "foul: white sunk")

    def test_black_ball_win_and_forfeit(self):
        core = Mot8BallPoolCore(seed=4)
        core.players[0]["color"] = "solid"
        core.players[0]["sunk"] = 7

        core.resolve_pocket("black")
        self.assertTrue(core.game_over)
        self.assertEqual(core.winner, 0)

        core = Mot8BallPoolCore(seed=5)
        core.players[0]["color"] = "solid"
        core.resolve_pocket("black")
        self.assertEqual(core.winner, 1)


if __name__ == "__main__":
    unittest.main()

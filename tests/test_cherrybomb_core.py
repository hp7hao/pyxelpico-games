from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "cherrybomb"
sys.path.insert(0, str(GAME_DIR))

from cherrybomb_core import CherryBombCore, Enemy  # noqa: E402


class CherryBombCoreTest(unittest.TestCase):
    def test_player_moves_within_screen_bounds(self):
        core = CherryBombCore(seed=1)

        for _ in range(80):
            core.tick(left=True, up=True)

        self.assertGreaterEqual(core.player_x, 10)
        self.assertGreaterEqual(core.player_y, 142)

    def test_shot_destroys_enemy_and_scores(self):
        core = CherryBombCore(seed=2)
        core.enemies = [Enemy(core.player_x, core.player_y - 18, kind=1)]

        self.assertTrue(core.shoot())
        for _ in range(8):
            core.tick()

        self.assertEqual(core.enemies, [])
        self.assertGreater(core.score, 0)

    def test_enemy_bullet_hit_costs_life_and_can_end_game(self):
        core = CherryBombCore(seed=3)
        core.lives = 1
        core.enemy_bullets = [(core.player_x, core.player_y - 1, 0, 2)]

        core.tick()

        self.assertEqual(core.lives, 0)
        self.assertTrue(core.game_over)

    def test_cherry_pickups_restore_life_after_ten_or_score_at_full_life(self):
        core = CherryBombCore(seed=4)
        core.lives = 3
        core.cherries = 9
        core.pickups = [(core.player_x, core.player_y)]

        core.tick()

        self.assertEqual(core.lives, 4)
        self.assertEqual(core.cherries, 0)

        core.cherries = 9
        core.pickups = [(core.player_x, core.player_y)]
        before_score = core.score
        core.tick()

        self.assertEqual(core.lives, 4)
        self.assertEqual(core.cherries, 0)
        self.assertGreater(core.score, before_score)

    def test_bomb_spends_cherries_and_clears_threats(self):
        core = CherryBombCore(seed=5)
        core.cherries = 3
        core.enemies = [Enemy(core.player_x, core.player_y - 30, kind=1), Enemy(core.player_x + 50, core.player_y - 40, kind=1)]
        core.enemy_bullets = [(core.player_x + 4, core.player_y - 20, 0, 2)]

        self.assertTrue(core.bomb())

        self.assertEqual(core.cherries, 0)
        self.assertEqual(core.enemy_bullets, [])
        self.assertLess(len(core.enemies), 2)

    def test_clearing_wave_advances_until_victory(self):
        core = CherryBombCore(seed=6)
        core.wave = 8
        core.enemies = []

        core.tick()

        self.assertTrue(core.victory)
        self.assertFalse(core.game_over)


if __name__ == "__main__":
    unittest.main()

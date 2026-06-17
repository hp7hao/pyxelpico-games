from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "justoneboss"
sys.path.insert(0, str(GAME_DIR))

from justoneboss_core import Direction, GameCore, Phase  # noqa: E402


class JustOneBossCoreTest(unittest.TestCase):
    def test_player_steps_on_grid_and_cannot_leave_arena(self):
        core = GameCore()

        self.assertEqual(core.player_col, 4)
        self.assertEqual(core.player_row, 3)

        self.assertTrue(core.step_player(Direction.LEFT))
        self.assertEqual(core.player_col, 3)
        self.assertEqual(core.player_row, 3)

        for _ in range(8):
            core.step_player(Direction.LEFT)

        self.assertEqual(core.player_col, 1)
        self.assertEqual(core.player_row, 3)

    def test_player_hit_by_hazard_loses_health_and_becomes_invincible(self):
        core = GameCore()
        hazard = core.spawn_hazard(core.player_col, core.player_row, ttl=10)

        core.tick()

        self.assertTrue(hazard.expired)
        self.assertEqual(core.player_health, 3)
        self.assertGreater(core.invincible_ticks, 0)

        core.spawn_hazard(core.player_col, core.player_row, ttl=10)
        core.tick()

        self.assertEqual(core.player_health, 3)

    def test_magic_tile_hit_damages_boss_and_advances_phase(self):
        core = GameCore()
        core.boss_health = 2
        tile = core.spawn_magic_tile(core.player_col, core.player_row, ttl=10)

        core.tick()

        self.assertTrue(tile.expired)
        self.assertEqual(core.boss_health, 1)
        self.assertEqual(core.score, 100)
        self.assertEqual(core.phase, Phase.ONE)

        core.spawn_magic_tile(core.player_col, core.player_row, ttl=10)
        core.tick()
        self.assertEqual(core.boss_health, core.phase_health(Phase.TWO))
        self.assertEqual(core.phase, Phase.TWO)

    def test_final_phase_win_and_zero_health_loss(self):
        core = GameCore()
        core.phase = Phase.FINAL
        core.boss_health = 1
        core.spawn_magic_tile(core.player_col, core.player_row, ttl=10)

        core.tick()
        self.assertTrue(core.won)
        self.assertFalse(core.lost)

        core = GameCore()
        core.player_health = 1
        core.spawn_hazard(core.player_col, core.player_row, ttl=10)
        core.tick()
        self.assertTrue(core.lost)
        self.assertFalse(core.won)


if __name__ == "__main__":
    unittest.main()

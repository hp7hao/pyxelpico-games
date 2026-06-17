from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "bas"
sys.path.insert(0, str(GAME_DIR))

from bas_core import BasCore, Saw  # noqa: E402


class BasCoreTest(unittest.TestCase):
    def test_jump_left_and_right_switches_wall_and_scores(self):
        core = BasCore(seed=1)

        core.jump(False)
        core.tick(12)

        self.assertFalse(core.player.right_wall)
        self.assertEqual(core.score, 1)
        self.assertEqual(core.state, "playing")

        core.jump(True)
        core.tick(12)

        self.assertTrue(core.player.right_wall)
        self.assertEqual(core.score, 2)

    def test_mid_air_jump_changes_target_without_waiting_to_land(self):
        core = BasCore(seed=2)

        core.jump(False)
        core.tick(3)
        core.jump(True)

        self.assertTrue(core.player.target_right_wall)
        self.assertTrue(core.player.jumping)

    def test_saw_on_target_wall_predicts_will_die_and_collision_kills(self):
        core = BasCore(seed=3)
        core.columns.saws = [Saw(tile=core.player.tile_pos - 1, right_wall=False)]

        self.assertTrue(core.will_collide(False))
        core.jump(False)
        core.tick(12)

        self.assertEqual(core.state, "dead")

    def test_trap_catches_player_when_camera_climbs_too_slowly(self):
        core = BasCore(seed=4)
        core.trap_y = core.player.y

        core.tick()

        self.assertEqual(core.state, "dead")

    def test_columns_spawn_saws_and_score_increases_over_time(self):
        core = BasCore(seed=5)

        for i in range(8):
            core.columns.saws = []
            core.jump(i % 2 == 0)
            core.tick(12)

        core.columns.next_spawn_tile = core.player.tile_pos - 3
        core.tick()

        self.assertGreaterEqual(core.score, 8)
        self.assertGreater(len(core.columns.saws), 0)

    def test_game_over_updates_highscore_and_restart_resets_run(self):
        core = BasCore(seed=6)
        core.highscore = 3
        core.score = 7

        core.die()
        core.restart()

        self.assertEqual(core.highscore, 7)
        self.assertEqual(core.score, 0)
        self.assertEqual(core.state, "initial")


if __name__ == "__main__":
    unittest.main()

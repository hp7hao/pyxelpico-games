from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "guncho"
sys.path.insert(0, str(GAME_DIR))

from guncho_core import GunchoCore  # noqa: E402


class GunchoCoreTest(unittest.TestCase):
    def test_seeded_camp_has_player_bandits_revolver_and_six_directions(self):
        core = GunchoCore(seed=1)

        self.assertEqual(core.level, 1)
        self.assertEqual(len(core.directions), 6)
        self.assertEqual(len(core.bullets), 6)
        self.assertTrue(all(core.bullets))
        self.assertGreaterEqual(len(core.enemies), 2)
        self.assertIn(core.player, core.cells)

    def test_move_action_steps_to_selected_free_hex_and_rotates_revolver(self):
        core = GunchoCore(seed=2)
        start = core.player
        direction = core.first_free_direction()

        self.assertTrue(core.move(direction))

        self.assertEqual(core.player, core.neighbor(start, direction))
        self.assertEqual(core.aim, core.rotated_after(direction))
        self.assertTrue(core.enemy_turn_pending)

    def test_revolver_shoots_first_target_and_spends_then_reloads_chamber(self):
        core = GunchoCore(seed=3)
        core.enemies.clear()
        target = core.add_enemy(core.ray_cells(core.player, 0)[1], kind="axe")

        self.assertTrue(core.shoot(0))
        self.assertTrue(target.killed)
        self.assertFalse(core.bullets[0])
        self.assertEqual(core.bandits_killed, 1)

        self.assertTrue(core.shoot(0))
        self.assertTrue(core.bullets[0])
        self.assertEqual(core.message, "reloaded")

    def test_punch_pushes_enemy_and_stuns_it_for_one_turn(self):
        core = GunchoCore(seed=4)
        core.enemies.clear()
        direction = core.first_free_direction()
        enemy = core.add_enemy(core.neighbor(core.player, direction), kind="axe")
        before = enemy.pos

        self.assertTrue(core.punch(direction))

        self.assertNotEqual(enemy.pos, before)
        self.assertEqual(enemy.stun, 1)
        self.assertTrue(core.enemy_turn_pending)

    def test_dynamite_explodes_after_enemy_turns_and_kills_adjacent_bandit(self):
        core = GunchoCore(seed=5)
        dynamite_pos = core.first_free_neighbor(core.player)
        enemy = core.add_enemy(core.first_free_neighbor(dynamite_pos), kind="gun")
        dynamite = core.add_dynamite(dynamite_pos)

        core.perform_enemy_turn()
        core.perform_enemy_turn()
        core.perform_enemy_turn()

        self.assertTrue(dynamite.exploded)
        self.assertTrue(enemy.killed)

    def test_clearing_camp_advances_until_boss_victory(self):
        core = GunchoCore(seed=6)
        for enemy in list(core.enemies):
            enemy.kill()

        self.assertTrue(core.check_level_clear())
        self.assertEqual(core.advance_level(), 2)

        core.level = core.max_level
        for enemy in list(core.enemies):
            enemy.kill()
        self.assertTrue(core.check_level_clear())
        self.assertTrue(core.won)


if __name__ == "__main__":
    unittest.main()

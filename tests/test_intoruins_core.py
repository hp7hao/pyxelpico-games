from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "intoruins"
sys.path.insert(0, str(GAME_DIR))

from intoruins_core import Enemy, IntoRuinsCore  # noqa: E402


class IntoRuinsCoreTest(unittest.TestCase):
    def test_player_explores_visible_tiles_and_bumps_enemy(self):
        core = IntoRuinsCore(seed=1)
        core.enemies = [Enemy(11, 10, "goblin", hp=3, attack=1)]
        start_hp = core.enemies[0].hp

        core.step(1, 0)

        self.assertEqual((core.player_x, core.player_y), (10, 10))
        self.assertLess(core.enemies[0].hp, start_hp)
        self.assertGreater(len(core.explored), 12)

    def test_statuses_tick_down_and_hurt_or_block_player(self):
        core = IntoRuinsCore(seed=2)
        core.player_hp = 10
        core.statuses = {"burn": 2, "freeze": 1}

        core.step(1, 0)

        self.assertEqual((core.player_x, core.player_y), (10, 10))
        self.assertEqual(core.player_hp, 9)
        self.assertNotIn("freeze", core.statuses)
        self.assertEqual(core.statuses["burn"], 1)

    def test_ranged_enemy_attacks_when_in_line_of_sight(self):
        core = IntoRuinsCore(seed=3)
        core.enemies = [Enemy(14, 10, "archer", hp=3, attack=2, ranged=True)]
        start_hp = core.player_hp

        core.wait_turn()

        self.assertLess(core.player_hp, start_hp)

    def test_items_heal_light_and_freeze_nearby_enemies(self):
        core = IntoRuinsCore(seed=4)
        core.player_hp = 5
        core.items = {(10, 10): "torch", (10, 11): "potion", (10, 12): "frost"}
        core.enemies = [Enemy(12, 12, "shade", hp=3, attack=1)]

        core.wait_turn()
        core.step(0, 1)
        core.step(0, 1)

        self.assertGreaterEqual(core.light, 6)
        self.assertGreater(core.player_hp, 5)
        self.assertIn("freeze", core.enemies[0].statuses)

    def test_descending_deep_enough_finds_wings_and_wins(self):
        core = IntoRuinsCore(seed=5)
        for level in range(core.final_depth - 1):
            core.player_x, core.player_y = core.exit_pos
            core.descend()
            self.assertEqual(core.depth, level + 2)

        core.player_x, core.player_y = core.exit_pos
        core.descend()

        self.assertTrue(core.won)
        self.assertEqual(core.mode, "won")

    def test_player_loses_when_hp_reaches_zero(self):
        core = IntoRuinsCore(seed=6)
        core.player_hp = 1
        core.enemies = [Enemy(11, 10, "brute", hp=5, attack=2)]

        core.wait_turn()

        self.assertTrue(core.lost)
        self.assertEqual(core.mode, "lost")


if __name__ == "__main__":
    unittest.main()

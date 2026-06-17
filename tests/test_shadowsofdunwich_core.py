from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "shadowsofdunwich"
sys.path.insert(0, str(GAME_DIR))

from shadowsofdunwich_core import ShadowsOfDunwichCore  # noqa: E402


class ShadowsOfDunwichCoreTest(unittest.TestCase):
    def test_soldier_moves_spends_action_points_and_shoots_enemy(self):
        core = ShadowsOfDunwichCore(seed=1)
        core.enemies.clear()
        enemy = core.add_enemy((5, 2), kind="cultist", hp=1)

        self.assertTrue(core.move_soldier(0, (3, 2)))
        self.assertEqual(core.soldiers[0].pos, (3, 2))
        self.assertEqual(core.soldiers[0].ap, 1)

        self.assertTrue(core.shoot(0, enemy.pos))
        self.assertTrue(enemy.dead)
        self.assertEqual(core.soldiers[0].xp, 1)
        self.assertEqual(core.soldiers[0].ap, 0)

    def test_grenade_damages_cluster_and_splitter_creates_spawn(self):
        core = ShadowsOfDunwichCore(seed=2)
        core.enemies.clear()
        core.add_enemy((5, 4), kind="splitter", hp=1)
        core.add_enemy((6, 4), kind="thrall", hp=1)

        self.assertTrue(core.grenade(1, (5, 4)))

        living = [enemy for enemy in core.enemies if not enemy.dead]
        self.assertEqual(len(living), 2)
        self.assertTrue(all(enemy.kind == "spawn" for enemy in living))
        self.assertEqual(core.soldiers[1].xp, 2)

    def test_surviving_battle_levels_soldiers_and_advances_campaign(self):
        core = ShadowsOfDunwichCore(seed=3)
        core.enemies.clear()
        core.soldiers[0].xp = 2
        core.soldiers[1].xp = 1

        self.assertTrue(core.complete_battle())

        self.assertEqual(core.soldiers[0].level, 2)
        self.assertEqual(core.soldiers[0].skill_points, 1)
        self.assertGreater(core.campaign_level, 1)
        self.assertFalse(core.victory)

    def test_casualties_are_replaced_and_level_sixteen_wins_campaign(self):
        core = ShadowsOfDunwichCore(seed=4)
        core.enemies.clear()
        core.campaign_level = 16
        core.soldiers[2].alive = False

        self.assertTrue(core.complete_battle())

        self.assertTrue(core.victory)
        self.assertTrue(core.soldiers[2].alive)
        self.assertIn("recruit", core.soldiers[2].name.lower())
        self.assertGreaterEqual(core.soldiers[2].skill_points, 1)


if __name__ == "__main__":
    unittest.main()

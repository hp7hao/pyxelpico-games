from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "dungeonbang"
sys.path.insert(0, str(GAME_DIR))

from dungeonbang_core import DungeonBangCore  # noqa: E402


class DungeonBangCoreTest(unittest.TestCase):
    def test_movement_jump_and_wall_jump(self):
        core = DungeonBangCore(seed=1)
        core.player.x = 6
        core.player.grounded = False

        core.tick(move=1, jump=True)

        self.assertGreater(core.player.vx, 0)
        self.assertLess(core.player.vy, 0)
        self.assertEqual(core.message, "wall jump")

    def test_collecting_coins_and_buying_shop_powerup(self):
        core = DungeonBangCore(seed=2)
        core.coins = 8

        bought = core.buy_powerup("sword")

        self.assertTrue(bought)
        self.assertTrue(core.powerups["sword"])
        self.assertLess(core.coins, 8)

    def test_attack_defeats_enemy_and_awards_coins(self):
        core = DungeonBangCore(seed=3)
        enemy_count = len(core.enemies)

        core.player.x = core.enemies[0]["x"] - 8
        core.attack()

        self.assertLess(len(core.enemies), enemy_count)
        self.assertGreater(core.coins, 0)

    def test_portal_advances_zone_and_final_rescue_wins(self):
        core = DungeonBangCore(seed=4)
        core.player.x = core.portal_x
        core.enter_portal()
        self.assertEqual(core.depth, 2)

        core.depth = core.final_depth
        core.player.x = core.portal_x
        core.enter_portal()
        self.assertTrue(core.victory)
        self.assertEqual(core.message, "princess rescued")


if __name__ == "__main__":
    unittest.main()

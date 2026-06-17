from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "picosnail"
sys.path.insert(0, str(GAME_DIR))

from picosnail_core import PicoSnailCore  # noqa: E402


class PicoSnailCoreTest(unittest.TestCase):
    def test_collecting_stars_enables_double_jump_and_wand_shot(self):
        core = PicoSnailCore(seed=1)
        core.collect_star()
        core.tick(jump=True)
        core.tick(jump=True)

        self.assertEqual(core.stars, 0)
        self.assertLess(core.player.vy, 0)
        self.assertEqual(core.message, "double jump")

        core.collect_star()
        self.assertTrue(core.cast_wand())
        self.assertEqual(core.stars, 0)
        self.assertEqual(len(core.shots), 1)

    def test_centered_thwack_defeats_thorn_enemy(self):
        core = PicoSnailCore(seed=2)
        enemy_count = len(core.enemies)
        core.player.x = core.enemies[0]["x"] - 8

        self.assertTrue(core.thwack())

        self.assertLess(len(core.enemies), enemy_count)
        self.assertEqual(core.message, "dream safe")

    def test_hazard_spends_star_before_health(self):
        core = PicoSnailCore(seed=3)
        core.collect_star()
        core.hit_hazard("salt")

        self.assertEqual(core.stars, 0)
        self.assertEqual(core.health, core.max_health)

        core.hit_hazard("thorn")
        self.assertLess(core.health, core.max_health)
        self.assertEqual(core.message, "ouch thorn")

    def test_switch_opens_door_and_warp_advances_level(self):
        core = PicoSnailCore(seed=4)

        self.assertFalse(core.door_open)
        core.press_switch()
        self.assertTrue(core.door_open)

        core.player.x = core.warp_x
        self.assertTrue(core.enter_warp())
        self.assertEqual(core.level_index, 1)
        self.assertEqual(core.level_name, "courtyard")

    def test_cat_boss_requires_open_door_then_final_warp_wins(self):
        core = PicoSnailCore(seed=5)
        core.level_index = core.boss_level
        core.level_name = core.levels[core.level_index]
        core.boss_hp = 1

        self.assertFalse(core.attack_boss())
        core.press_switch()
        self.assertTrue(core.attack_boss())
        self.assertTrue(core.boss_defeated)

        core.player.x = core.warp_x
        self.assertTrue(core.enter_warp())
        self.assertTrue(core.victory)
        self.assertEqual(core.message, "dream castle saved")


if __name__ == "__main__":
    unittest.main()

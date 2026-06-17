from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "scrapboy"
sys.path.insert(0, str(GAME_DIR))

from scrapboy_core import ScrapBoyCore  # noqa: E402


class ScrapBoyCoreTest(unittest.TestCase):
    def test_runs_jumps_and_collects_scrap(self):
        core = ScrapBoyCore(seed=1)
        core.scraps = {(3, 9)}

        for _ in range(10):
            core.tick(right=True)
        core.move_to_tile(3, 9)
        core.tick()

        self.assertGreater(core.x, core.spawn_x)
        self.assertEqual(core.scrap, 1)
        self.assertNotIn((3, 9), core.scraps)

    def test_shot_defeats_enemy_and_bomb_opens_door(self):
        core = ScrapBoyCore(seed=2)
        core.enemies = {(5, 9): 1}
        core.weapon = "laser"
        core.move_to_tile(3, 9)

        self.assertTrue(core.shoot(1, 0))
        self.assertNotIn((5, 9), core.enemies)
        self.assertGreater(core.score, 0)

        core.weapon = "bomb"
        self.assertIn((7, 9), core.doors)
        self.assertTrue(core.shoot(1, 0))
        self.assertNotIn((7, 9), core.doors)

    def test_spikes_damage_normal_form_but_not_bomb_armor(self):
        core = ScrapBoyCore(seed=3)
        spike = next(iter(core.spikes))

        core.move_to_tile(*spike)
        core.tick()
        self.assertEqual(core.hp, 2)

        core.weapon = "bomb"
        core.move_to_tile(*spike)
        core.tick()
        self.assertEqual(core.hp, 2)

    def test_magnet_wall_jump_and_collectible_goal_clear(self):
        core = ScrapBoyCore(seed=4)
        core.weapon = "magnet"
        core.move_to_tile(1, 8)

        self.assertTrue(core.wall_jump(direction=1))
        self.assertGreater(core.vx, 0)
        self.assertLess(core.vy, 0)

        core.scraps.clear()
        core.move_to_tile(*core.exit)
        core.tick()
        self.assertTrue(core.level_clear)


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "birdswithguns"
sys.path.insert(0, str(GAME_DIR))

from birdswithguns_core import BirdsCore, Weapon  # noqa: E402


class BirdsWithGunsCoreTest(unittest.TestCase):
    def test_player_movement_is_clamped_to_train_bounds(self):
        core = BirdsCore(seed=1)
        for _ in range(80):
            core.move_player(-1, -1)
        self.assertEqual(core.player_x, 12)
        self.assertEqual(core.player_y, 24)

        for _ in range(160):
            core.move_player(1, 1)
        self.assertEqual(core.player_x, core.width - 12)
        self.assertEqual(core.player_y, core.height - 18)

    def test_revolver_shot_damages_nearest_enemy_and_can_clear_wagon(self):
        core = BirdsCore(seed=1)
        core.enemies = []
        enemy = core.spawn_enemy(core.player_x + 28, core.player_y)

        self.assertTrue(core.shoot())
        for _ in range(8):
            core.tick()
        self.assertEqual(enemy.hp, 1)
        for _ in range(12):
            core.tick()
        self.assertTrue(core.shoot())
        for _ in range(8):
            core.tick()
        self.assertTrue(enemy.dead)

        core.tick()
        self.assertEqual(core.wagon, 2)
        self.assertGreater(len(core.enemies), 0)

    def test_weapon_swap_changes_fire_profile(self):
        core = BirdsCore(seed=1)
        self.assertEqual(core.weapon, Weapon.REVOLVER)
        core.swap_weapon()
        self.assertEqual(core.weapon, Weapon.SHOTGUN)
        core.swap_weapon()
        self.assertEqual(core.weapon, Weapon.REVOLVER)

    def test_player_can_lose_and_boss_clear_wins(self):
        core = BirdsCore(seed=1)
        core.player_hp = 1
        enemy = core.spawn_enemy(core.player_x, core.player_y)
        core._touch_enemy(enemy)
        self.assertTrue(core.lost)

        core = BirdsCore(seed=1)
        core.wagon = core.final_wagon
        core.enemies = []
        boss = core.spawn_enemy(core.player_x + 20, core.player_y, boss=True)
        for _ in range(240):
            core.shoot()
            core.tick()
            if boss.dead:
                break
        core.tick()
        self.assertTrue(core.won)


if __name__ == "__main__":
    unittest.main()

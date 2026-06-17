from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "buns"
sys.path.insert(0, str(GAME_DIR))

from buns_core import BunsCore, Upgrade  # noqa: E402


class BunsCoreTest(unittest.TestCase):
    def test_player_moves_and_stays_inside_arena(self):
        core = BunsCore(seed=1)
        for _ in range(200):
            core.move_player(-1, -1)
        self.assertEqual(core.player_x, 12)
        self.assertEqual(core.player_y, 20)

        for _ in range(240):
            core.move_player(1, 1)
        self.assertEqual(core.player_x, core.width - 12)
        self.assertEqual(core.player_y, core.height - 12)

    def test_auto_fire_kills_enemy_and_drops_gem(self):
        core = BunsCore(seed=1)
        core.enemies = []
        enemy = core.spawn_enemy(core.player_x + 20, core.player_y, hp=1)

        for _ in range(20):
            core.tick()
            if enemy.dead:
                break

        self.assertTrue(enemy.dead)
        self.assertEqual(len(core.gems), 1)
        self.assertEqual(core.kills, 1)

    def test_collecting_gems_levels_up_and_upgrade_changes_stats(self):
        core = BunsCore(seed=1)
        core.exp = core.exp_needed - 1
        core.spawn_gem(core.player_x, core.player_y)

        core.tick()

        self.assertTrue(core.awaiting_upgrade)
        self.assertEqual(core.level, 1)
        core.apply_upgrade(Upgrade.DAMAGE)
        self.assertFalse(core.awaiting_upgrade)
        self.assertEqual(core.damage, 2)

    def test_enemy_touch_damages_player_once_per_iframe_window(self):
        core = BunsCore(seed=1)
        core.enemies = []
        enemy = core.spawn_enemy(core.player_x, core.player_y, hp=2)

        core.tick()
        self.assertEqual(core.player_hp, core.max_hp - 1)
        core.tick()
        self.assertEqual(core.player_hp, core.max_hp - 1)
        self.assertTrue(enemy.dead)

    def test_boss_timer_spawns_boss_and_boss_death_wins(self):
        core = BunsCore(seed=1)
        core.enemies = []
        core.timer = core.boss_time - 1
        core.tick()

        boss = next(enemy for enemy in core.enemies if enemy.boss)
        boss.hp = 1
        core._damage_enemy(boss, 1)
        core.tick()
        self.assertTrue(core.won)


if __name__ == "__main__":
    unittest.main()

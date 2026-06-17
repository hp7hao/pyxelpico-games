from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "subsurface"
sys.path.insert(0, str(GAME_DIR))

from subsurface_core import SubsurfaceCore  # noqa: E402


class SubsurfaceCoreTest(unittest.TestCase):
    def test_collecting_upgrades_unlocks_movement_options(self):
        core = SubsurfaceCore(seed=1)

        core.collect_upgrade("wall_jump")
        core.collect_upgrade("glide")
        core.collect_upgrade("swim")

        self.assertTrue(core.upgrades["wall_jump"])
        self.assertTrue(core.upgrades["glide"])
        self.assertTrue(core.upgrades["swim"])
        self.assertEqual(core.message, "swim unlocked")

    def test_shooting_defeats_enemy_and_opens_path(self):
        core = SubsurfaceCore(seed=2)
        enemy_count = len(core.enemies)

        core.player.x = 62
        core.shoot()
        for _ in range(20):
            core.tick()

        self.assertLess(len(core.enemies), enemy_count)
        self.assertGreater(core.energy, 0)

    def test_water_requires_swim_upgrade(self):
        core = SubsurfaceCore(seed=3)
        core.player.x = 114
        core.player.y = 178

        core.tick()
        self.assertLess(core.health, core.max_health)

        core.collect_upgrade("swim")
        health_after = core.health
        core.tick()
        self.assertEqual(core.health, health_after)

    def test_boss_defeat_wins(self):
        core = SubsurfaceCore(seed=4)
        core.collect_upgrade("gun")
        core.boss_hp = 2
        core.player.x = core.boss_x - 16

        for _ in range(3):
            core.shoot()
            core.tick()

        self.assertTrue(core.victory)
        self.assertEqual(core.message, "surface reached")


if __name__ == "__main__":
    unittest.main()

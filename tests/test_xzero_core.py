from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "xzero"
sys.path.insert(0, str(GAME_DIR))

from xzero_core import Enemy, XZeroCore  # noqa: E402


class XZeroCoreTest(unittest.TestCase):
    def test_player_moves_jumps_and_lands_on_floor(self):
        core = XZeroCore(seed=1)
        start_x = core.player_x
        core.move(1)
        core.jump()

        for _ in range(40):
            core.tick()

        self.assertGreater(core.player_x, start_x)
        self.assertTrue(core.on_ground)
        self.assertEqual(core.player_y, core.ground_y)

    def test_shot_uses_aim_direction_and_can_defeat_enemy(self):
        core = XZeroCore(seed=2)
        core.enemies = [Enemy(core.player_x + 24, core.player_y, hp=2)]
        core.aim_y = 0

        core.shoot()
        for _ in range(8):
            core.tick()
        core.shoot()
        for _ in range(8):
            core.tick()

        self.assertTrue(core.enemies[0].dead)
        self.assertEqual(core.score, 10)

    def test_enemy_contact_damages_player_once_per_iframe_window(self):
        core = XZeroCore(seed=3)
        core.enemies = [Enemy(core.player_x, core.player_y, hp=2)]

        core.tick()
        hp = core.player_hp
        core.tick()

        self.assertEqual(hp, core.max_hp - 1)
        self.assertEqual(core.player_hp, hp)

    def test_pickup_restores_health_and_increases_score(self):
        core = XZeroCore(seed=4)
        core.player_hp = core.max_hp - 2
        core.pickups = [(core.player_x, core.player_y)]

        core.tick()

        self.assertEqual(core.player_hp, core.max_hp)
        self.assertEqual(core.score, 5)
        self.assertEqual(core.pickups, [])

    def test_reaching_exit_advances_zone_and_final_zone_wins(self):
        core = XZeroCore(seed=5)
        core.player_x = core.exit_x

        core.tick()

        self.assertEqual(core.zone, 2)
        core.zone = core.final_zone
        core.player_x = core.exit_x
        core.tick()
        self.assertTrue(core.won)


if __name__ == "__main__":
    unittest.main()

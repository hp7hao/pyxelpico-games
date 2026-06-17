from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "littledragon"
sys.path.insert(0, str(GAME_DIR))

from littledragon_core import LittleDragonCore  # noqa: E402


class LittleDragonCoreTest(unittest.TestCase):
    def test_dragon_runs_jumps_and_lands_on_floor(self):
        core = LittleDragonCore(seed=1)
        start_x = core.player.x

        for _ in range(8):
            core.tick(right=True)
        core.tick(jump=True)
        airborne_y = core.player.y
        for _ in range(50):
            core.tick(right=True)

        self.assertGreater(core.player.x, start_x + 20)
        self.assertLess(airborne_y, core.floor_y)
        self.assertTrue(core.player.on_ground)

    def test_double_jump_allows_second_air_jump_once(self):
        core = LittleDragonCore(seed=2)

        core.tick(jump=True)
        first_dy = core.player.dy
        for _ in range(4):
            core.tick()
        core.tick(jump=True)
        second_dy = core.player.dy
        for _ in range(2):
            core.tick()
        core.tick(jump=True)

        self.assertLess(first_dy, 0)
        self.assertLess(second_dy, 0)
        self.assertEqual(core.player.jumps_left, 0)

    def test_fireball_defeats_enemy_and_awards_egg(self):
        core = LittleDragonCore(seed=3)
        core.enemies[0].x = core.player.x + 18
        core.enemies[0].y = core.player.y
        core.enemies[0].hp = 1

        core.tick(fire=True)
        for _ in range(10):
            core.tick()

        self.assertEqual(core.eggs, 1)
        self.assertFalse(core.enemies[0].alive)
        self.assertEqual(core.message, "egg rescued")

    def test_checkpoint_respawns_dragon_after_hazard(self):
        core = LittleDragonCore(seed=4)
        core.player.x = core.checkpoint_x
        core.tick()
        core.player.x = core.hazards[0][0]
        core.player.y = core.hazards[0][1]

        core.tick()

        self.assertEqual(core.deaths, 1)
        self.assertEqual(round(core.player.x), core.checkpoint_x)
        self.assertEqual(core.message, "checkpoint")

    def test_boss_requires_eggs_and_fireballs_to_clear(self):
        core = LittleDragonCore(seed=5)
        core.eggs = core.total_eggs
        core.player.x = core.boss.x - 28
        core.player.y = core.boss.y
        core.player.facing = 1
        for enemy in core.enemies:
            enemy.alive = False

        for _ in range(3):
            core.tick(fire=True)
            for _ in range(10):
                core.tick()

        self.assertTrue(core.cleared)
        self.assertEqual(core.message, "eggs saved")

    def test_boss_gate_blocks_until_all_eggs_are_rescued(self):
        core = LittleDragonCore(seed=6)
        core.player.x = core.boss.x - 28
        core.player.y = core.boss.y
        core.player.facing = 1
        for enemy in core.enemies:
            enemy.alive = False

        core.tick(fire=True)
        for _ in range(10):
            core.tick()

        self.assertFalse(core.cleared)
        self.assertEqual(core.message, "need dragon eggs")


if __name__ == "__main__":
    unittest.main()

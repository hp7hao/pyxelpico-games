from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "trialsorcerer"
sys.path.insert(0, str(GAME_DIR))

from trialsorcerer_core import TrialSorcererCore  # noqa: E402


class TrialSorcererCoreTest(unittest.TestCase):
    def test_seeded_dungeon_contains_start_loot_key_door_and_exit(self):
        core = TrialSorcererCore(seed=7)

        self.assertEqual(core.level, 1)
        self.assertEqual(core.player_tile(), core.start_tile)
        self.assertIn(core.key_tile, core.pickups)
        self.assertEqual(core.tile_at(*core.door_tile), "D")
        self.assertEqual(core.tile_at(*core.exit_tile), "E")
        self.assertGreaterEqual(len(core.monsters), 2)

    def test_turning_forward_and_strafing_respect_walls(self):
        core = TrialSorcererCore(seed=1)
        start = core.player_tile()

        core.tick(forward=True)
        moved = core.player_tile()
        core.tick(turn_right=True)
        core.tick(forward=True)
        after_turn = core.player_tile()
        core.tick(strafe=True, turn_left=True)
        after_strafe = core.player_tile()

        self.assertNotEqual(moved, start)
        self.assertNotEqual(after_turn, moved)
        self.assertNotEqual(after_strafe, after_turn)
        self.assertNotEqual(core.tile_at(*after_strafe), "#")

    def test_staff_shot_defeats_monster_and_awards_loot(self):
        core = TrialSorcererCore(seed=2)
        core.monsters = [core.monsters[0]]
        monster = core.monsters[0]
        monster.x = core.x + 2
        monster.y = core.y
        monster.hp = core.staff_power
        core.facing = 0

        core.tick(shoot=True)

        self.assertFalse(monster.alive)
        self.assertEqual(core.loot, 1)
        self.assertEqual(core.message, "monster banished")

    def test_key_opens_matching_locked_door(self):
        core = TrialSorcererCore(seed=3)
        core.x, core.y = core.key_tile

        core.tick()
        self.assertEqual(core.keys, 1)
        self.assertNotIn(core.key_tile, core.pickups)

        core.x, core.y = core.door_tile[0] - 1, core.door_tile[1]
        core.facing = 0
        core.tick(forward=True)

        self.assertEqual(core.keys, 0)
        self.assertEqual(core.tile_at(*core.door_tile), ".")
        self.assertEqual(core.player_tile(), core.door_tile)

    def test_crystal_levels_staff_and_exit_advances_level(self):
        core = TrialSorcererCore(seed=4)
        core.x, core.y = core.crystal_tile


        core.tick()
        self.assertEqual(core.staff_power, 2)

        core.x, core.y = core.exit_tile
        core.tick()

        self.assertEqual(core.level, 2)
        self.assertEqual(core.staff_power, 2)
        self.assertEqual(core.message, "deeper into the realm")

    def test_final_boss_defeat_clears_trial(self):
        core = TrialSorcererCore(seed=5)
        core.level = core.final_level
        core._build_level()
        boss = next(monster for monster in core.monsters if monster.kind == "bahmott")
        boss.x = core.x + 2
        boss.y = core.y
        boss.hp = core.staff_power
        core.facing = 0

        core.tick(shoot=True)

        self.assertTrue(core.cleared)
        self.assertEqual(core.message, "bahmott defeated")


if __name__ == "__main__":
    unittest.main()

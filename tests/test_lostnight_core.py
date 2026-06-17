from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "lostnight"
sys.path.insert(0, str(GAME_DIR))

from lostnight_core import LostNightCore  # noqa: E402


class LostNightCoreTest(unittest.TestCase):
    def test_player_moves_between_rooms_and_finds_encounter(self):
        core = LostNightCore(seed=1)
        start_room = core.room

        for _ in range(32):
            core.tick_overworld(right=True)

        self.assertNotEqual(core.room, start_room)
        self.assertEqual(core.mode, "battle")
        self.assertGreater(core.enemy.hp, 0)
        self.assertEqual(core.message, "night shape appears")

    def test_bullets_damage_player_unless_dodged(self):
        core = LostNightCore(seed=2)
        core.start_battle("drifter")
        core.player.x = core.enemy_bullets[0].x
        core.player.y = core.enemy_bullets[0].y
        before = core.hp

        core.tick_battle()

        self.assertLess(core.hp, before)
        self.assertEqual(core.message, "hit by a spark")

    def test_player_shots_clear_enemy_for_candy_and_room_key(self):
        core = LostNightCore(seed=3)
        core.start_battle("drifter")
        core.enemy.hp = 3

        core.fire()
        for _ in range(8):
            core.tick_battle()

        self.assertEqual(core.mode, "overworld")
        self.assertGreater(core.candy, 0)
        self.assertIn(core.room, core.cleared_rooms)

    def test_tea_heals_and_spends_inventory(self):
        core = LostNightCore(seed=4)
        core.hp = 2
        core.tea = 1

        core.drink_tea()

        self.assertEqual(core.hp, 7)
        self.assertEqual(core.tea, 0)
        self.assertEqual(core.message, "warm tea +5hp")

    def test_shop_upgrades_cost_candy_and_improve_stats(self):
        core = LostNightCore(seed=5)
        core.candy = 9

        core.buy_upgrade("power")
        core.buy_upgrade("speed")

        self.assertEqual(core.power_level, 2)
        self.assertEqual(core.speed_level, 2)
        self.assertEqual(core.candy, 1)

    def test_defeating_all_rooms_unlocks_dawn(self):
        core = LostNightCore(seed=6)
        core.cleared_rooms = set(core.encounter_rooms[:-1])
        core.room = core.encounter_rooms[-1]
        core.start_battle("boss")
        core.enemy.hp = 1

        core.fire()
        for _ in range(8):
            core.tick_battle()

        self.assertEqual(core.mode, "clear")
        self.assertEqual(core.message, "dawn returns")


if __name__ == "__main__":
    unittest.main()

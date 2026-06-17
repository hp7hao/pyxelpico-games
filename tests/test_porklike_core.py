from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "porklike"
sys.path.insert(0, str(GAME_DIR))

from porklike_core import MoveResult, PorklikeCore, Tile  # noqa: E402


class PorklikeCoreTest(unittest.TestCase):
    def test_dungeon_generation_places_exit_and_reachable_floor(self):
        core = PorklikeCore(seed=4)

        self.assertEqual(core.level, 1)
        self.assertEqual(core.tile_at(core.exit_x, core.exit_y), Tile.EXIT)
        self.assertGreater(core.floor_count(), 45)
        self.assertNotEqual((core.player_x, core.player_y), (core.exit_x, core.exit_y))

    def test_player_movement_blocks_walls_and_consumes_turn_on_floor(self):
        core = PorklikeCore(seed=3)
        core.set_test_map(
            [
                "#####",
                "#@..#",
                "###>#",
                "#####",
            ]
        )

        self.assertEqual(core.move_player(-1, 0), MoveResult.BLOCKED)
        self.assertEqual((core.player_x, core.player_y), (1, 1))
        self.assertEqual(core.turn, 0)

        self.assertEqual(core.move_player(1, 0), MoveResult.MOVED)
        self.assertEqual((core.player_x, core.player_y), (2, 1))
        self.assertEqual(core.turn, 1)

    def test_bumping_enemy_attacks_and_defeated_enemy_drops_food(self):
        core = PorklikeCore(seed=1)
        core.set_test_map(
            [
                "#####",
                "#@e.#",
                "#..>#",
                "#####",
            ]
        )
        enemy = core.enemies[0]
        enemy.hp = 2

        self.assertEqual(core.move_player(1, 0), MoveResult.ATTACKED)

        self.assertTrue(enemy.dead)
        self.assertEqual(core.score, 10)
        self.assertTrue(any(item.kind == "food" for item in core.items))
        self.assertEqual((core.player_x, core.player_y), (1, 1))

    def test_enemy_turn_attacks_adjacent_player_and_can_end_run(self):
        core = PorklikeCore(seed=2)
        core.set_test_map(
            [
                "#####",
                "#@e>#",
                "#####",
            ]
        )
        core.player_hp = 1

        core.move_player(0, 0)

        self.assertTrue(core.lost)
        self.assertEqual(core.player_hp, 0)

    def test_collect_food_restores_health_and_exit_advances_level(self):
        core = PorklikeCore(seed=5)
        core.set_test_map(
            [
                "#####",
                "#@f>#",
                "#####",
            ]
        )
        core.player_hp = core.max_hp - 2


        self.assertEqual(core.move_player(1, 0), MoveResult.ITEM)
        self.assertEqual(core.player_hp, core.max_hp)
        self.assertEqual(core.move_player(1, 0), MoveResult.EXIT)
        self.assertEqual(core.level, 2)
        self.assertEqual(core.player_hp, core.max_hp)


if __name__ == "__main__":
    unittest.main()

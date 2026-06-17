from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "pcraft"
sys.path.insert(0, str(GAME_DIR))

from pcraft_core import PCraftCore  # noqa: E402


class PCraftCoreTest(unittest.TestCase):
    def test_seeded_island_has_spawn_resources_workbench_cave_and_boat_site(self):
        core = PCraftCore(seed=1)

        self.assertEqual(core.player_pos(), core.spawn)
        self.assertGreaterEqual(core.count_tiles("tree"), 4)
        self.assertGreaterEqual(core.count_tiles("stone"), 2)
        self.assertEqual(core.tile_at(*core.workbench), "workbench")
        self.assertEqual(core.tile_at(*core.cave), "cave")
        self.assertEqual(core.tile_at(*core.boat_site), "shore")

    def test_gather_tree_and_stone_with_basic_tools(self):
        core = PCraftCore(seed=2)
        tree = core.find_tile("tree")
        stone = core.find_tile("stone")

        core.move_to(*tree)
        core.use_equipped()
        core.move_to(*stone)
        core.use_equipped()

        self.assertGreaterEqual(core.inventory["wood"], 2)
        self.assertGreaterEqual(core.inventory["stone"], 1)
        self.assertEqual(core.tile_at(*tree), "grass")
        self.assertEqual(core.tile_at(*stone), "grass")

    def test_workbench_crafts_axe_then_sword(self):
        core = PCraftCore(seed=3)
        core.inventory.update({"wood": 6, "stone": 3})
        core.move_to(*core.workbench)

        self.assertTrue(core.craft("axe"))
        self.assertIn("axe", core.tools)
        self.assertTrue(core.craft("sword"))
        self.assertIn("sword", core.tools)
        self.assertEqual(core.message, "crafted sword")

    def test_axe_increases_wood_yield(self):
        core = PCraftCore(seed=4)
        tree = core.find_tile("tree")
        core.tools.add("axe")

        core.move_to(*tree)
        core.use_equipped()

        self.assertEqual(core.inventory["wood"], 4)

    def test_cave_requires_sword_and_rewards_crystal(self):
        core = PCraftCore(seed=5)
        core.move_to(*core.cave)

        self.assertFalse(core.explore_cave())
        self.assertEqual(core.message, "need a sword")

        core.tools.add("sword")
        self.assertTrue(core.explore_cave())

        self.assertEqual(core.inventory["crystal"], 1)
        self.assertTrue(core.cave_cleared)

    def test_boat_escape_requires_boat_recipe_and_shore(self):
        core = PCraftCore(seed=6)
        core.inventory.update({"wood": 10, "fiber": 4, "crystal": 1})
        core.move_to(*core.workbench)

        self.assertTrue(core.craft("boat"))
        self.assertIn("boat", core.tools)
        core.move_to(*core.boat_site)
        core.use_equipped()

        self.assertTrue(core.escaped)
        self.assertEqual(core.message, "escaped the island")


if __name__ == "__main__":
    unittest.main()

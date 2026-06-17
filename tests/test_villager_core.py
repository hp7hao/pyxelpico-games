from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "villager"
sys.path.insert(0, str(GAME_DIR))

from villager_core import VillagerCore  # noqa: E402


class VillagerCoreTest(unittest.TestCase):
    def test_gathering_resources_from_world_tiles(self):
        core = VillagerCore(seed=1)
        core.cursor = (2, 2)
        core.world[(2, 2)] = "tree"

        gained = core.gather()

        self.assertEqual(gained, "wood")
        self.assertGreater(core.resources["wood"], 5)
        self.assertEqual(core.world[(2, 2)], "grass")

    def test_build_house_invites_peeple(self):
        core = VillagerCore(seed=2)
        core.resources.update({"wood": 20, "stone": 10, "food": 5})

        self.assertTrue(core.build("house"))

        for _ in range(core.arrival_delay):
            core.tick()
        self.assertGreater(core.population, 0)

    def test_workshop_and_farm_produce_when_population_is_happy(self):
        core = VillagerCore(seed=3)
        core.resources.update({"wood": 30, "stone": 30, "food": 20})
        core.population = 2
        core.happiness = 80
        core.build("workshop")
        core.cursor = (core.cursor[0] + 1, core.cursor[1])
        core.build("farm")
        before = dict(core.resources)

        for _ in range(core.production_interval):
            core.tick()

        self.assertGreater(core.resources["wood"], before["wood"])
        self.assertGreater(core.resources["food"], before["food"])

    def test_hungry_sad_peeple_leave(self):
        core = VillagerCore(seed=4)
        core.population = 3
        core.resources["food"] = 0
        core.happiness = 10

        for _ in range(core.production_interval * 2):
            core.tick()

        self.assertLess(core.population, 3)
        self.assertEqual(core.message, "somebody left")


if __name__ == "__main__":
    unittest.main()

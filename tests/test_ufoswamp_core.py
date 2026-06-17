from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "ufoswamp"
sys.path.insert(0, str(GAME_DIR))

from ufoswamp_core import UfoSwampCore  # noqa: E402


class UfoSwampCoreTest(unittest.TestCase):
    def test_platform_movement_jump_and_water_buoyancy(self):
        core = UfoSwampCore(seed=1)
        start_x = core.player.x

        for _ in range(12):
            core.tick(right=True)
        self.assertGreater(core.player.x, start_x + 5)

        core.player.on_ground = True
        core.tick(jump=True)
        self.assertLess(core.player.dy, 0)

        core.player.y = core.water_y + 8
        core.player.dy = 2.0
        core.tick()
        self.assertLess(core.player.dy, 2.0)
        self.assertEqual(core.message, "swamp bounce")

    def test_collects_score_and_unlocks_zapper_modes(self):
        core = UfoSwampCore(seed=2)
        core.set_test_room([
            "################",
            "#..............#",
            "#@..s.E.p.g....#",
            "################",
        ])

        for _ in range(120):
            core.tick(right=True)

        self.assertEqual(core.score, 10)
        self.assertEqual(core.unlocked_guns, 3)
        self.assertEqual(core.gun, "grapple")

    def test_emp_zapper_stuns_enemies_and_can_destroy_core(self):
        core = UfoSwampCore(seed=3)
        core.set_test_room([
            "####################",
            "#..................#",
            "#@E.e..........C...#",
            "####################",
        ])
        for _ in range(20):
            core.tick(right=True)
        core.tick(shoot=True)

        self.assertGreater(core.enemies[0].stunned, 0)
        self.assertEqual(core.message, "eyebot stunned")

        core.player.x = core.core_x + 32
        core.player.y = core.core_y
        core.player.facing = -1
        for _ in range(core.core_charge_ticks):
            core.tick(shoot=True)

        self.assertTrue(core.cleared)
        self.assertEqual(core.message, "emp cannon disabled")

    def test_portal_zapper_teleports_between_linked_stands(self):
        core = UfoSwampCore(seed=4)
        core.set_test_room([
            "####################",
            "#..................#",
            "#@p...1........2...#",
            "####################",
        ])
        for _ in range(20):
            core.tick(right=True)
        core.select_gun("portal")
        core.tick(shoot=True)

        self.assertAlmostEqual(core.player.x, core.portals[2][0] * core.tile, delta=core.tile)
        self.assertEqual(core.message, "portal jump")

    def test_grapple_zapper_pulls_toward_blue_hook(self):
        core = UfoSwampCore(seed=5)
        core.set_test_room([
            "####################",
            "#........H.........#",
            "#@g................#",
            "####################",
        ])
        for _ in range(20):
            core.tick(right=True)
        core.select_gun("grapple")
        before = core.player.x
        core.tick(shoot=True)

        self.assertGreater(core.player.x, before)
        self.assertLess(core.player.dy, 0)
        self.assertEqual(core.message, "grapple")


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "airdelivery"
sys.path.insert(0, str(GAME_DIR))

from airdelivery_core import AirDeliveryCore  # noqa: E402


class AirDeliveryCoreTest(unittest.TestCase):
    def test_walk_jump_coyote_and_glide(self):
        core = AirDeliveryCore(seed=1)
        start_x = core.player.x
        for _ in range(10):
            core.tick(right=True)
        self.assertGreater(core.player.x, start_x + 4)

        core.player.on_ground = False
        core.player.coyote = 5
        core.tick(jump=True)
        self.assertLess(core.player.dy, 0)

        core.player.has_glider = True
        core.player.dy = 4.0
        core.tick(interact=True)
        self.assertLessEqual(core.player.dy, core.glide_fall_speed)
        self.assertEqual(core.message, "glide")

    def test_ladder_climb_uses_up_and_down_controls(self):
        core = AirDeliveryCore(seed=2)
        core.set_test_room([
            "################",
            "#......H.......#",
            "#......H.......#",
            "#@.....H.......#",
            "################",
        ])
        core.player.x = 7 * core.tile
        core.player.y = 3 * core.tile
        before = core.player.y
        core.tick(up=True)

        self.assertLess(core.player.y, before)
        self.assertTrue(core.player.on_ladder)

    def test_collects_letters_and_delivers_to_recipient(self):
        core = AirDeliveryCore(seed=3)
        core.set_test_room([
            "####################",
            "#..................#",
            "#@..L......R.......#",
            "####################",
        ])
        for _ in range(25):
            core.tick(right=True)
        self.assertEqual(core.letters, 1)

        for _ in range(55):
            core.tick(right=True)
        core.tick(interact=True)

        self.assertEqual(core.delivered, 1)
        self.assertEqual(core.letters, 0)
        self.assertTrue(core.player.has_glider)
        self.assertEqual(core.message, "letter delivered")

    def test_drill_opens_secret_passage_after_delivery_reward(self):
        core = AirDeliveryCore(seed=4)
        core.set_test_room([
            "####################",
            "#..................#",
            "#@..L.R..D......A..#",
            "####################",
        ])
        for _ in range(55):
            core.tick(right=True)
        core.tick(interact=True)
        self.assertTrue(core.player.has_drill)

        for _ in range(35):
            core.tick(right=True)
        core.tick(interact=True)

        self.assertEqual(core.tile_at(*core.player_tile()), ".")
        self.assertEqual(core.message, "secret passage")

    def test_hazard_respawns_and_airship_requires_all_deliveries(self):
        core = AirDeliveryCore(seed=5)
        core.set_test_room([
            "####################",
            "#..................#",
            "#@..^....A.........#",
            "####################",
        ])
        for _ in range(25):
            core.tick(right=True)
        self.assertEqual(core.deaths, 1)

        core.player.x = core.airship_x * core.tile
        core.player.y = core.airship_y * core.tile
        core.total_recipients = 1
        core.tick(interact=True)
        self.assertFalse(core.cleared)

        core.total_recipients = 0
        core.tick(interact=True)
        self.assertTrue(core.cleared)


if __name__ == "__main__":
    unittest.main()

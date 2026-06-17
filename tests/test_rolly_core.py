from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "rolly"
sys.path.insert(0, str(GAME_DIR))

from rolly_core import RollyCore  # noqa: E402


class RollyCoreTest(unittest.TestCase):
    def test_seeded_level_has_spawn_friend_orbs_spikes_and_exit(self):
        core = RollyCore(seed=1)

        self.assertEqual(core.player_pos(), core.spawn)
        self.assertGreaterEqual(len(core.orbs), 2)
        self.assertGreaterEqual(len(core.spikes), 1)
        self.assertGreaterEqual(len(core.friends), 1)
        self.assertIn(core.exit, core.solid)

    def test_walk_jump_and_gravity_land_on_floor(self):
        core = RollyCore(seed=2)

        core.tick(right=True)
        self.assertGreater(core.x, core.spawn[0])
        self.assertTrue(core.jump())
        self.assertLess(core.vy, 0)
        for _ in range(80):
            core.tick()

        self.assertTrue(core.on_ground)
        self.assertEqual(core.deaths, 0)

    def test_roll_boosts_forward_and_spends_hop_until_orb_recharge(self):
        core = RollyCore(seed=3)
        before = core.vx

        self.assertTrue(core.roll(direction=1))
        self.assertGreater(core.vx, before)
        self.assertFalse(core.can_hop)

        orb = next(iter(core.orbs))
        core.move_to_tile(*orb)
        core.tick()

        self.assertTrue(core.can_hop)
        self.assertNotIn(orb, core.orbs)

    def test_spike_respawns_at_checkpoint_and_counts_death(self):
        core = RollyCore(seed=4)
        spike = next(iter(core.spikes))

        core.move_to_tile(*spike)
        core.tick()

        self.assertEqual(core.player_pos(), core.spawn)
        self.assertEqual(core.deaths, 1)

    def test_collecting_friend_opens_exit_and_clears_level(self):
        core = RollyCore(seed=5)
        friend = next(iter(core.friends))

        core.move_to_tile(*friend)
        core.tick()

        self.assertEqual(core.friends_rescued, 1)
        self.assertTrue(core.exit_open)

        core.move_to_tile(*core.exit)
        core.tick()
        self.assertTrue(core.level_clear)


if __name__ == "__main__":
    unittest.main()

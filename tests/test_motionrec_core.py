from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "motionrec"
sys.path.insert(0, str(GAME_DIR))

from motionrec_core import MotionRecCore  # noqa: E402


class MotionRecCoreTest(unittest.TestCase):
    def test_player_runs_jumps_and_lands_on_floor(self):
        core = MotionRecCore(seed=1)
        start_x = core.player.x

        for _ in range(12):
            core.tick(right=True)
        core.tick(jump=True)
        airborne_y = core.player.y
        for _ in range(50):
            core.tick(right=True)

        self.assertGreater(core.player.x, start_x + 24)
        self.assertLess(airborne_y, core.floor_y)
        self.assertTrue(core.player.on_ground)

    def test_recording_stores_motion_path(self):
        core = MotionRecCore(seed=2)

        core.start_recording()
        for _ in range(8):
            core.tick(right=True)
        core.tick(jump=True)
        for _ in range(5):
            core.tick(right=True)
        core.stop_recording()

        self.assertGreater(len(core.recorded_path), 8)
        self.assertEqual(core.mode, "play")
        self.assertGreater(core.recorded_path[-1][0], core.recorded_path[0][0])

    def test_playback_reuses_recorded_motion_from_current_position(self):
        core = MotionRecCore(seed=3)
        core.recorded_path = [(0, 0), (6, 0), (12, -8), (18, 0)]
        core.player.x = 40
        core.player.y = core.floor_y

        core.start_playback(reverse=False)
        for _ in range(4):
            core.tick()

        self.assertEqual(core.mode, "play")
        self.assertAlmostEqual(core.player.x, 58)
        self.assertAlmostEqual(core.player.y, core.floor_y)

    def test_reverse_playback_walks_recorded_motion_backwards(self):
        core = MotionRecCore(seed=4)
        core.recorded_path = [(0, 0), (6, 0), (12, -8), (18, 0)]
        core.player.x = 100
        core.player.y = core.floor_y

        core.start_playback(reverse=True)
        for _ in range(4):
            core.tick()

        self.assertAlmostEqual(core.player.x, 82)
        self.assertAlmostEqual(core.player.y, core.floor_y)

    def test_recorded_clone_can_hold_switch_and_open_goal(self):
        core = MotionRecCore(seed=5)
        core.recorded_path = [(0, 0), (16, 0), (32, 0), (48, 0)]
        core.switch_x = core.player.x + 48
        core.goal_x = core.player.x + 80
        core.start_playback(reverse=False)

        for _ in range(4):
            core.tick()

        self.assertTrue(core.switch_active)
        self.assertFalse(core.goal_locked)

        core.player.x = core.goal_x
        core.tick()

        self.assertTrue(core.cleared)

    def test_reset_clears_bad_recording_without_changing_level_layout(self):
        core = MotionRecCore(seed=6)
        core.start_recording()
        core.tick(left=True)
        core.stop_recording()
        core.player.x = -20

        core.restart_level()

        self.assertEqual(core.player.x, core.spawn_x)
        self.assertEqual(core.recorded_path, [])
        self.assertFalse(core.cleared)


if __name__ == "__main__":
    unittest.main()

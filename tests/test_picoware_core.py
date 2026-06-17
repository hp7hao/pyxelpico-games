from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "picoware"
sys.path.insert(0, str(GAME_DIR))

from picoware_core import MicroKind, PicowareCore, RoundState  # noqa: E402


class PicowareCoreTest(unittest.TestCase):
    def test_new_rush_starts_first_microgame_with_lives_and_timer(self):
        core = PicowareCore(seed=1)
        core.start()

        self.assertEqual(core.state, RoundState.PLAYING)
        self.assertEqual(core.lives, 4)
        self.assertEqual(core.score, 0)
        self.assertGreater(core.time_left, 0)
        self.assertIsNotNone(core.current)

    def test_tap_target_succeeds_when_pressing_required_direction(self):
        core = PicowareCore(seed=2)
        core.force_microgame(MicroKind.TAP_TARGET, target="left")

        core.input_press("right")
        self.assertEqual(core.state, RoundState.PLAYING)
        core.input_press("left")

        self.assertEqual(core.state, RoundState.RESULT)
        self.assertTrue(core.success)
        self.assertEqual(core.score, 1)

    def test_dodge_hazard_fails_when_player_moves_into_hazard_lane(self):
        core = PicowareCore(seed=3)
        core.force_microgame(MicroKind.DODGE, target="up")

        core.input_press("up")

        self.assertEqual(core.state, RoundState.RESULT)
        self.assertFalse(core.success)
        self.assertEqual(core.lives, 3)

    def test_countdown_timeout_marks_unsolved_microgame_failed(self):
        core = PicowareCore(seed=4)
        core.force_microgame(MicroKind.TAP_TARGET, target="a", duration=3)

        for _ in range(3):
            core.tick()

        self.assertEqual(core.state, RoundState.RESULT)
        self.assertFalse(core.success)
        self.assertEqual(core.lives, 3)

    def test_result_delay_advances_to_next_microgame_or_game_over(self):
        core = PicowareCore(seed=5)
        core.force_microgame(MicroKind.TAP_TARGET, target="a")
        core.input_press("a")
        for _ in range(core.result_delay):
            core.tick()

        self.assertEqual(core.state, RoundState.PLAYING)
        self.assertEqual(core.round_index, 2)

        core.lives = 1
        core.force_microgame(MicroKind.TAP_TARGET, target="b", duration=1)
        core.tick()
        for _ in range(core.result_delay):
            core.tick()

        self.assertEqual(core.state, RoundState.GAME_OVER)


if __name__ == "__main__":
    unittest.main()

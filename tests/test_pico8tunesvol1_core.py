from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "pico8tunesvol1"
sys.path.insert(0, str(GAME_DIR))

from pico8tunesvol1_core import Pico8TunesVol1Core  # noqa: E402


class Pico8TunesVol1CoreTest(unittest.TestCase):
    def test_album_starts_with_twelve_track_setlist(self):
        core = Pico8TunesVol1Core()

        self.assertEqual(len(core.tracks), 12)
        self.assertEqual(core.current_track.title, "Pastoral")
        self.assertEqual(core.status, "playing")

    def test_next_previous_and_direct_selection_wrap(self):
        core = Pico8TunesVol1Core()

        core.next_track()
        self.assertEqual(core.current_index, 1)
        core.previous_track()
        self.assertEqual(core.current_index, 0)
        core.previous_track()
        self.assertEqual(core.current_index, 11)
        core.select_track(4)
        self.assertEqual(core.current_index, 4)

    def test_pause_resume_and_auto_advance(self):
        core = Pico8TunesVol1Core()

        core.toggle_pause()
        core.tick(600)
        self.assertEqual(core.elapsed_beats, 0)
        self.assertEqual(core.status, "paused")

        core.toggle_pause()
        core.tick(core.current_track.length_beats)
        self.assertEqual(core.current_index, 1)
        self.assertEqual(core.elapsed_beats, 0)

    def test_visualizer_points_are_deterministic_per_track_and_beat(self):
        core = Pico8TunesVol1Core()
        points_a = core.visualizer_points(beat=8, count=6)
        points_b = core.visualizer_points(beat=8, count=6)

        self.assertEqual(points_a, points_b)
        self.assertEqual(len(points_a), 6)
        self.assertTrue(all(0 <= x <= 239 and 0 <= y <= 239 for x, y, _c in points_a))


if __name__ == "__main__":
    unittest.main()

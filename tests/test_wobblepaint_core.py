from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "wobblepaint"
sys.path.insert(0, str(GAME_DIR))

from wobblepaint_core import WobblepaintCore  # noqa: E402


class WobblepaintCoreTest(unittest.TestCase):
    def test_cursor_moves_and_paint_places_brush_dabs(self):
        core = WobblepaintCore(seed=1)
        core.move_cursor(3, -2)
        self.assertEqual(core.cursor, (67, 62))

        core.brush_size = 2
        core.color = 10
        core.paint()

        self.assertGreater(len(core.strokes), 1)
        self.assertTrue(all(stroke.color == 10 for stroke in core.strokes))

    def test_undo_restores_previous_stroke_group(self):
        core = WobblepaintCore(seed=2)
        core.paint()
        first_count = len(core.strokes)
        core.move_cursor(5, 0)
        core.paint()

        self.assertGreater(len(core.strokes), first_count)
        self.assertTrue(core.undo())
        self.assertEqual(len(core.strokes), first_count)

    def test_adjust_brush_and_cycle_color(self):
        core = WobblepaintCore(seed=3)

        core.adjust_brush(2)
        core.cycle_color(1)

        self.assertEqual(core.brush_size, 3)
        self.assertEqual(core.color, 11)

    def test_wobble_points_animate_without_changing_saved_strokes(self):
        core = WobblepaintCore(seed=4)
        core.paint()
        before = core.animated_points(frame=0)
        after = core.animated_points(frame=12)

        self.assertEqual(len(before), len(after))
        self.assertNotEqual(before[0][:2], after[0][:2])
        self.assertEqual(core.strokes[0].x, 64)


if __name__ == "__main__":
    unittest.main()

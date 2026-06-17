from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "maichanssweetbuns"
sys.path.insert(0, str(GAME_DIR))

from maichanssweetbuns_core import BakeryCore, BunKind, OrderState  # noqa: E402


class BakeryCoreTest(unittest.TestCase):
    def test_new_shift_starts_with_order_and_empty_tray(self):
        core = BakeryCore(seed=1)

        self.assertEqual(core.state, OrderState.PLAYING)
        self.assertEqual(core.day, 1)
        self.assertEqual(core.score, 0)
        self.assertEqual(core.tray, [])
        self.assertGreater(len(core.order), 0)

    def test_selecting_ingredient_adds_to_tray_in_order(self):
        core = BakeryCore(seed=2)
        core.set_order([BunKind.PLAIN, BunKind.JAM])

        core.choose(BunKind.PLAIN)
        core.choose(BunKind.JAM)

        self.assertEqual(core.tray, [BunKind.PLAIN, BunKind.JAM])
        self.assertEqual(core.state, OrderState.READY)

    def test_wrong_bun_costs_patience_and_clears_tray(self):
        core = BakeryCore(seed=3)
        core.set_order([BunKind.CHOCOLATE])

        core.choose(BunKind.JAM)

        self.assertEqual(core.patience, core.max_patience - 1)
        self.assertEqual(core.tray, [])
        self.assertEqual(core.state, OrderState.PLAYING)

    def test_serving_ready_order_scores_and_advances_day(self):
        core = BakeryCore(seed=4)
        core.set_order([BunKind.PLAIN])

        core.choose(BunKind.PLAIN)
        core.serve()

        self.assertEqual(core.score, 10)
        self.assertEqual(core.day, 2)
        self.assertEqual(core.state, OrderState.PLAYING)

    def test_timer_can_end_shift_when_patience_runs_out(self):
        core = BakeryCore(seed=5)
        core.patience = 1
        core.timer = 1

        core.tick()

        self.assertEqual(core.state, OrderState.GAME_OVER)


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "highstakes"
sys.path.insert(0, str(GAME_DIR))

from highstakes_core import HighStakesCore, Result  # noqa: E402


class HighStakesCoreTest(unittest.TestCase):
    def test_deal_has_nine_unique_cards_one_vampire_and_one_visible_safe_card(self):
        core = HighStakesCore(seed=3)

        values = [card.value for card in core.cards]
        self.assertEqual(sorted(values), [2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(sum(card.is_vampire for card in core.cards), 1)
        visible = [card for card in core.cards if not card.hidden]
        self.assertEqual(len(visible), 1)
        self.assertFalse(visible[0].is_vampire)

    def test_flip_safe_card_scores_and_vampire_flip_loses_round(self):
        core = HighStakesCore(seed=4)
        safe = next(card for card in core.cards if card.hidden and not card.is_vampire)
        vampire = next(card for card in core.cards if card.is_vampire)

        self.assertEqual(core.flip(safe.pos), Result.CONTINUE)
        self.assertFalse(safe.hidden)
        self.assertGreater(core.stakes, 0)

        self.assertEqual(core.flip(vampire.pos), Result.LOST)
        self.assertEqual(core.result, Result.LOST)

    def test_hint_token_marks_cards_at_or_above_threshold(self):
        core = HighStakesCore(seed=5)
        hidden_high = [card.pos for card in core.cards if card.hidden and card.value >= 7]

        marked = core.place_hint_token(7)

        self.assertEqual(sorted(marked), sorted(hidden_high))
        self.assertEqual(core.hints_left, 1)

    def test_stabbing_vampire_wins_and_stabbing_safe_card_loses(self):
        core = HighStakesCore(seed=6)
        vampire = next(card for card in core.cards if card.is_vampire)

        self.assertEqual(core.stab(vampire.pos), Result.WON)
        self.assertGreater(core.payout(), 0)

        core = HighStakesCore(seed=6)
        safe = next(card for card in core.cards if card.hidden and not card.is_vampire)
        self.assertEqual(core.stab(safe.pos), Result.LOST)

    def test_pass_scores_only_when_vampire_remains_hidden(self):
        core = HighStakesCore(seed=7)
        self.assertEqual(core.pass_round(), Result.WON)
        self.assertGreater(core.payout(), 0)

        core = HighStakesCore(seed=7)
        vampire = next(card for card in core.cards if card.is_vampire)
        vampire.hidden = False
        self.assertEqual(core.pass_round(), Result.LOST)


if __name__ == "__main__":
    unittest.main()

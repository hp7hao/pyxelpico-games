from pathlib import Path
import sys
import unittest


GAME_DIR = Path(__file__).resolve().parents[1] / "games" / "freezingknights"
sys.path.insert(0, str(GAME_DIR))

from freezingknights_core import FreezingKnightsCore  # noqa: E402


class FreezingKnightsCoreTest(unittest.TestCase):
    def test_knights_advance_from_safe_zone_into_first_encounter(self):
        core = FreezingKnightsCore(seed=1)

        core.choose_path(0)

        self.assertEqual(core.mode, "battle")
        self.assertEqual(core.current_node.name, "pine pass")
        self.assertEqual(len(core.enemies), 2)
        self.assertEqual(core.message, "ambush at pine pass")

    def test_attacks_spend_stamina_and_defeat_enemy_for_gold(self):
        core = FreezingKnightsCore(seed=2)
        core.choose_path(0)
        core.enemies[0].hp = 4

        core.knight_action(0, "strike", target_index=0)


        self.assertEqual(core.party[0].stamina, 1)
        self.assertEqual(core.gold, 4)
        self.assertEqual(core.enemies[0].hp, 0)
        self.assertIn("wins 4g", core.message)

    def test_timed_defense_reduces_enemy_damage(self):
        core = FreezingKnightsCore(seed=3)
        core.choose_path(0)
        core.party[0].hp = 18

        core.enemy_turn(defense_timing=0.93)
        blocked_hp = core.party[0].hp
        blocked_quality = core.guard_quality
        core.party[0].hp = 18
        core.enemy_turn(defense_timing=0.10)
        missed_hp = core.party[0].hp

        self.assertGreater(blocked_hp, missed_hp)
        self.assertEqual(blocked_quality, "great")
        self.assertEqual(core.guard_quality, "miss")

    def test_rest_node_restores_party_and_records_safe_state(self):
        core = FreezingKnightsCore(seed=4)
        core.choose_path(1)
        core.party[0].hp = 5
        core.party[1].hp = 3
        core.potions = 0

        core.rest()

        self.assertEqual(core.mode, "map")
        self.assertEqual([k.hp for k in core.party], [k.max_hp for k in core.party])
        self.assertEqual(core.potions, 3)
        self.assertEqual(core.last_safe_node, core.current_node_index)

    def test_upgrade_at_rest_spends_gold_and_improves_knight(self):
        core = FreezingKnightsCore(seed=5)
        core.choose_path(1)
        core.gold = 8

        core.buy_upgrade(1, "attack")

        self.assertEqual(core.gold, 2)
        self.assertEqual(core.party[1].attack, 5)
        self.assertEqual(core.message, "ember attack up")

    def test_party_wipe_returns_to_last_safe_zone_with_relief_potions(self):
        core = FreezingKnightsCore(seed=6)
        core.choose_path(1)
        core.rest()
        core.choose_path(0)
        core.party[0].hp = 1
        core.party[1].hp = 1
        for enemy in core.enemies:
            enemy.attack = 9

        core.enemy_turn(defense_timing=0.0)

        self.assertEqual(core.mode, "map")
        self.assertEqual(core.current_node_index, core.last_safe_node)
        self.assertEqual(core.potions, 5)
        self.assertTrue(all(knight.hp > 0 for knight in core.party))


if __name__ == "__main__":
    unittest.main()

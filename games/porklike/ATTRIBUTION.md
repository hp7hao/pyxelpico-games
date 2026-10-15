# Porklike

**Original author**: Krystman
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=37045
**Original cart**: https://www.lexaloffle.com/bbs/cposts/po/porklike-2.p8.png

PICO-8 metadata source: FCDB PICO-8 bbs metadata
(id/pid `73825`, tid `37045`).

## Changes for PyxelPico

- Reimplemented a first playable turn-based dungeon crawler in Python for
  Pyxel/PyxelPico.
- Preserved the handheld-compatible premise: grid movement, bump-to-attack
  enemies, food pickups, health, score, floor exits, turn-based enemy actions,
  win, and loss states.
- Added `porklike_core.py` as a host-testable gameplay core for dungeon
  generation, wall blocking, enemy combat, item collection, enemy turns, and
  level advancement.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by a compact roguelike
  dungeon.

## Notes

- FCDB's numeric cart URL currently returns 404 for this entry; the live BBS
  slug cart URL downloads, but the current local extractor returns empty Lua
  from its old `:c:` compressed code region. Exact API/Lua parity is therefore
  blocked until extractor parity with pico8ide is repaired.
- This is a first playable adaptation, not a full translation of the original
  map generation, enemy roster, item rules, sprite sheet, animation, or
  soundtrack.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

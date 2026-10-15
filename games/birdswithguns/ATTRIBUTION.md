# Birds With Guns

**Original authors**: Yolwoocle and Gouspourd
**Extra credits**: notgoyome; music by Simon T.
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=45334
**Original cart**: https://www.lexaloffle.com/bbs/cposts/bi/birdswithguns-5.p8.png

PICO-8 metadata source: FCDB PICO-8 bbs metadata
(id/pid `100000`, tid `45334`).

## Changes for PyxelPico

- Reimplemented a first playable train-wagon roguelike shooter loop in Python
  for Pyxel/PyxelPico.
- Preserved the handheld-compatible core: D-pad movement, firing, weapon swap,
  enemy clearing, wagon progression, boss wagon, health, ammo, score, win, and
  death states.
- Added `birdswithguns_core.py` as a host-testable gameplay core for movement,
  shooting, weapon switching, wagon progression, enemy touch damage, and boss
  victory.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the train/bird/gun setup.

## Notes

- Cart Lua was extracted from the downloadable BBS slug cart using
  `scripts/pico8_cart_extract.py` for API and gameplay audit.
- This is a first playable adaptation, not a full translation of the original
  procedural train map, sprite sheet, particle system, drops, bird roster,
  weapon list, boss script, or soundtrack.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

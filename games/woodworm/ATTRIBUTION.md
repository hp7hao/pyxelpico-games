# Woodworm

**Original author**: spratt
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=142717
**Original cart**: https://www.lexaloffle.com/bbs/cposts/wo/woodworm-0.p8.png

PICO-8 metadata source: `projects/fcdb/platforms/pico8/metadata/sources/bbs.json`
(id/pid `149969`, tid `142717`).

## Changes for PyxelPico

- Reimplemented a first playable grid-puzzle adaptation in Python for
  Pyxel/PyxelPico.
- Preserved the BBS/comment-described core: a Snakebird-like worm moves through
  clever puzzles, eats wood, avoids reversing into itself, uses undo heavily,
  lets unsupported blocks and the worm fall, and clears by reaching the goal.
- Added `woodworm_core.py` as a host-testable gameplay core for worm movement,
  reverse blocking, wood eating, undo, gravity, and clear states.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the wood/cake/worm
  premise.

## Notes

- The live BBS slug cart extracts usable Lua and API surface with
  `scripts/pico8_cart_extract.py`; the extracted API includes `_init`,
  `_update`, `_draw`, input, map/camera/clip rendering, SFX/music, cartdata
  persistence, and math calls.
- The original has authored puzzle levels, level select, save progress, custom
  font/UI, falling animation polish, jar/cabinet presentation, and a cake ending.
  This is a compact first playable adaptation, not a full level-set/source
  translation.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

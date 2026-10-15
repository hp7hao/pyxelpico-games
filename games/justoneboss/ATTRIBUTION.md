# Just One Boss

**Original author**: bridgs
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=49234
**Original cart**: https://www.lexaloffle.com/bbs/cposts/49234.p8.png
**Local source trail**: justonebossmod.p8

PICO-8 metadata source: FCDB PICO-8 bbs metadata
(id/pid `49234`, tid `49234`).

## Changes for PyxelPico

- Reimplemented the arena-boss loop in Python for Pyxel/PyxelPico.
- Preserved the main premise: move on a small grid, collect magic tiles to hurt
  the boss, avoid damaging tiles, progress through escalating boss phases, and
  retry from end states with handheld controls.
- Added `justoneboss_core.py` as a host-testable gameplay core for movement,
  tile collision, boss damage, phase progression, and win/loss rules.
- Added handheld-friendly controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the arena/boss setup.

## Notes

- This is a first playable PyxelPico adaptation, not a line-by-line translation
  of the full original PICO-8 phase script, animation system, sprite sheet, or
  soundtrack.
- The local Picovibe source trail includes the original author note pointing to
  https://github.com/bridgs/just-one-boss for hacking on the cart.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

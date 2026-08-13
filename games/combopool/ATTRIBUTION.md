# Combo Pool

**Original author**: NuSan
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=3467
**Original cart**: https://www.lexaloffle.com/bbs/cposts/co/combopool-0.p8.png

PICO-8 metadata source: `projects/fcdb/platforms/pico8/metadata/sources/bbs.json`
(id/pid `21515`, tid `3467`).

## Changes for PyxelPico

- Reimplemented a first playable colored-marble merge pool loop in Python for
  Pyxel/PyxelPico.
- Preserved the BBS-described core: aim and shoot marbles, collide balls,
  merge same colors into higher colors, score from merges/rebounds/combos,
  pressure the life bar when too many or too-dark balls remain, and clear by
  reaching the final merge.
- Added `combopool_core.py` as a host-testable gameplay core for aim rotation,
  shooting, wall rebounds, same-color merging, scoring, combo tracking, life
  pressure, win, and loss states.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the marble table.

## Notes

- The live BBS slug cart downloads, but current local extraction returns only a
  shallow 1.6k-char output with no useful API surface. The BBS thread provides
  detailed gameplay notes, so this first pass is based on those mechanics.
- This is a first playable adaptation, not a full translation of the original
  physics tuning, difficulty modes, mouse/touch aiming, sprite effects, color
  progression, sudden-death behavior, or soundtrack.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

# High Stakes

**Original author**: Krystian Majewski / Lazy Devs
**Music**: Gruber Music
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=40099
**Original cart**: https://www.lexaloffle.com/bbs/cposts/hi/highstakes-2.p8.png

PICO-8 metadata source: `projects/fcdb/platforms/pico8/metadata/sources/bbs.json`
(id/pid `83548`, tid `40099`).

## Changes for PyxelPico

- Reimplemented a first playable vampire card-deduction loop in Python for
  Pyxel/PyxelPico.
- Preserved the central 3x3 hidden-card premise: one vampire card, one visible
  safe card, flip safe cards for stakes, use hint tokens, stab suspected
  vampires, or pass while the vampire remains hidden.
- Added `highstakes_core.py` as a host-testable gameplay core for deal,
  flip, hint, stab, pass, result, and payout rules.
- Added handheld controls using `lib/input_helper.py` (D-pad cursor, A action,
  B/Select tool cycle, Start pass).
- Added an original PyxelPico cover image inspired by the vampire-card table.

## Notes

- Cart Lua was extracted from the downloadable BBS slug cart using
  `scripts/pico8_cart_extract.py` for API and gameplay audit.
- This first port does not yet reproduce the full original blood economy,
  unlock ladder, chained score mode, card/chip animations, custom sprites, or
  soundtrack.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

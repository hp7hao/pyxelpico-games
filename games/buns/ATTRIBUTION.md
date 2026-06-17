# Buns: Bunny Survivor

**Original author**: unikotoast
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=48032
**Original cart**: https://www.lexaloffle.com/bbs/cposts/bu/bunnysurvivor-9.p8.png

PICO-8 metadata source: `projects/fcdb/sources/pico8/bbs_release.json`
(id/pid `112740`, tid `48032`).

## Changes for PyxelPico

- Reimplemented a first playable survivor loop in Python for Pyxel/PyxelPico.
- Preserved the handheld-compatible core: D-pad movement, automatic firing,
  enemy waves, gem collection, level-up upgrades, timer pressure, boss spawn,
  health, win, and loss states.
- Added `buns_core.py` as a host-testable gameplay core for movement bounds,
  enemy spawn/chase, auto-fire, gem XP, upgrades, damage iframes, boss timing,
  and victory.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the bunny-survivor setup.

## Notes

- Cart Lua was extracted from the downloadable BBS slug cart using
  `scripts/pico8_cart_extract.py` for API and gameplay audit.
- This is a first playable adaptation, not a full translation of the original
  sprite sheet, enemy/weapon roster, upgrade table, stage pacing, particles, or
  soundtrack.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

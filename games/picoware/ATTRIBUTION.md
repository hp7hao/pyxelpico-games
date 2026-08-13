# PICOWARE

**Original authors**: The PICOWARE team, coordinated by szczm_
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=34751
**Original cart**: https://www.lexaloffle.com/bbs/cposts/pi/picoware-20.p8.png

PICO-8 metadata source: `projects/fcdb/platforms/pico8/metadata/sources/bbs.json`
(id/pid `65884`, tid `34751`).

## Changes for PyxelPico

- Reimplemented a first playable microgame-rush loop in Python for
  Pyxel/PyxelPico.
- Preserved the handheld-compatible structure: short timed prompts, D-pad/A/B
  inputs, pass/fail results, lives, score, increasing speed pressure, game over,
  and retry.
- Added `picoware_core.py` as a host-testable gameplay core for round starts,
  target-button microgames, dodge prompts, mash prompts, countdown failure,
  result delay, scoring, lives, and game-over transition.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the microgame grid.

## Notes

- The BBS thread describes the original as a 24-hour collaboration with 50+
  developers and 68 microgames. This first PyxelPico adaptation is a compact
  microgame-rush subset, not a full recreation of all subcart content.
- Cart Lua was extracted from the downloadable BBS slug cart using
  `scripts/pico8_cart_extract.py` for API and structure audit.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

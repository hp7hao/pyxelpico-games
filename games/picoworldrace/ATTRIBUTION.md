# Pico World Race 1.2

**Original author**: PAK9
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=46495
**Original cart**: https://www.lexaloffle.com/bbs/cposts/pp/ppwr-5.p8.png
**Upstream source trail**: https://github.com/PAK9/PicoWorldRace

PICO-8 metadata source: FCDB PICO-8 bbs metadata
(id/pid `106518`, tid `46495`).

## Changes for PyxelPico

- Reimplemented a first playable racing loop in Python for Pyxel/PyxelPico.
- Preserved the handheld-compatible core from the extracted Lua and BBS thread:
  gas, steering, drift, lap progress, opponents, token collection, standing,
  finish, score, and retry.
- Added `picoworldrace_core.py` as a host-testable gameplay core for
  acceleration, steering, drift speed tradeoffs, off-track penalties, token
  crossing, laps, finish state, and opponent progress.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the world-race road.

## Notes

- Cart Lua was extracted from the downloadable BBS slug cart using
  `scripts/pico8_cart_extract.py` for API and structure audit.
- This is a first playable adaptation, not a full translation of the original
  8 themed races, 8 opponents, 20-token-per-race campaign, custom track
  generator, sprite art, physics tuning, profile saves, or soundtrack.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

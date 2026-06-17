# PICORACER-2048

**Original author**: impbox
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=2243
**Original cart**: https://www.lexaloffle.com/bbs/cposts/1/16305.p8.png

PICO-8 metadata source: `projects/fcdb/sources/pico8/bbs_release.json`
(id `12408`, thread tid `2243`; live cart id `16305` from the BBS thread).

## Changes for PyxelPico

- Reimplemented a first playable anti-gravity/top-down racer adaptation in
  Python for Pyxel/PyxelPico.
- Preserved the BBS-described core: 4 speed classes, 8 looping tracks reduced
  to one compact section chain, 3-lap racing, narrowing/curving track sections,
  boost pads, brake-assisted turning, wall-hit slowdown, and AI race pressure.
- Added `picoracer2048_core.py` as a host-testable gameplay core for
  acceleration, braking, boost pads, curve drift, steering, off-track wall hits,
  lap/finish timing, and AI progress.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the vector-racer premise.

## Notes

- FCDB's numeric cart URL is stale; the BBS thread exposes the working cart
  path `https://www.lexaloffle.com/bbs/cposts/1/16305.p8.png`.
- The live cart downloads, but local `scripts/pico8_cart_extract.py` returns
  empty Lua/API for this older cart; the Lexaloffle source snippet endpoint
  depends on browser-side cart tooling not available in the local extractor.
- This is a compact first playable adaptation based on BBS/cart evidence and
  thread notes, not a full source translation of the original 8 tracks, ghost
  data, AI racers, track editor/storage format, sprite/vector effects, music,
  or exact handling.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

# Marballs 2

**Original author**: lucatron
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=28414
**Original cart**: https://www.lexaloffle.com/bbs/cposts/ma/marballs_2-0.p8.png

PICO-8 metadata source: FCDB PICO-8 bbs metadata
(id/pid `34773`, tid `28414`; live cart id `marballs_2-0` from the BBS thread).

## Changes for PyxelPico

- Reimplemented a first playable rolling-ball platformer adaptation in Python
  for Pyxel/PyxelPico.
- Preserved the BBS-described core: rolling with D-pad, jump pads, verticality
  represented by ball height, orb collection, orb-gated exits, wall-bounce
  momentum, timer/medal pressure, restart, and optional 45-degree controls.
- Added `marballs2_core.py` as a host-testable gameplay core for rolling
  acceleration/friction, jump pads, orb collection, goal locking, wall bounce,
  medal timing, and rotated controls.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the marble/orb/jump-pad
  premise.

## Notes

- FCDB's numeric cart URL is stale; the BBS thread exposes the working cart
  path `https://www.lexaloffle.com/bbs/cposts/ma/marballs_2-0.p8.png`.
- The live cart extracts partial Lua with `scripts/pico8_cart_extract.py`,
  including the title data and authoritative level table (`simple`, `climb`,
  `plateaus`, `orbs`, `boost`, `trampoline`, etc.), but no useful API scan.
- This is a compact first playable adaptation, not a full source translation of
  the original official level pack, custom cart workflow, exact collision,
  level select, music, intro, save data, or ace-time routing.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

# X-Zero

**Original author**: paranoidcactus
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=36053
**Original cart**: https://www.lexaloffle.com/bbs/cposts/xz/xzero-3.p8.png

PICO-8 metadata source: FCDB PICO-8 bbs metadata
(id/pid `70362`, tid `36053`).

## Changes for PyxelPico

- Reimplemented a first playable platform-shooter loop in Python for
  Pyxel/PyxelPico.
- Preserved the handheld-compatible premise observed from the BBS thread:
  side-view platforming, jump/shoot controls, directional aiming, enemies,
  pickups, zones, health, win, and loss states.
- Added `xzero_core.py` as a host-testable gameplay core for movement, jumping,
  shooting, enemy hits, contact damage, pickups, zone exits, and final clear.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the neon platform-shooter
  setup.

## Notes

- The live BBS slug cart downloads, but the current local extractor returns
  empty Lua, so exact API/Lua parity is blocked until extraction is repaired
  for this cart.
- This is a first playable adaptation, not a full translation of the original
  prefab map randomization, level layouts, sprites, animation, aiming model, or
  soundtrack.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

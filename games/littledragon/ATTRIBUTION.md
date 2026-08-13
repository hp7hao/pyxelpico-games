# Little Dragon Adventure

**Original author**: Mush
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=31469
**Original cart**: https://www.lexaloffle.com/bbs/cposts/5/53895.p8.png

PICO-8 metadata source: `projects/fcdb/platforms/pico8/metadata/sources/bbs.json`
(id/pid `53896`, tid `31469`; live cart id `53895` from the BBS thread).

## Changes for PyxelPico

- Reimplemented a first playable dragon platform-adventure adaptation in Python
  for Pyxel/PyxelPico.
- Preserved the BBS/comment-visible core: cute dragon movement, jumping and
  double jumping, fireballs, enemies, hazards, checkpoints, rescued dragon eggs,
  boss gate, and final rescue clear.
- Added `littledragon_core.py` as a host-testable gameplay core for movement,
  double jump, fireball hits, egg collection, checkpoint respawn, hazards,
  boss gating, and clear state.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the dragon/egg rescue
  premise.

## Notes

- The live cart downloads, but local extraction currently returns empty Lua/API
  with `scripts/pico8_cart_extract.py`, so this pass is a BBS-evidence/manual
  Pyxel/Python adaptation rather than a source translation.
- This is a compact first playable adaptation, not a full source translation of
  the original metroidvania map, bosses, exact enemy behavior, challenge mode,
  checkpoints, music, sprite work, or ending surprise.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

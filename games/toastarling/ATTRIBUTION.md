# To a Starling

**Original authors**: Peteksi and Gruber
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=45958
**Original cart**: https://www.lexaloffle.com/bbs/cposts/to/to_a_starling-0.p8.png

PICO-8 metadata source: `projects/fcdb/platforms/pico8/metadata/sources/bbs.json`
(id/pid `104057`, tid `45958`).

## Changes for PyxelPico

- Reimplemented a first playable platform-adventure adaptation in Python for
  Pyxel/PyxelPico.
- Preserved the extracted cart's core platforming shape: acceleration,
  friction, coyote/buffered jumps, glide/fast-fall feel, checkpoints, hazards,
  berries, keys, locked doors, switches, bridges, and room goals.
- Added `toastarling_core.py` as a host-testable gameplay core for movement,
  jump/coyote timing, glide, collectibles, switch/door puzzle state,
  checkpoint respawn, and clear states.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the bird/platforming
  premise.

## Notes

- The live BBS slug cart extracts usable Lua and API surface with
  `scripts/pico8_cart_extract.py`; the extracted API includes `_init`,
  `_update60`, `_draw`, input, map mutation, sprite/tile rendering, SFX/music,
  cartdata persistence, and math calls.
- The original is a broader room-based puzzle platform adventure with custom
  maps, camera transitions, teleport/portal logic, merchants, save data,
  animation polish, music, and authored level progression. This is a compact
  first playable adaptation, not a full map or source translation.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

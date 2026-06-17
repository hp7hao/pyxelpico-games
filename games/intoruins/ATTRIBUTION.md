# Into Ruins

**Original author**: Eric Billingsley (`ericb`)
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=49928
**Original cart**: https://www.lexaloffle.com/bbs/cposts/in/intoruins-7.p8.png
**Upstream source trail**: https://github.com/Woflox/intoruins

PICO-8 metadata source: `projects/fcdb/sources/pico8/bbs_release.json`
(id/pid `119614`, tid `49928`).

## Changes for PyxelPico

- Reimplemented a first playable turn-based roguelike adaptation in Python for
  Pyxel/PyxelPico.
- Preserved the published core goal and theme: descend through ruins, manage
  HP/light/status pressure, fight or avoid creatures, collect potions/torches
  and fire/frost orbs, and retrieve the Wings of Yendor on depth 16.
- Added `intoruins_core.py` as a host-testable gameplay core for movement,
  bump combat, visibility/exploration, burn/freeze status turns, ranged enemy
  attacks, item effects, descent, win, and loss states.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the ruins/Wings premise.

## Notes

- The live BBS slug cart extracts usable Lua and API surface with
  `scripts/pico8_cart_extract.py`; the extracted API includes `_update`,
  `_draw`, sprite/rect/print/palette/camera/music/data/math calls.
- The original is a dense Brogue-inspired roguelike with hex/isometric map
  rendering, many weapons, staffs, orbs, creatures, terrain interactions, fire,
  light, freezing, pits, bridge/object physics, music, and extensive emergent
  rules. This is a compact first playable adaptation, not a full line-by-line
  translation.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

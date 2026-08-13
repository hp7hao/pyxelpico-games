# UFO Swamp Odyssey

**Original author**: paranoidcactus
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=38153
**Original cart**: https://www.lexaloffle.com/bbs/cposts/uf/ufo-0.p8.png

PICO-8 metadata source: `projects/fcdb/platforms/pico8/metadata/sources/bbs.json`
(id/pid `77254`, tid `38153`).

## Changes for PyxelPico

- Reimplemented a first playable platform-adventure adaptation in Python for
  Pyxel/PyxelPico.
- Preserved the BBS-described core premise: a robot UFO pilot stranded in a
  swamp junkyard, collecting zapper fuel from friendly aliens, using EMP,
  portal, and grapple zappers, stunning eyebots, and disabling the EMP cannon.
- Added `ufoswamp_core.py` as a host-testable gameplay core for movement,
  water buoyancy, pickup progression, enemy stun, portal teleport, grapple
  pull, and final cannon disable rules.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the UFO/swamp/zapper
  premise.

## Notes

- FCDB's numeric cart URL is stale; the live BBS thread exposes the working
  cart path `https://www.lexaloffle.com/bbs/cposts/uf/ufo-0.p8.png`.
- The live BBS slug cart extracts usable Lua and API surface with
  `scripts/pico8_cart_extract.py`; the original uses `_update60`, map/sprite
  rendering, custom palette, SFX/music, portals, grapples, enemies, and story
  scripting.
- This is a compact first playable adaptation, not a full source translation of
  the original authored map, animation, dialogue pacing, palette work, music,
  and transition polish.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

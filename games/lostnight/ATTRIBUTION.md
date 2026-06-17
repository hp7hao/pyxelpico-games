# The Lost Night

**Original author**: arlefreak
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=41791
**Original cart**: https://www.lexaloffle.com/bbs/cposts/th/the_lost_night-6.p8.png

PICO-8 metadata source: `projects/fcdb/sources/pico8/bbs_release.json`
(id/pid `88259`, tid `41791`; live cart id `the_lost_night-6` from the BBS
thread).

## Changes for PyxelPico

- Reimplemented a first playable night-themed RPG/shooter adaptation in Python
  for Pyxel/PyxelPico.
- Preserved the extracted/BBS-visible core: room-to-room overworld movement,
  enemy encounters, a bullet-dodging battle box, player shots, HP/tea healing,
  candy rewards, shop upgrades, and a final dawn clear condition.
- Added `lostnight_core.py` as a host-testable gameplay core for room
  traversal, encounter start, bullet collision, enemy defeat, tea healing,
  candy upgrades, room clears, and dawn unlock.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the night/shooter
  premise.

## Notes

- FCDB tags include `earthbound`, and BBS comments mention Mother/Undertale
  vibes. This port avoids third-party branded characters, names, and assets and
  uses generic night, room, candy, and bullet-dodging presentation.
- The live cart extracts usable Lua/API with `scripts/pico8_cart_extract.py`,
  including `_init`, `_update60`, `_draw`, `btn`, `btnp`, map/sprite calls,
  persistence, music, HP, shop, and battle-related symbols.
- This is a compact first playable adaptation, not a full source translation of
  the original maps, art, enemy patterns, dialogue, music, persistence, or
  upgrade/menu presentation.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

# Santaban

**Original author**: skutter-de  
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)  
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=153450  
**Original cart**: https://www.lexaloffle.com/bbs/cposts/sa/santaban-3.p8.png

PICO-8 metadata source: `projects/fcdb/sources/pico8/bbs_release.json` (id/pid `179484`, tid `153450`).

## Changes for PyxelPico

- Reimplemented gameplay loop in Python for Pyxel/PyxelPico (`games/santaban/santaban.py`).
- Preserved original level layouts, box/player starts, map collision/goal flags, and 25-level progression by extracting cart map/flag data (`games/santaban/santaban_data.py`).
- Implemented core Sokoban mechanics: push-only movement, undo history, restart, level select, and completion gating.
- Added handheld-friendly controls using `lib/input_helper.py` (D-pad move, A/Start confirm/next, B undo, Select menu).
- Added launcher cover derived from the cart label (`games/santaban/cover.png`).

## Notes

- Cart Lua and map sections were inspected from the downloadable cart PNG (`/bbs/cposts/sa/santaban-3.p8.png`) using a local decode path that supports PXA-compressed code.
- This port targets gameplay and level-fidelity first; original sprite art/audio are approximated with simplified Pyxel primitives/SFX.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must respect those terms.

# BAS

**Original author**: yokozuna / yokoboko
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=54986
**Original cart**: https://www.lexaloffle.com/bbs/cposts/ba/bas-9.p8.png
**GitHub source trail**: https://github.com/yokoboko/bas-pico-8

PICO-8 metadata source: `projects/fcdb/platforms/pico8/metadata/sources/bbs.json`
(id/pid `137287`, tid `54986`).

## Changes for PyxelPico

- Reimplemented a first playable endless wall-jump/highscore adaptation in
  Python for Pyxel/PyxelPico.
- Preserved the BBS-described core: jump left/right between walls, chain jumps
  without waiting to land, avoid circular saws, outrun the rising trap, score
  from successful jumps, and update a local high score.
- Added `bas_core.py` as a host-testable gameplay core for jump targeting,
  mid-air retargeting, saw collision prediction/collision, trap death, saw
  spawning, scoring, high score update, and restart.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the wall-jump/saw/trap
  premise.

## Notes

- The live BBS slug cart extracts usable Lua and API surface with
  `scripts/pico8_cart_extract.py`; the extracted API includes `_init`,
  `_update60`, `_draw`, input, sprite/shape rendering, SFX/music, cartdata
  persistence, and math calls.
- The original is a demake of the author's own classic iOS/mobile game, per the
  BBS description, and the local FCDB record provides CC BY-NC-SA 4.0 metadata.
- This is a compact first playable adaptation, not a full source translation of
  the original easing, sprite animation, music, transition, and visual polish.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

# Pico Checkmate

**Original author**: Krystman
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=31213
**Itch page**: https://krystman.itch.io/pico-checkmate
**Original cart**: https://www.lexaloffle.com/bbs/cposts/5/54038.p8.png

PICO-8 metadata source: `projects/fcdb/platforms/pico8/metadata/sources/bbs.json`
(id/pid `52226`, tid `31213`; live cart id `54038` from the BBS thread).

## Changes for PyxelPico

- Reimplemented a first playable classic chess adaptation in Python for
  Pyxel/PyxelPico.
- Preserved the BBS-described core: chess board, legal piece movement, check
  prevention, check/checkmate/stalemate states, castling, en passant, promotion,
  basic AI opponent, and handheld cursor controls.
- Added `picocheckmate_core.py` as a host-testable gameplay core for movement
  legality, check safety, castling, en passant, promotion, checkmate, and AI
  move selection.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the chess-board premise.

## Notes

- The live cart downloads, but local extraction currently returns empty Lua/API
  with `scripts/pico8_cart_extract.py`, so this pass is a rules-based manual
  Pyxel/Python adaptation rather than a source translation.
- Like the BBS note for the original, this first pass does not recognize draws
  by threefold repetition. It also omits the original's juicy animation polish,
  exact AI evaluation/search, two-human mode, soundtrack, and visual assets.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

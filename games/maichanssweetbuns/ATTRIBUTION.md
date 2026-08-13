# Mai-Chan's Sweet Buns

**Original author**: Krystman
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=31864
**Original cart**: https://www.lexaloffle.com/bbs/cposts/5/56576.p8.png

PICO-8 metadata source: `projects/fcdb/platforms/pico8/metadata/sources/bbs.json`
(FCDB id `56575`, live BBS pid/cart `56576`, tid `31864`).

## Changes for PyxelPico

- Reimplemented a first playable bakery order-matching loop in Python for
  Pyxel/PyxelPico.
- Preserved a handheld-compatible sweet-shop premise: read the customer order,
  choose matching buns, serve completed trays, manage patience, score orders,
  and retry after closing.
- Added `maichanssweetbuns_core.py` as a host-testable gameplay core for order
  generation, tray matching, wrong-bun penalties, serving, timer pressure,
  score, day progression, and game-over transition.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by a bakery counter.

## Notes

- FCDB points at `56575.p8.png`, but the live BBS thread exposes the playable
  cart as `/bbs/cposts/5/56576.p8.png`. That cart downloads, but the current
  local extractor returns empty Lua, so exact API/Lua parity is blocked until
  extraction is repaired for this older numeric cart path.
- This is a first playable adaptation, not a full translation of the original
  sprites, timing, recipe set, animation, or soundtrack.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

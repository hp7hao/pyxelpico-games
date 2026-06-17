# Pico Snail!: Dream Castle Attribution

This PyxelPico port adapts **Pico Snail!: Dream Castle** by GiantLNT / Floofinator.

- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=39897
- Live cart used for audit: https://www.lexaloffle.com/bbs/cposts/sn/snail-9.p8.png
- FCDB record: `id=82864`, `tid=39897`
- License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0

## Original Notes

The BBS thread presents Snail-Chan defending Dream Castle, credits the music and
character inspiration to Ujico / Snail's House, and explicitly allows modifying
and remixing the cart. The extracted cart source defines levels for the garden,
courtyard, entrance, halls, rooftops, moon, nightmare, and end scenes, with
stars, doors, switches, warps, books, hazards, and a cat encounter.

## PyxelPico Adaptation Notes

- This first playable pass keeps a compact platform-adventure loop: movement,
  jump, star-powered double jump, wand/star shots, centered thwack attacks,
  hazards, switches, doors, warps, a cat boss gate, and dream-clear ending.
- Procedural replacement art/audio and an original cover are used instead of
  copying the cart label, sprite sheet, map, story text, or music data.
- Exact authored rooms, save-data unlocks, full story-book text, original
  background renderers, all object variants, animation timing, and music are
  outside this first playable adaptation.

Original authors retain copyright. This adaptation is distributed under the
same CC BY-NC-SA 4.0 terms as the source cart.

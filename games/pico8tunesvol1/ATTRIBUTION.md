# Pico-8 Tunes Volume 1 Attribution

This PyxelPico port adapts **Pico-8 Tunes Volume 1** by Gruber and Krajzeg.

- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=29008
- Live cart used for audit: https://www.lexaloffle.com/bbs/cposts/3/38440.p8.png
- FCDB record: `id=38442`, `tid=29008`
- License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0

## Original Credits

- Music: Gruber (`@gruber_music` on the original BBS post)
- Code and animations: Krajzeg

The BBS post describes the cart as a 12-tune album intended for reuse in other
PICO-8 games. Krajzeg also confirmed in the thread that the cart code, sprites,
and other assets were available under the same Creative Commons umbrella.

## PyxelPico Adaptation Notes

- This is a controller-friendly album/player adaptation rather than a
  line-by-line audio-data conversion.
- The current local cart extractor downloads the live cart but returns no Lua or
  API surface for this older cart image, so this pass does not copy the original
  SFX/music data.
- Visuals, cover art, and Pyxel sound patterns are procedural replacements
  inspired by the album/demo-player premise.
- The port preserves the top-level structure: 12 selectable tunes, automatic
  track advance, play/pause, reset, setlist display, and animated visualizer.

Original authors retain copyright. This adaptation is distributed under the
same CC BY-NC-SA 4.0 terms as the source cart.

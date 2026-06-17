# Starjump Attribution

This PyxelPico port adapts **Starjump 1.0** by lucatron / Luca Harris.

- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=41874
- Live cart used for audit: https://www.lexaloffle.com/bbs/cposts/st/starjump-0.p8.png
- FCDB record: `id=88554`, `tid=41874`
- License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0

## Original Notes

The BBS post describes a star that jumps, with arrow/ESDF movement, Z/X/N/M
jump input, a menu for wobble intensity, timer display, screen skip, progress
reset, and an external soundtrack by the author. Community comments call out
vector-style art, tight platforming, breakable/disappearing platforms, toggled
floor/wall colors, red balloon/cannon sections, and discoverable double/triple
jump behavior.

## PyxelPico Adaptation Notes

- This first playable pass keeps a compact vector-platformer loop: movement,
  normal jump, double/triple jump charges, breakable bounce platforms, color
  toggled solid platforms, cannon launch, staged progression, timer, wobble
  visual style, and final return-to-start completion.
- Procedural replacement art/audio and an original cover are used instead of
  copying the cart label, vector data, level layouts, save data, or soundtrack.
- Exact authored room sequence, disappearing platform wave timings, original
  progress persistence, full menu/options surface, visual wobble math, and
  soundtrack synchronization are outside this first playable adaptation.

Original authors retain copyright. This adaptation is distributed under the
same CC BY-NC-SA 4.0 terms as the source cart.

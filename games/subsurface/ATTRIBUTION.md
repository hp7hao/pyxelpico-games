# subsurface Attribution

This PyxelPico port adapts **Subsurface 1.0.2** by JulianR / Julian Reid.

- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=54080
- Live cart used for audit: https://www.lexaloffle.com/bbs/cposts/su/subsurface-2.p8.png
- FCDB record: `id=134197`, `tid=54080`
- License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0

## Original Notes

The BBS post describes a compact metroidvania with 40 screens, 6 upgrades, about
6 enemies, one boss fight, save points, and controls for jumping/wall jumping,
gliding, swimming, shooting, and horizontal movement.

## PyxelPico Adaptation Notes

- The original source extracts successfully and shows upgrade flags for glide,
  double jump, wall jump, swim, health upgrades, switches, enemies, bullets,
  story captions, and boss/exploration systems.
- This first playable pass keeps a compact exploration loop: upgrades, jump,
  double jump, wall jump, glide, swim gating, shooting, enemies, health/energy,
  water hazard, boss damage, and victory.
- Procedural replacement art/audio and an original cover are used instead of
  copying the cart label, map, sprite sheet, story text, or music data.
- Exact 40-screen map progression, save-file behavior, story caption routing,
  switch rooms, all enemy variants, final platforming section, and original boss
  tuning are outside this first playable adaptation.

Original authors retain copyright. This adaptation is distributed under the
same CC BY-NC-SA 4.0 terms as the source cart.

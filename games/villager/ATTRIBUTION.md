# Villager Attribution

This PyxelPico port adapts **Villager** by partnano.

- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=38905
- Live cart used for audit: https://www.lexaloffle.com/bbs/cposts/na/nano_villager-0.p8.png
- FCDB record: `id=79613`, `tid=38905`
- License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0

## Original Notes

The BBS post describes a relaxing city-builder about gathering wood and stone,
building houses and other structures, attracting peeple, feeding them, keeping
them happy, and creating a cosy town with no harsh lose condition. The original
was inspired by a tile set by Cluly and intentionally shipped without save data.

## PyxelPico Adaptation Notes

- The original source extracts successfully and includes generated island/world
  objects, resources, buildings, player/UI, peeple, particles, and map mutation.
- This first playable pass keeps a compact city-builder loop: generated island
  resources, cursor movement, gathering, houses, farms, workshops, taverns,
  arrivals, food consumption, happiness, production, and peeple leaving if sad
  and hungry.
- Procedural replacement art/audio and an original cover are used instead of
  copying the cart label, tile set, sprites, map, or sound data.
- Exact island generator, Cluly tile-set presentation, all building types,
  villager pathing, particle/weather ambience, elegant two-button UI, and full
  no-save creative flow are outside this first playable adaptation.

Original authors retain copyright. This adaptation is distributed under the
same CC BY-NC-SA 4.0 terms as the source cart.

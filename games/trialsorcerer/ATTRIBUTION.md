# Trial of the Sorcerer

- Original title: Trial of the Sorcerer
- Original author: Mot
- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=43833
- Original cart: https://www.lexaloffle.com/bbs/cposts/mo/mot_sorcerer-11.p8.png
- License: CC BY-NC-SA 4.0

## Port Notes

This PyxelPico port is a first-playable Python adaptation for the Pico8Go
handheld target. It preserves the BBS-described core loop: first-person dungeon
movement, staff shots, monsters, loot, keys, locked doors, power crystals,
level exits, and a final Bahmott encounter.

The original cart is a dense procedural raycast FPS with custom rendering,
menus, enemy types, dungeon generation, mouse/controller options, music, and
PICO-8-specific presentation. This port uses a compact deterministic dungeon
core, simplified procedural art/audio, and a handheld control layout rather
than copying the original assets or full engine.

## Source Evidence

- FCDB entry: `id=94900`, `tid=43833`, author `Mot`, license
  `CC4-BY-NC-SA`.
- BBS description: procedurally generated 3D first-person shooter inspired by
  Wolfenstein 3D and Catacomb Abyss; shoot monsters, collect loot, find keys,
  unlock doors, find exits, and collect power crystals to level up the magic
  staff.
- Local extraction: `scripts/pico8_cart_extract.py` can extract source from
  the live slug cart URL, but this pass remains a manual first-playable
  adaptation because the original raycaster/game code is large and tightly
  token-packed.

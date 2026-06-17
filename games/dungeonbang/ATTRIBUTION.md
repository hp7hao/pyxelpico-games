# DUNGEON! Attribution

This PyxelPico port adapts **DUNGEON!** by deklaswas.

- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=46206
- Live cart used for audit: https://www.lexaloffle.com/bbs/cposts/du/dungeon-0.p8.png
- FCDB record: `id=105213`, `tid=46206`
- License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0

## Original Notes

The BBS post describes a retro platform dungeon run with randomly selected
courses, harder enemies as the game progresses, coins, a gift-shop powerup
system, zones with different visuals/music, wall jumping, weapons, and a final
rescue sequence.

## PyxelPico Adaptation Notes

- The current local extractor gets a compressed/minified fragment and top-level
  initialization strings, including shop item names/descriptions and ending
  dialogue, but not a practical source-level API scan for all gameplay systems.
- This first playable pass keeps the BBS-described core loop: wall-jump
  platforming, enemies, coins, shop upgrades, weapons, depth/zone progression,
  portal exits, and final rescue.
- Procedural replacement art/audio and an original cover are used instead of
  copying the cart label, room layouts, sprites, shop art, or music data.
- Exact room templates, full random course selection, all original items,
  enemy varieties, quips/dialogue, zone music, and ending scene are outside this
  first playable adaptation.

Original authors retain copyright. This adaptation is distributed under the
same CC BY-NC-SA 4.0 terms as the source cart.

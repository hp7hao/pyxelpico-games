# Harold's Bad Day Attribution

This PyxelPico port adapts **Harold's Bad Day 1.6** by biovoid.

- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=45507
- Live cart used for audit: https://www.lexaloffle.com/bbs/cposts/ha/harold-6.p8.png
- FCDB record: `id=100973`, `tid=45507`
- License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0

## Original Credits

- Game: biovoid
- Inspiration and additional graphics: thefreakar

## PyxelPico Adaptation Notes

- The original cart source extracts successfully and uses platformer physics,
  map/tile collision, deaths/respawns, corpse interactions, water/drowning,
  fire, wind, arrows, doors, SFX, music, and a 32-level map-memory campaign.
- This first playable pass keeps the core puzzle idea: lives as a resource,
  death creating a body, body-as-bridge puzzles, water drowning, spikes, goal
  completion, saved-Harold scoring, and reset/next-level flow.
- Procedural replacement art/audio and an original cover are used instead of
  copying the cart label, sprite sheet, map, or music data.
- Exact 32 authored levels, speedrun timer polish, water music muffling,
  palette fading, arrows/wind/fire variants, door/key systems, and original
  sprite/particle presentation are outside this first playable adaptation.

Original authors retain copyright. This adaptation is distributed under the
same CC BY-NC-SA 4.0 terms as the source cart.

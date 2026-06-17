# Cab Ride Attribution

This PyxelPico port adapts **Cab Ride 1.2** by Powersaurus.

- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=41332
- Live cart used for audit: https://www.lexaloffle.com/bbs/cposts/ca/cab_ride-7.p8.png
- FCDB record: `id=86966`, `tid=41332`
- License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0

## Original Credits

- Programming: Ben Jones / Powersaurus
- Music: Stephen `rych-t` Jones
- Based on Tom Mulgrew / Mot's Pseudo-3D Racer tutorials, also licensed under
  CC BY-NC-SA 4.0

## PyxelPico Adaptation Notes

- The original source extracts successfully and uses `_init`, `_update`,
  `_draw`, input, sprite/sprite-sheet rendering, palette/clip effects, SFX,
  music, random, and trigonometric helpers.
- This first playable pass keeps the relaxed train-sim loop: throttle/brake,
  slow braking, horn, station stops, doors, passengers, stop ratings, express
  mode, last-station announcement, journey completion, weather, and rolling
  scenery.
- Procedural replacement art/audio and an original cover are used instead of
  copying the cart label, sprite sheet, map, or music data.
- Exact pseudo-3D renderer, route generation, city/tunnel variety, second train,
  long-run memory behavior, full soundtrack, pause menu, and all visual effects
  are outside this first playable adaptation.

Original authors retain copyright. This adaptation is distributed under the
same CC BY-NC-SA 4.0 terms as the source cart.

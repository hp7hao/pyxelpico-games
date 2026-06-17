# Mot's 8-Ball Pool Attribution

This PyxelPico port adapts **Mot's 8-Ball Pool** by Mot.

- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=39859
- Live cart used for audit: https://www.lexaloffle.com/bbs/cposts/mo/mot_pool-23.p8.png
- FCDB record: `id=82696`, `tid=39859`
- License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0

## Original Notes

The BBS post describes a 3D 8-ball pool simulation inspired by 3D pool games on
C64/Amiga, playable against a friend or seven AI characters. It implements a
simplified 8-ball rule set with color assignment on the first sunk ball, legal
first-hit checks, fouls, free balls, and black-ball win/forfeit handling.

## PyxelPico Adaptation Notes

- The original source extracts successfully and includes table/ball constants,
  cue aiming/power, simulation modes, place-ball mode, AI, fouls, SFX, and menu
  state.
- This first playable pass keeps a compact top-down/3D-inspired pool loop: aim,
  power, cue-ball movement, ball contact/pocket resolution, first color
  assignment, fouls, free ball, black-ball win/forfeit, and two-player turn
  state.
- Procedural replacement art/audio and an original cover are used instead of
  copying the cart label, 3D renderer, ball sprites, UI, or sound/music data.
- Full 3D camera, AI opponents, ball-ball physics fidelity, white-ball placement
  UI, full shot legality edge cases, and all HUD polish are outside this first
  playable adaptation.

Original authors retain copyright. This adaptation is distributed under the
same CC BY-NC-SA 4.0 terms as the source cart.

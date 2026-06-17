# Brutal Pico Race Attribution

This PyxelPico port adapts **Brutal Pico Race 1.0.4** by dhostin / Damien
Hostin.

- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=31490
- Live cart used for audit: https://www.lexaloffle.com/bbs/cposts/br/brutalpicorace_104-0.p8.png
- FCDB record: `id=54001`, `tid=31490`
- License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0

## Original Credits

- Game: Damien Hostin / dhostin / yourykiki
- Community and technical thanks in the BBS thread include zep, p01,
  FSouchu, Felice Enellen, Morgan, playtesters, and family contributors.

## PyxelPico Adaptation Notes

- The original cart source extracts successfully and uses a pseudo-3D road and
  layered ship renderer, ship classes, six tracks, AI levels, split-screen
  multiplayer, boost, brake, drafting, health, lap timing, SFX, music, and
  persistence.
- This first playable pass keeps a compact single-player futuristic race:
  heavy/normal/light ship classes, acceleration/brake, boost meter, curved road,
  wall damage, drafting, AI opponent progress, lap finish, health, and ranking.
- Procedural replacement art/audio and an original cover are used instead of
  copying the cart label, sprite sheet, track data, ship sprites, or music data.
- Exact six tracks, split-screen/two-player mode, full 3D ship rasterizer,
  complete AI tuning, time boards, all HUD polish, and original soundtrack are
  outside this first playable adaptation.

Original authors retain copyright. This adaptation is distributed under the
same CC BY-NC-SA 4.0 terms as the source cart.

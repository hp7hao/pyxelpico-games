# Pico Tennis

- Original title: Pico Tennis
- Original author: paranoidcactus
- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=31450
- Original cart: https://www.lexaloffle.com/bbs/cposts/pi/picotennis2-0.p8.png
- License: CC BY-NC-SA 4.0

## Port Notes

This PyxelPico port is a first-playable Python adaptation for the Pico8Go
handheld target. It preserves the documented premise: tennis against AI,
serves, rallies, directional returns based on ball offset, power meter buildup,
power shots, faults, out calls, tennis scoring, games, sets, and match victory.

The port uses a host-tested rules core and procedural replacement art/audio
rather than copying original sprites, 3D rendering code, multiplayer support,
exact AI, exact shot physics, label art, or music.

## Source Evidence

- FCDB entry: `id=53753`, `tid=31450`, author `paranoidcactus`, license
  `CC4-BY-NC-SA`.
- BBS thread/cart display: live cart `picotennis2-0`, license
  `CC4-BY-NC-SA`.
- BBS description documents AI and up-to-4-player play, Z hit, X power shot,
  offset-based shot direction, power meter buildup, fault/out messaging, and
  best-of match updates.
- Local extraction: FCDB's numeric cart URL 404s; the live BBS slug cart
  downloads but current local extraction returns empty Lua/API text, so this
  pass uses BBS and FCDB evidence for a mechanics-level adaptation.

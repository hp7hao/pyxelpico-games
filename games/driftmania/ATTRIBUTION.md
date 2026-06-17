# Driftmania

- Original title: Driftmania
- Original author: Max Bize
- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=140202
- Original cart: https://www.lexaloffle.com/bbs/cposts/dr/driftmania-5.p8.png
- License: CC BY-NC-SA 4.0

## Original Credits From BBS

- Created by Max Bize
- Music by Vav
- Cars based on art by PixelArtM
- Cover art by TerracotaScarf
- Special thanks to `thisismypassword`, `TheRoboZ`, and `johanp`

## Port Notes

This PyxelPico port is a first-playable Python adaptation for the Pico8Go
handheld target. It preserves the documented premise: arcade time-trial racing,
acceleration, braking/reverse, left/right steering, drift brake, grass traction,
boost tiles, checkpoint gates, lap timing, restart, and medal targets.

The port uses a host-tested rules core and procedural replacement art/audio
rather than copying original sprites, car art, cover art, music, full 15-track
campaign, ghost replay, garage customization, pause/options menus, exact 3D
sprite-stacking presentation, or speedrun tuning.

## Source Evidence

- FCDB entry: `id=141515`, `tid=140202`, author `MaxBize`, license
  `CC4-BY-NC-SA`, tags `racing` and `speedrun`.
- BBS thread/cart display: live cart `driftmania-5`, license `CC4-BY-NC-SA`.
- BBS description documents 15 tracks, time trial goal, accelerate/brake/turn,
  D-brake, restart, pause/options, grass traction, boost tiles, ghost replay,
  medals, garage customization, and upstream contributor credits.
- Local extraction: the live BBS slug cart downloads and extracts minified Lua
  with `scripts/pico8_cart_extract.py`.

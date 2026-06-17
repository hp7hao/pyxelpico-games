# pigments

- Original title: pigments
- Original author: benjamin_soule
- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=40490
- Original cart: https://www.lexaloffle.com/bbs/cposts/pi/pigments-0.p8.png
- License: CC BY-NC-SA 4.0

## Port Notes

This PyxelPico port is a first-playable Python adaptation for the Pico8Go
handheld target. It preserves the documented core premise: collect pigment
droplets, paint the board, dodge razor discs, and use special grass, water,
and trigger tiles to survive.

The port uses a host-tested rules core and procedural replacement art/audio
rather than copying original sprites, label art, fruit/unlock progression,
highscore persistence, exact disc behavior, music, or full level variants.

## Source Evidence

- FCDB entry: `id=84480`, `tid=40490`, author `benjamin_soule`, license
  `CC4-BY-NC-SA`.
- BBS thread/cart display: live cart `pigments-0`, license `CC4-BY-NC-SA`.
- BBS description documents the goal: get pigment droplets, dodge deadly razor
  discs, and paint all tiles.
- BBS description documents special tiles: grass blocks discs, water hides the
  player from discs while consuming pigments, and triggers make all discs dash
  toward the player.
- Local extraction: FCDB's numeric cart URL 404s, but the BBS slug cart
  downloads and extracts readable obfuscated Lua/mechanic strings with
  `scripts/pico8_cart_extract.py`.

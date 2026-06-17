# Shadows of Dunwich 2.0

- Original title: Shadows of Dunwich 2.0
- Original author: paranoidcactus
- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=34047
- Original cart: https://www.lexaloffle.com/bbs/cposts/sh/shadowsofdunwich-4.p8.png
- License: CC BY-NC-SA 4.0

## Port Notes

This PyxelPico port is a first-playable Python adaptation for the Pico8Go
handheld target. It preserves the documented tactical premise: a small soldier
squad, turn-based action points, movement, shooting, grenades, enemy turns,
split-on-death enemies, soldier survival, leveling, recruit replacement, and a
campaign that resolves at level 16.

The port uses a host-tested rules core and procedural replacement art/audio
rather than copying original sprites, map data, 3D sprite presentation, music,
exact procedural battle generation, full talent tree, save data, or original
balance. BBS text describes the game as X-Com-like; this port uses generic
occult squad-tactics presentation and no third-party branded assets.

## Source Evidence

- FCDB entry: `id=63959`, `tid=34047`, author `paranoidcactus`, license
  `CC4-BY-NC-SA`.
- BBS thread/cart display: live cart `shadowsofdunwich-4`, license
  `CC4-BY-NC-SA`.
- BBS description documents multiple battles, procedurally generated maps,
  soldier leveling, skill points, recruit replacement after casualties, new
  enemy types, campaign levels, level 16 victory, and between-mission saving.
- Local extraction: the live BBS cart downloads, but the current local
  extractor returns empty Lua/API text for this cart, so this pass uses BBS and
  FCDB evidence for a mechanics-level adaptation.

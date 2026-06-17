# Whiplash Taxi Co

- Original title: Whiplash Taxi Co
- Original author: Mot
- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=53583
- Original cart: https://www.lexaloffle.com/bbs/cposts/mo/mot_taxi-7.p8.png
- License: CC BY-NC-SA 4.0

## Port Notes

This PyxelPico port is a first-playable Python adaptation for the Pico8Go
handheld target. It preserves the documented premise: driving a taxi around a
city, stopping near passengers to pick them up, following destination
indicators, stopping to drop them off, earning fares, deliberate forward/reverse
switching, crashes, and a five-minute shift timer.

The port uses a host-tested rules core and procedural replacement art/audio
rather than copying original sprites, map data, 3D rendering, music, AI traffic,
free-explore/race modes, full Motsville layout, lap records, or exact driving
tuning. BBS comments compare the game to Crazy Taxi/GTA; this port uses generic
taxi delivery presentation and no third-party branded assets.

## Source Evidence

- FCDB entry: `id=132559`, `tid=53583`, author `Mot`, license
  `CC4-BY-NC-SA`, tags `3d`, `taxi`, `racing`, and `driving`.
- BBS thread/cart display: live cart `mot_taxi-7`, license `CC4-BY-NC-SA`.
- BBS description documents passenger pickup, destination indicators, stopping
  to board/drop off, a five-minute money goal, free-explore map study, street
  circuits/lap records, and deliberate stop-before-reverse control behavior.
- Local extraction: the live BBS slug cart downloads and extracts readable Lua
  plus a broad PICO-8 API surface with `scripts/pico8_cart_extract.py`.

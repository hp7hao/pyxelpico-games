# Night Ride

- Original title: Night Ride
- Original author: vladcom
- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=39650
- Original cart: https://www.lexaloffle.com/bbs/cposts/ni/nightride-0.p8.png
- License: CC BY-NC-SA 4.0

## Port Notes

This PyxelPico port is a first-playable Python adaptation for the Pico8Go
handheld target. It preserves the documented premise: high-speed night driving
through traffic, escalating levels, survival hazards, a later shooting mechanic,
enemy vehicles, a boss fight, score, health, and sunrise victory.

The port uses a host-tested rules core and procedural replacement art/audio
rather than copying original sprites, particles, music, exact level scripts,
boss patterns, car rotation art, sunrise ending art, or precise difficulty. BBS
comments compare the game to Spy Hunter; this port uses generic night-road
presentation and no third-party branded assets.

## Source Evidence

- FCDB entry: `id=82007`, `tid=39650`, author `vladcom`, license
  `CC4-BY-NC-SA`, tags `racing`, `shooter`, `boss`, and `fight`.
- BBS thread/cart display: live cart `nightride-0`, license `CC4-BY-NC-SA`.
- BBS description documents high-speed traffic survival, dangers, night-to-dawn
  progression, racing/shooter/boss-fight tags, and comments document later
  shooting mechanics, traffic, level escalation, boss, and sunrise ending.
- Local extraction: the live BBS slug cart downloads and extracts readable Lua
  plus a PICO-8 API surface with `scripts/pico8_cart_extract.py`.

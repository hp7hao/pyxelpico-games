# Scrap Boy

- Original title: Scrap Boy
- Original author: BoneVolt
- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=39800
- Original cart: https://www.lexaloffle.com/bbs/cposts/sc/scrap_boy-6.p8.png
- License: CC BY-NC-SA 4.0

## Port Notes

This PyxelPico port is a first-playable Python adaptation for the Pico8Go
handheld target. It preserves the documented core premise: compact action
platforming, collectibles, multiple weapon/forms, spike hazards, bomb-gated
doors, magnet wall-jump behavior, enemies, and level clear.

The port uses a host-tested rules core and procedural replacement art/audio
rather than copying original sprites, map data, music, exact enemy patterns,
full 3-level progression, 6 complete weapons, difficulty modes, time attack,
pause-menu button swapping, or speedrun tuning. BBS comments compare the game
to Mega Man-like platformers; this port uses generic robot/scrap presentation
and no third-party branded assets.

## Source Evidence

- FCDB entry: `id=82518`, `tid=39800`, author `BoneVolt`, license
  `CC4-BY-NC-SA`.
- BBS thread/cart display: live cart `scrap_boy-6`, license `CC4-BY-NC-SA`.
- BBS description documents 3 levels, 6 weapons, 3 difficulties, collectibles,
  time attack, and X/O swapping.
- BBS comments mention bomb-gated walls/doors, spike immunity with bomb power,
  auto-laser, magnet power-up, and magnet wall-jumping.
- Local extraction: FCDB's numeric cart URL 404s, but the BBS slug cart
  downloads and extracts readable Lua/API with `scripts/pico8_cart_extract.py`.

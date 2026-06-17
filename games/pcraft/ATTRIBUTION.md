# P.Craft

- Original title: P.Craft
- Original author: NuSan
- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=3200
- Original cart: https://www.lexaloffle.com/bbs/cposts/2/24981.p8.png
- License: CC BY-NC-SA 4.0

## Port Notes

This PyxelPico port is a first-playable Python adaptation for the Pico8Go
handheld target. It preserves the BBS-described core loop: wake on a deserted
island, gather materials, craft tools at a workbench, explore a cave, and build
a boat to escape.

The original thread says P.Craft is heavily inspired by Notch's Ludum Dare game
Minicraft. This port documents that inspiration trail but uses generic island
survival presentation and procedural replacement art/audio rather than copying
Minicraft or P.Craft assets. The later P.Craft Deluxe / Stranded Isle releases
are not used as source material here.

## Source Evidence

- FCDB entry: `id=19680`, `tid=3200`, author `NuSan`, license
  `CC4-BY-NC-SA`.
- BBS description: crafting/survival game; gather materials, build tools,
  explore the area, find a cave, craft a sword, and craft a boat to escape.
- Local extraction: FCDB's numeric cart URL returns 404 and the live cart URL
  downloads, but `scripts/pico8_cart_extract.py` returned no usable Lua/API
  text for this cart, so this pass is a manual first-playable adaptation.

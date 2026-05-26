# XMAS Pong

**Original title**: XMAS Pong  
**Original author**: ReturnOH  
**License**: CC BY-NC-SA 4.0  
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=153606  
**Original cart**: https://www.lexaloffle.com/bbs/cposts/ra/ramgadofu-1.p8.png

PICO-8 metadata source: `projects/fcdb/sources/pico8/bbs_release.json` (id/pid `179971`, tid `153606`, slug `ramgadofu`).

## Changes for PyxelPico

- Implemented a handheld-friendly Pyxel/PyxelPico port in `games/xmaspong/xmaspong.py`.
- Preserved the core 1vCPU pong loop: paddle movement, ball bounce, scoring race to 10.
- Added simple holiday-themed presentation (snow + festive colors) consistent with the original theme.
- Adapted controls for dual keyboard/gamepad through `lib/input_helper.py`.
- Added a native 240x240 cover image (`games/xmaspong/cover.png`) for launcher/cart metadata.

## Notes

- This is a gameplay-faithful manual port; exact original PICO-8 sprite/audio data is not embedded.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); distribution must follow those terms.

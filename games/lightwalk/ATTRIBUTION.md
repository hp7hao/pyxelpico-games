# LightWalk

**Original author**: juliusspeak
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=154308
**Original cart**: https://www.lexaloffle.com/bbs/cposts/li/lightwalk-0.p8.png
**Upstream source**: https://github.com/juliusspeak/lightwalk

PICO-8 metadata source: `projects/fcdb/sources/pico8/bbs_release.json` (id `181886`, tid `154308`).

## Changes for PyxelPico

- Reimplemented the gameplay logic in Python for Pyxel/PyxelPico (`games/lightwalk/lightwalk.py`).
- Preserved core puzzle mechanics: generated network, tile rotation, power propagation, and lamp win condition.
- Added handheld-friendly controls using `lib/input_helper.py` (D-pad cursor movement, A rotate, B/Start restart).
- Added launcher cover from BBS thumbnail (`games/lightwalk/cover.png`).

## Notes

- Upstream GitHub repo currently has no standalone LICENSE file; project license is taken from BBS/FCDB metadata.
- This port currently recreates gameplay behavior with simplified custom rendering instead of original PICO-8 sprite extraction.

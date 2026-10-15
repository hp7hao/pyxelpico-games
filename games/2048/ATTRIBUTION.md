# 2048

**Original author**: straversi
**License**: CC BY-NC-SA 4.0
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=153397
**Original cart**: https://www.lexaloffle.com/bbs/cposts/179297.p8.png

PICO-8 metadata source: FCDB PICO-8 bbs metadata (id/pid `179297`, tid `153397`).

## Changes for PyxelPico

- Reimplemented gameplay loop in Python for Pyxel/PyxelPico (`games/2048/2048.py`).
- Preserved core 4x4 merge rules, random tile spawning (2/4), score accumulation, and game-over detection.
- Adapted controls for handheld mapping via `lib/input_helper.py` (D-pad move, A/B/Start restart).
- Added a native 240x240 cover image (`games/2048/cover.png`) for launcher/cart metadata.

## Notes

- This port targets gameplay fidelity and simple presentation; it does not reproduce exact original PICO-8 visuals/audio.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); distribution must respect those terms.

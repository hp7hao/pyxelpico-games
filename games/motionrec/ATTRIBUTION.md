# MOTION REC

- Original title: MOTION.REC
- Original author: shomaisshi
- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=53392
- Original cart: https://www.lexaloffle.com/bbs/cposts/mo/motionrec-3.p8.png
- License: CC BY-NC-SA 4.0

## Port Notes

This PyxelPico port is a first-playable Python adaptation for the Pico8Go
handheld target. It preserves the BBS-described core idea: an action-puzzle
platformer where the player records movement, replays the stored motion, plays
it back in reverse, and uses repeated motion to solve switch/goal puzzles.

The original cart credits @matthughson's Advanced Micro Platformer Starter Kit
as its template. This port keeps that attribution trail and implements a small
host-tested motion-recording rules core rather than copying original sprites,
maps, timing, effects, or full level design.

## Source Evidence

- FCDB entry: `id=131910`, `tid=53392`, author `shomaisshi`, license
  `CC4-BY-NC-SA`.
- BBS description: action puzzle game with the concept of "recording and
  replaying movements"; Up+Z starts recording, Z plays back the recorded
  motion, and Down+Z plays it in reverse.
- Local extraction: `scripts/pico8_cart_extract.py` extracts source from the
  live slug cart URL and confirms the platformer-template attribution.

# Guncho

- Original title: Guncho
- PICO-8 cart author: spoike
- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=48452
- Original cart: https://www.lexaloffle.com/bbs/cposts/gu/guncho-3.p8.png
- License: CC BY-NC-SA 4.0

## Port Notes

This PyxelPico port is a first-playable Python adaptation for the Pico8Go
handheld target. It preserves the documented PICO-8 cart loop: a turn-based
wild-west tactics game across bandit camps, with move, revolver, punch,
bullet-hail, wait, dynamite, and boss progression concepts.

The PICO-8 cart itself credits the original 7DRL game by Arnold Rauers and
Terri Vellman. This port uses the CC BY-NC-SA BBS cart as the migration source
and implements a compact host-tested rules core rather than copying original
sprites, music, exact map generation, UI, AI tuning, or assets from later
commercial releases.

## Source Evidence

- FCDB entry: `id=114060`, `tid=48452`, author `spoike`, license
  `CC4-BY-NC-SA`.
- BBS description: battle through five bandit camps in a turn-based western
  roguelike.
- BBS controls/mechanics: rotate with left/right; actions include move,
  revolver shoot/reload, punch, sprint, bullet hail, and wait.
- Extracted cart source: `scripts/pico8_cart_extract.py` successfully extracts
  the live slug cart and confirms API usage plus modes/enemy/dynamite/revolver
  mechanics.

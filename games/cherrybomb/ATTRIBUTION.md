# Cherry Bomb

- Original title: Cherry Bomb
- Original author/designer: Krystian Majewski / Lazy Devs Academy
- Original music credit: Sebastian Hassler
- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=48986
- Original cart: https://www.lexaloffle.com/bbs/cposts/ch/cherrybomb-0.p8.png
- License: CC BY-NC-SA 4.0

## Port Notes

This PyxelPico port is a first-playable Python adaptation for the Pico8Go
handheld target. It preserves the documented core premise: pilot a red ship,
shoot through 9 waves of aliens, dodge enemy fire, collect cherry pickups,
spend cherries on a bomb, restore hearts after 10 cherries, and chase score.

The port uses a host-tested rules core and procedural replacement art/audio
rather than copying original sprites, music, logo/title animation, exact enemy
formations, highscore persistence, tutorial code structure, or full scoring
tuning.

## Source Evidence

- FCDB entry: `id=116115`, `tid=48986`, author `Krystman`, license
  `CC4-BY-NC-SA`.
- BBS thread/cart display: live cart `cherrybomb-0`, license `CC4-BY-NC-SA`.
- BBS description documents controls: arrow keys move, X shoots, O bombs.
- BBS description documents 9 waves, hearts, cherry pickups, cherry-powered
  bombs, 10-cherry heart restoration/bonus scoring, and enemy-bullet bomb
  scoring.
- Local extraction: FCDB's numeric cart URL 404s, but the BBS slug cart
  downloads and extracts readable Lua/API with `scripts/pico8_cart_extract.py`.

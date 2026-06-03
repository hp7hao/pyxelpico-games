# PICO-BALL Attribution

**PyxelPico port**: `games/picoball/picoball.py`

**Original title**: PICO-BALL: a Sports Game Starring Jelpi  
**Original author**: Munchkin  
**Original source**: https://www.lexaloffle.com/bbs/?tid=150620  
**Original cart**: https://www.lexaloffle.com/bbs/cposts/pi/pico_ball-5.p8.png  
**License**: CC BY-NC-SA 4.0, as reported by the Lexaloffle BBS / local FCDB metadata (`CC4-BY-NC-SA`).

## Port notes

- This is a first playable PyxelPico adaptation for the 240x240 Pico8Go target.
- It preserves the published solo/wallball premise: a mashup of tennis, volleyball, squash, and wallball where two bounces on one side gives the other side a point.
- Controls are reduced for handheld solo play: D-pad moves Jelpi, A/Up jumps, A/Start serves or rematches.
- The original cart code is stored with newer PICO-8 `pxa` compression. The vendored `picotool` path currently extracts cart RAM/label bytes but cannot decode Lua, so this pass is not line-by-line source parity.
- The cover image is derived from the original downloadable PICO-8 cart label. Gameplay rendering and SFX are simplified procedural replacements.

Original author retains copyright. This port follows the same CC BY-NC-SA 4.0 constraints.

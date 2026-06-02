# Office Hell Attribution

**PyxelPico port**: `games/officehell/officehell.py`

**Original title**: Office Hell  
**Original author**: OlieB123  
**Original source**: https://www.lexaloffle.com/bbs/?tid=154283  
**Original cart**: https://www.lexaloffle.com/bbs/cposts/of/office_hell_1_0-0.p8.png  
**License**: CC BY-NC-SA 4.0, as reported by the Lexaloffle BBS / local FCDB metadata.

## Port notes

- This is a first playable PyxelPico adaptation for the 240x240 Pico8Go target.
- It preserves the documented premise and control model: choose Jimbo's left/right direction, then time jumps while he auto-runs through office hazards.
- The original cart code is stored with newer PICO-8 `pxa` compression. The vendored `picotool` path currently extracts map/gfx/sfx/music bytes but cannot decode Lua, so this pass is not line-by-line source parity.
- The cover image is derived from the original downloadable PICO-8 cart label. Gameplay rendering and SFX are simplified procedural replacements.

Original author retains copyright. This port follows the same CC BY-NC-SA 4.0 constraints.

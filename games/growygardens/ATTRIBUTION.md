# GrowyGardens Attribution

**Original Game**: GrowyGardens
**Author**: SuperZooper3
**License**: MIT (see LICENSE file)
**Source**: https://github.com/SuperZooper3/GrowyGardens

## Changes for Pico8Go

- Resolution scaled from 128x128 to 240x240 via 2x integer scale with screen-copy blit (8px crop per edge)
- Added gamepad D-pad support for movement
- Added gamepad cycle+execute action system (A=cycle through water/plant/bonk, B=execute selected action)
- Added bottom bar action indicator highlight for gamepad users
- Added Start/A button to begin game
- Resource path changed to use relative SCRIPT_DIR for portable loading
- Added `display_scale=3` for desktop preview

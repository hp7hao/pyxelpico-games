# Kektris

**Original author**: Konstantin Klepikov
**License**: MIT
**Source**: https://github.com/KonstantinKlepikov/kektris

## Changes for Pico8Go

- Resolution changed from 256x256 to 240x240
- Cell size reduced from 5px to 4px (stride 5px) to fit grid + sidebar in 240px
- Grid area repositioned and resized for 240x240
- All keyboard inputs now also accept gamepad equivalents (dual-input)
- Keyboard-only shortcuts (R=restart, P=pause, M=music, G=grid) remapped to gamepad buttons:
  - Start = pause/unpause
  - Select = toggle music
  - A = restart (on game-over screen)
  - B = toggle grid highlight
- Bottom controls help replaced with gamepad button labels
- Logo/image asset repositioned for new layout

# Field Jump Attribution

**Original title**: Field Jump - Collect coins, avoid obstacles
**Original author**: fieldjump
**Original source**: https://www.lexaloffle.com/bbs/?tid=154315
**Original cart**: https://www.lexaloffle.com/bbs/cposts/fi/fieldjump-0.p8.png
**License**: CC BY-NC-SA 4.0, per local FCDB/BBS metadata (`CC4-BY-NC-SA`)

## Adaptation

This PyxelPico version is a Python/Pyxel port for the 240x240 Pico8Go target.
It preserves the published high-level premise — side-scrolling platformer,
collect coins, avoid obstacles, with level progression — with handheld controls:

- D-pad Up or A: jump
- D-pad Down: duck
- Start/A: start, advance clear screens, or restart

## Notes

- The PICO-8 cart was downloaded and inspected from the BBS cart URL.
- Current local tooling can extract the cart shell and label, but the Lua code
  is stored with newer PICO-8 `pxa` compression that the vendored `picotool`
  does not decode yet. This port is therefore a first playable approximation,
  not a line-by-line Lua translation.
- `cover.png` is derived from the original downloadable cart label.
- No original audio data was reused; simple replacement Pyxel SFX are generated
  in code.
- 2026-06-05 follow-up: added explicit stage goals, level-clear transitions,
  a final win state, progress meter, and a higher-level flying obstacle to more
  closely match the BBS-described "levels and many more features" premise while
  exact Lua parity remains blocked by `pxa` decoding.

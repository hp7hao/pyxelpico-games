# ACLM

**Original author**: Jay Kumogata
**License**: Apache-2.0
**Source**: https://github.com/jay-kumogata/RetroGames

Inspired by Wingman's "ACLM" from BASIC Magazine (Oct 1983, p.77).

## Changes for Pico8Go

- Rewritten to native 240x240 resolution with coordinate scaling (all positions multiplied by 240/128)
- Missile trails render natively using `circ(r=1)` for visible dots at higher resolution
- Input remapped for 8-button gamepad (D-pad LEFT/RIGHT or A/B to steer, A/Start to restart)

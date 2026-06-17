# Freezing Knights

**Original author**: tinyevilwizard
**Music author**: OhCurtains
**License**: CC BY-NC-SA 4.0
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=50683
**Source (GitHub)**: https://github.com/tinyevilwizard/FreezingKnights
**Original cart**: https://www.lexaloffle.com/bbs/cposts/fr/freezing_knights-9.p8.png

PICO-8 metadata source: `projects/fcdb/sources/pico8/bbs_release.json`
(id/pid `122532`, tid `50683`; live cart id `freezing_knights-9` from the
BBS thread and GitHub source repository).

## Changes for PyxelPico

- Reimplemented a first playable two-knight turn-based RPG adaptation in
  Python for Pyxel/PyxelPico.
- Preserved the BBS-described core: snowy mountain-path progression, two
  knights with distinct stats, enemy encounters, timed defensive jumps/guards,
  potions, gold rewards, rest/safe zones, upgrades, party-wipe recovery, and a
  summit boss route.
- Added `freezingknights_core.py` as a host-testable gameplay core for path
  selection, battle attacks, timed defense, rest recovery, upgrades, and wipe
  fallback.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the snowy two-knight RPG
  premise.

## Notes

- The upstream source is a polished 14-cart PICO-8 RPG with authored maps,
  menus, many encounters, two-player controls, soundtrack, custom sprites,
  hard mode, persistence, and full ending flow.
- This is a compact first playable adaptation, not a full source translation of
  all carts, exact battle patterns, original assets, music, menus, or
  progression data.
- The original is described as inspired by turn-based RPGs; this port avoids
  third-party branded characters, names, and assets and uses generic knight,
  mountain, enemy, and timing-defense presentation.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

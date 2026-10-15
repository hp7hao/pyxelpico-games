# Air Delivery

**Original author**: pianoman373
**License**: CC BY-NC-SA 4.0 (from PICO-8 BBS / FCDB metadata)
**Source (BBS thread)**: https://www.lexaloffle.com/bbs/?tid=52598
**Original cart**: https://www.lexaloffle.com/bbs/cposts/ai/air_delivery_1-3.p8.png

PICO-8 metadata source: FCDB PICO-8 bbs metadata
(id/pid `129275`, tid `52598`; live cart id `air_delivery_1-3` from the BBS thread).

## Changes for PyxelPico

- Reimplemented a first playable sky-island delivery platformer adaptation in
  Python for Pyxel/PyxelPico.
- Preserved the BBS-described core: moving and climbing around sky islands,
  coyote-time jumping, interacting with recipients, finding letters/packages,
  delivery rewards, gliding, secret passage drilling, hazards/death, and
  finishing at the airship after deliveries.
- Added `airdelivery_core.py` as a host-testable gameplay core for movement,
  ladder climb, coyote jump, glide, letter collection, recipient delivery,
  reward unlocks, drill passage, hazard respawn, and airship completion.
- Added handheld controls using `lib/input_helper.py`.
- Added an original PyxelPico cover image inspired by the mail/sky-island
  premise.

## Notes

- FCDB's numeric cart URL is stale; the BBS thread exposes the working cart
  path `https://www.lexaloffle.com/bbs/cposts/ai/air_delivery_1-3.p8.png`.
- The live cart extracts a partial Lua/API surface with `scripts/pico8_cart_extract.py`,
  including the title/prologue, palette setup, sprite/string data, and rendering
  calls, but most gameplay code remains opaque to the local extractor.
- This is a compact first playable adaptation, not a full source translation of
  the original dense world, all 9 letters, NPC dialogue, exact glider handling,
  secrets, music, sprite work, or ending presentation.
- License is non-commercial share-alike (CC BY-NC-SA 4.0); redistribution must
  respect those terms.

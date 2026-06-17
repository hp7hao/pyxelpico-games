# Two Hiking Cats Attribution

This PyxelPico port adapts **Two Hiking Cats Have An In Depth Discussion About
Life The Universe And Everything** by solar.

- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=2719
- Live cart used for audit: https://www.lexaloffle.com/bbs/cposts/1/16151.p8.png
- FCDB record: `id=16152`, `tid=2719`
- License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0

## Original Notes

The BBS post describes the cart as a scrolling background/art toy made mostly
from lines, circles, and the modulo operator. It is intentionally not a
traditional game: left/right change speed, up randomizes the palette, and down
resets the changes. Comments and the author discussion describe the meow cadence
as the imagined conversation.

## PyxelPico Adaptation Notes

- The current local extractor downloads the live cart but returns only a tiny
  invalid fragment, so this pass follows BBS-described behavior rather than
  line-by-line source parity.
- This first playable pass keeps scrolling hills, two walking cats, meow
  cadence, speed adjustment, palette randomization, and reset controls.
- A/B meow buttons are added as a small controller-friendly art-toy extension
  inspired by BBS comments about puppet-like cat conversations.
- Visuals, cover art, and audio are procedural replacements and do not copy the
  original cart label/sprite/audio data.

Original authors retain copyright. This adaptation is distributed under the
same CC BY-NC-SA 4.0 terms as the source cart.

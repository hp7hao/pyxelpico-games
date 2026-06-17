# Wobblepaint

- Original title: Wobblepaint 1.6
- Original author: zep
- Original BBS thread: https://www.lexaloffle.com/bbs/?tid=40058
- Original cart: https://www.lexaloffle.com/bbs/cposts/wo/wobblepaint-6.p8.png
- License: CC BY-NC-SA 4.0

## Port Notes

This PyxelPico port is a first-playable Python adaptation for the Pico8Go
handheld target. It preserves the documented gamepad-friendly premise: D-pad
cursor movement, painting, brush size adjustment, undo, simple color changes,
clear/new doodle behavior, and animated wobbling strokes.

The port uses a host-tested rules core and procedural replacement art/audio
rather than copying original cart data, menu system, palettes, patterns,
multi-doodle storage, paste/export format, GIF recording, self-saving cart data,
or exact wobble rendering.

## Source Evidence

- FCDB entry: `id=83422`, `tid=40058`, author `zep`, license
  `CC4-BY-NC-SA`, tags `tool`, `paint`, `doodle`, and `wobblepaint`.
- BBS thread/cart display: live cart `wobblepaint-6`, license
  `CC4-BY-NC-SA`.
- BBS description documents brush size/color/pattern/shape, presets,
  undo/redo, multiple doodles, menu toggle, save/export behavior, GIF capture,
  and gamepad controls: D-pad cursor, X paint, O plus left/right undo/redo,
  and O plus up/down brush size.
- Local extraction: FCDB's numeric cart URL is stale; the live BBS slug cart
  downloads but current local extraction returns empty Lua/API text, so this
  pass uses BBS and FCDB evidence for a mechanics-level adaptation.

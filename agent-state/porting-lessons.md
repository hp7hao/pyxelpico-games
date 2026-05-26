# PyxelPico Games Porting Lessons

Append concise lessons after each candidate attempt.

Template:

```markdown
## <game-id> — <YYYY-MM-DD>

- Result: done | blocked | partial
- What translated cleanly:
- What needed shims/manual rewrite:
- Asset/audio notes:
- Verification:
- Reusable helper opportunities:
- Backlog changes:
```

## xmaspong — 2026-05-26

- Result: done
- What translated cleanly: Core Pong loop (single paddle + CPU paddle, wall/paddle bounce, score race to win) maps cleanly to a small Pyxel state machine.
- What needed shims/manual rewrite: Full manual rewrite in Python; relied on `lib/input_helper.py` for D-pad + A/B/Start mapping and added a lightweight title/gameover flow for handheld play.
- Asset/audio notes: Could not reliably extract newer slug-style cart Lua/data with current local tooling; used an original 240x240 festive cover and no original PICO-8 audio.
- Verification: `python3 -m py_compile scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/xmaspong/xmaspong.py`; `make cart-game GAME=xmaspong PYTHON=python3`.
- Reusable helper opportunities: A tiny shared `pong_core` helper (ball/paddle collision + AI tracking) could speed up future arcade ports.
- Backlog changes: Marked XMAS Pong done with FCDB license/source confirmation and noted remaining extraction limitation.

## lightwalk — 2026-05-26

- Result: done
- What translated cleanly: Upstream Lua structure (`cell/grid/game/pointer`) maps directly to Python classes; generation pipeline (seed source → line growth → fill + shuffle) preserved with near 1:1 control flow.
- What needed shims/manual rewrite: Replaced PICO-8 sprite-sheet rendering with procedural Pyxel drawing while keeping connection topology and power checks intact.
- Asset/audio notes: Used BBS thumbnail as cover; no original audio carried over yet.
- Verification: `python3 -m py_compile scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py`; `make cart-game GAME=lightwalk PYTHON=python3`.
- Reusable helper opportunities: A shared `grid_puzzle` helper (neighbors/connectivity/flood-power) would reduce duplicate logic for future Sokoban/net puzzles.
- Backlog changes: Marked XMAS Pong / Floppy Canary / PicoSorter blocked due to current cart-code extraction gap; advanced to LightWalk and completed.

## early-bbs-cart-inspection — 2026-05-26

- Result: blocked
- What translated cleanly: FCDB metadata lookup and BBS thread/cart URL discovery still works.
- What needed shims/manual rewrite: None yet; blocker occurs before gameplay translation.
- Asset/audio notes: Newer BBS slug-style cart URLs download, but current local picotool parsing returns empty Lua for sampled carts.
- Verification: Confirmed across `straversi_2048-2`, `ramgadofu-1`, `floppycanary-2`, `daworunut-0` carts (download ok, parsed Lua empty).
- Reusable helper opportunities: Add/repair a local extractor path (browser-side `print_pico8_code` equivalent or updated parser) before auditing more BBS-only carts.
- Backlog changes: Marked affected early candidates blocked with concrete tooling reason.


## 2048 — 2026-05-26

- Result: done
- What translated cleanly: 4x4 deterministic slide/merge rules, score accumulation, random 2/4 spawning, and dead-board detection.
- What needed shims/manual rewrite: full manual rewrite in Pyxel; used `lib/input_helper.py` for dual keyboard/gamepad directional + restart mapping.
- Asset/audio notes: no source sprite/audio extraction used; created a simple original 240x240 cover image; gameplay-only port with simplified visuals and no music/SFX.
- Verification: `python3 -m py_compile scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/2048/2048.py` and `make cart-game GAME=2048 PYTHON=python3` both passed.
- Reusable helper opportunities: consider a shared tiny `grid2048` utility if more number-puzzle ports land (line merge + spawn + move checks).
- Backlog changes: marked 2048 as done and recorded FCDB license/source/cart confirmation + implementation note.

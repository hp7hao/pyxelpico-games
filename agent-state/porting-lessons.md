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

## santaban — 2026-05-26

- Result: done
- What translated cleanly: Sokoban core (push-only movement, collision/goal checks, move counter, undo stack, level-complete gating) maps cleanly to a small grid-state engine.
- What needed shims/manual rewrite: Full manual rewrite in Python; replaced PICO-8 scene/menuitem flow and sprite/map drawing with Pyxel scene states and primitive rendering while preserving 25-level progression.
- Asset/audio notes: Decoded cart from `https://www.lexaloffle.com/bbs/cposts/sa/santaban-3.p8.png`; extracted level definitions plus map/flag RAM sections into `santaban_data.py`; used cart label-derived cover and simple replacement SFX (no original sprite/audio asset extraction yet).
- Verification: `python3 -m py_compile scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/santaban/santaban_data.py games/santaban/santaban.py`; `make cart-game GAME=santaban PYTHON=python3`.
- Reusable helper opportunities: A shared `sokoban_core` helper (tile/box occupancy, push validation, undo snapshots, win checks) could reduce duplicate logic for future box-pushing/grid puzzle ports.
- Backlog changes: Marked Santaban done with FCDB + BBS slug cart URL confirmation and noted the working PXA decode path for cart inspection.

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

## fieldjump — 2026-05-31

- Result: partial
- What translated cleanly: High-level BBS premise (Chrome-Dino-like side-scroller with coins/obstacles/levels) maps cleanly to a deterministic Pyxel runner loop with D-pad/A jump, down-duck, coin collection, lives, score, and level-scaled speed.
- What needed shims/manual rewrite: Full manual rewrite; exact PICO-8 Lua/API audit is blocked because the cart code begins with newer `pxa` compression unsupported by the vendored `picotool` path.
- Asset/audio notes: Used the downloadable cart label as `cover.png`; no original sprite/audio sections were reused in gameplay, and simple replacement SFX are generated in code.
- Verification: `python3 -m py_compile scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/fieldjump/fieldjump.py`; `make cart-game GAME=fieldjump PYTHON=python3`.
- Reusable helper opportunities: A shared endless-runner helper (spawn pacing, obstacle/coin lane patterns, simple runner collision) could speed up similar one-button platformers such as Floppy Canary once extraction is fixed.
- Backlog changes: Marked Field Jump partial with confirmed FCDB/BBS license/source/cart metadata and the `pxa` tooling blocker for exact parity.


## officehell — 2026-06-02

- Result: partial
- What translated cleanly: The documented control premise (choose left/right once, then time jumps while Jimbo auto-runs) maps cleanly to a small deterministic platformer state machine with level fixtures.
- What needed shims/manual rewrite: Full manual rewrite; exact PICO-8 Lua/API audit remains blocked because the cart code begins with newer `pxa` compression unsupported by the vendored `picotool` path.
- Asset/audio notes: Used the downloadable cart label as `cover.png`; map/gfx/sfx/music byte regions extract, but gameplay uses procedural office art and replacement SFX until Lua/assets can be decoded more completely.
- Verification: `python3 -m py_compile scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/officehell/officehell.py`; `make cart-game GAME=officehell PYTHON=python3`.
- Reusable helper opportunities: The one-way auto-runner platformer loop (preselect direction, coyote jump, fixture levels, hazard/exit checks) could help future Rat-on-the-Run-style puzzle-platformers.
- Backlog changes: Marked Office Hell partial with confirmed FCDB/BBS license/source/cart metadata and the `pxa` tooling blocker for exact parity.


## picoball — 2026-06-03

- Result: partial
- What translated cleanly: The published core rule — tennis/volleyball/squash/wallball with a point awarded after two bounces on one side — maps cleanly to a small Pyxel physics loop with a court divider, bounce counters, rally tracking, and handheld solo controls.
- What needed shims/manual rewrite: Full manual rewrite; exact PICO-8 Lua/API audit remains blocked because the live cart uses newer `pxa` compression unsupported by vendored `picotool`. Multiplayer, campaign opponents, hats, settings, and powerups are intentionally out of scope for this first solo/wallball pass.
- Asset/audio notes: Corrected the cart URL to the live BBS slug path (`https://www.lexaloffle.com/bbs/cposts/pi/pico_ball-5.p8.png`); used the downloadable cart label as `cover.png`; gameplay art and SFX are procedural replacements.
- Verification: `python3 -m py_compile scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/picoball/picoball.py`; `make cart-game GAME=picoball PYTHON=python3`.
- Reusable helper opportunities: A shared tiny sports-physics helper (body integration, ball/capsule collision, side/bounce scoring, simple CPU pursuit) could help future Pong/tennis/volleyball-style ports.
- Backlog changes: Marked PICO-BALL partial with confirmed FCDB/BBS metadata, corrected cart URL, BBS premise/control audit, and the `pxa` tooling blocker for exact parity.

## fieldjump — 2026-06-05

- Result: partial
- What translated cleanly: The BBS-confirmed levels premise maps to explicit stage goals, level-clear transitions, bonus scoring, a final win state, and a small HUD progress meter without changing the core runner loop.
- What needed shims/manual rewrite: Exact API/Lua parity is still blocked; cart version 43 has code bytes starting `00 70 78 61` (`pxa`), which vendored `picotool` still parses as empty Lua.
- Asset/audio notes: Reused existing cart-label cover; gameplay art/audio remain procedural replacements. Added a flying obstacle for later levels rather than extracted sprite data.
- Verification: `python3 -m py_compile scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/fieldjump/fieldjump.py`; `make cart-game GAME=fieldjump PYTHON=python3`.
- Reusable helper opportunities: Level-gated endless-runner helpers should include stage-distance goals, clear overlays, score bonuses, and obstacle tables keyed by level.
- Backlog changes: Kept Field Jump as partial; documented the measurable fidelity improvement and reconfirmed the `pxa` tooling blocker.

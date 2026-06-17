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

## justoneboss — 2026-06-17

- Result: partial
- What translated cleanly: The central arena premise maps cleanly to a host-tested grid core: step movement, magic tile collection, hazard damage, boss health, phase advancement, score, and win/loss states.
- What needed shims/manual rewrite: The full original PICO-8 entity/promise animation system, phase scripts, persistence, hard mode, sprite sheet, and soundtrack are not line-translated yet; the first PyxelPico pass uses a simplified phase-pattern generator around the same boss-loop shape.
- Asset/audio notes: Used a local source trail from `projects/picovibe/carts/pico8pixelbomb/justoneboss-pico8gomod/justonebossmod.p8`; added an original PyxelPico cover and simple in-code SFX rather than extracted sprite/audio data.
- Verification: `python3 -m unittest tests.test_justoneboss_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/justoneboss/justoneboss_core.py games/justoneboss/justoneboss.py`; `make cart-game GAME=justoneboss PYTHON=python3`.
- Reusable helper opportunities: Keep future top-100 action ports split into a pure gameplay core plus a Pyxel shell so movement/collision/progression rules are testable without launching Pyxel.
- Backlog changes: Added top-100 Just One Boss entry as partial with FCDB/BBS/license/source confirmation and current fidelity gaps.

## birdswithguns — 2026-06-17

- Result: partial
- What translated cleanly: The train-wagon shooter loop maps to a small host-tested core: D-pad movement, fire/weapon swap, enemy pursuit, ammo, health, wagon clearing, boss wagon, score, win, and loss states.
- What needed shims/manual rewrite: The original's procedural train map, mouse/keyboard aiming modes, bird roster, weapon roster, drops, particles, boss script, sprite sheet, and soundtrack are simplified in this first PyxelPico pass.
- Asset/audio notes: Added `scripts/pico8_cart_extract.py` and extracted the live BBS slug cart (`/bbs/cposts/bi/birdswithguns-5.p8.png`) for API audit; used original PyxelPico cover and simple in-code SFX rather than extracted sprite/audio data.
- Verification: `python3 -m unittest tests.test_birdswithguns_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/justoneboss/justoneboss_core.py games/justoneboss/justoneboss.py games/birdswithguns/birdswithguns_core.py games/birdswithguns/birdswithguns.py`; `make cart-game GAME=birdswithguns PYTHON=python3`.
- Reusable helper opportunities: Slug cart URL derivation from FCDB thumbnail paths is needed for newer BBS carts; keep `pico8_cart_extract.py` available for future candidate API audits.
- Backlog changes: Added top-100 Birds With Guns entry as partial with FCDB/BBS/license/cart confirmation and current fidelity gaps.

## highstakes — 2026-06-17

- Result: partial
- What translated cleanly: The core 3x3 vampire-card deduction round maps cleanly to a host-tested model: unique 2-10 card deal, one vampire, one visible safe card, safe flips, hint token marks, stab/pass outcomes, and payout.
- What needed shims/manual rewrite: The original blood economy, unlock ladder, chained score mode, animated chip/card UX, custom sprite generation, and soundtrack are simplified in this first PyxelPico pass.
- Asset/audio notes: Extracted the live BBS slug cart (`/bbs/cposts/hi/highstakes-2.p8.png`) with `scripts/pico8_cart_extract.py`; added an original PyxelPico cover and simple in-code SFX rather than extracted sprite/audio data.
- Verification: `python3 -m unittest tests.test_highstakes_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/highstakes/highstakes_core.py games/highstakes/highstakes.py`; `make cart-game GAME=highstakes PYTHON=python3`.
- Reusable helper opportunities: Deduction/card ports should keep board rules pure and render/control state separate so hint/pass/stab scoring remains easy to test.
- Backlog changes: Added top-100 High Stakes entry as partial with FCDB/BBS/license/cart confirmation and current fidelity gaps.

## buns — 2026-06-17

- Result: partial
- What translated cleanly: The survivor loop maps cleanly to a host-tested core: bounded D-pad movement, enemy spawn/chase, automatic nearest-target firing, gem collection, XP thresholds, upgrade selection, damage iframes, boss timer, win, and loss states.
- What needed shims/manual rewrite: The original's broader enemy/weapon/upgrade tables, sprite sheet, particles, soundtrack, and exact pacing are simplified in this first PyxelPico pass.
- Asset/audio notes: Extracted the live BBS slug cart (`/bbs/cposts/bu/bunnysurvivor-9.p8.png`) with `scripts/pico8_cart_extract.py`; added an original PyxelPico cover and simple in-code SFX rather than extracted sprite/audio data.
- Verification: `python3 -m unittest tests.test_buns_core`; `python3 -m unittest tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/buns/buns_core.py games/buns/buns.py`; `make cart-game GAME=buns PYTHON=python3`.
- Reusable helper opportunities: Survivor-style ports should keep target selection, spawn pacing, XP thresholds, and upgrade effects in pure cores so pacing can be tested without launching Pyxel.
- Backlog changes: Added top-100 Buns entry as partial with FCDB/BBS/license/cart confirmation and current fidelity gaps.

## porklike — 2026-06-17

- Result: partial
- What translated cleanly: The turn-based dungeon premise maps cleanly to a pure grid core: deterministic room/corridor generation, wall blocking, bump combat, food pickup, enemy turns, health, score, level exits, win, and loss states.
- What needed shims/manual rewrite: Exact original Lua/API parity is blocked because FCDB's numeric cart URL 404s and the live BBS slug cart currently extracts as empty Lua with the local tool despite an old `:c:` code header; this first pass uses a compact procedural roguelike adaptation.
- Asset/audio notes: Used the live BBS slug cart URL (`/bbs/cposts/po/porklike-2.p8.png`) for cart-shell inspection; added an original PyxelPico cover and simple in-code SFX rather than extracted sprite/audio data.
- Verification: `python3 -m unittest tests.test_porklike_core`; `python3 -m unittest tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/porklike/porklike_core.py games/porklike/porklike.py`; `make cart-game GAME=porklike PYTHON=python3`.
- Reusable helper opportunities: Roguelike ports benefit from a pure grid/entity core and fixture-map test hook so enemy movement and item/exit rules are easy to verify.
- Backlog changes: Added top-100 Porklike entry as partial with FCDB/BBS/license/cart confirmation and the cart extraction blocker.

## picoware — 2026-06-17

- Result: partial
- What translated cleanly: The WarioWare-like shell maps cleanly to a pure rush core: round starts, timed prompts, D-pad/A/B input checks, pass/fail result delay, score, lives, speed pressure, and game-over transition.
- What needed shims/manual rewrite: The original has 68 microgames across collaboration subcarts, saved progress, menu/list states, and bespoke minigame implementations; this first pass is a compact microgame-rush subset rather than full subcart parity.
- Asset/audio notes: Extracted the live BBS slug cart (`/bbs/cposts/pi/picoware-20.p8.png`) with `scripts/pico8_cart_extract.py`; added an original PyxelPico cover and simple in-code SFX rather than extracted sprite/audio data.
- Verification: `python3 -m unittest tests.test_picoware_core`; `python3 -m unittest tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/picoware/picoware_core.py games/picoware/picoware.py`; `make cart-game GAME=picoware PYTHON=python3`.
- Reusable helper opportunities: Microgame-collection ports should separate prompt/timer/result scoring from individual visual sketches so new microgames can be added without retesting the whole shell manually.
- Backlog changes: Added top-100 PICOWARE entry as partial with FCDB/BBS/license/cart confirmation and current fidelity gaps.

## maichanssweetbuns — 2026-06-17

- Result: partial
- What translated cleanly: The bakery order premise maps cleanly to a pure sequence core: generated orders, tray matching, wrong-bun penalties, serving, patience, timer pressure, score, day progression, and game-over transition.
- What needed shims/manual rewrite: Exact original Lua/API parity is blocked because FCDB's stored cart URL 404s and the BBS-discovered live cart `/bbs/cposts/5/56576.p8.png` extracts as empty Lua with the current local tool; this first pass is a compact order-matching adaptation.
- Asset/audio notes: Used the BBS thread to correct the live cart URL; added an original PyxelPico cover and simple in-code SFX rather than extracted sprite/audio data.
- Verification: `python3 -m unittest tests.test_maichanssweetbuns_core`; `python3 -m unittest tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_maichanssweetbuns_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/maichanssweetbuns/maichanssweetbuns_core.py games/maichanssweetbuns/maichanssweetbuns.py`; `make cart-game GAME=maichanssweetbuns PYTHON=python3`.
- Reusable helper opportunities: Recipe/order ports should keep sequence validation and penalties pure; shells can then vary ingredient controls and visuals safely.
- Backlog changes: Added top-100 Mai-Chan's Sweet Buns entry as partial with FCDB/BBS/license confirmation, corrected live cart URL, and current fidelity gaps.

## xzero — 2026-06-17

- Result: partial
- What translated cleanly: The platform-shooter premise maps cleanly to a pure action core: horizontal acceleration, jump/land physics, directional aiming, shots, enemy HP, contact damage, pickups, zone exits, win, and loss states.
- What needed shims/manual rewrite: Exact original Lua/API parity is blocked because the live BBS slug cart extracts as empty Lua with the current local tool; this first pass is a compact platform-shooter adaptation based on BBS-confirmed jump/shoot/platforming behavior.
- Asset/audio notes: Used the BBS thread and live cart path `/bbs/cposts/xz/xzero-3.p8.png` for source confirmation; added an original PyxelPico cover and simple in-code SFX rather than extracted sprite/audio data.
- Verification: `python3 -m unittest tests.test_xzero_core`; `python3 -m unittest tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_maichanssweetbuns_core tests.test_xzero_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/xzero/xzero_core.py games/xzero/xzero.py`; `make cart-game GAME=xzero PYTHON=python3`.
- Reusable helper opportunities: Platform-shooter ports need pure physics/combat tests before tuning visuals; keep cooldown, iframes, pickups, and zone progression outside Pyxel rendering.
- Backlog changes: Added top-100 X-Zero entry as partial with FCDB/BBS/license/cart confirmation and current fidelity gaps.

## picoworldrace — 2026-06-17

- Result: partial
- What translated cleanly: The racing loop maps cleanly to a pure core: acceleration, steering, drift turn/speed tradeoff, off-track slowdown, progress, lap completion, token crossing, opponent progress, standing, score, and finish state.
- What needed shims/manual rewrite: The original's 8 themed tracks, campaign unlocks, custom/random track generator, profile saves, exact sprite rendering, music, and tuned car physics are simplified in this first pass.
- Asset/audio notes: Extracted the live BBS slug cart (`/bbs/cposts/pp/ppwr-5.p8.png`) with `scripts/pico8_cart_extract.py`; BBS thread also links upstream source at `https://github.com/PAK9/PicoWorldRace`. Added an original PyxelPico cover and simple in-code SFX rather than extracted sprite/audio data.
- Verification: `python3 -m unittest tests.test_picoworldrace_core`; `python3 -m unittest tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/picoworldrace/picoworldrace_core.py games/picoworldrace/picoworldrace.py`; `make cart-game GAME=picoworldrace PYTHON=python3`.
- Reusable helper opportunities: Racing ports should keep progress/token/lap/opponent math pure; rendering can then experiment with road perspective independently.
- Backlog changes: Added top-100 Pico World Race entry as partial with FCDB/BBS/license/cart/source confirmation and current fidelity gaps.

## combopool — 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described merge-pool loop maps cleanly to a pure core: aim rotation, shooting, wall rebounds, same-color merge upgrades, score from merge/rebound/combo, life pressure from too many/dark balls, and win/loss states.
- What needed shims/manual rewrite: Local extraction of the live cart returns only shallow output with no useful API surface, so exact physics, difficulty modes, mouse/touch aiming, sprite effects, color progression, and sudden-death behavior are simplified in this first pass.
- Asset/audio notes: Used the BBS thread's detailed gameplay notes plus live cart path `/bbs/cposts/co/combopool-0.p8.png`; added an original PyxelPico cover and simple in-code SFX rather than extracted sprite/audio data.
- Verification: `python3 -m unittest tests.test_combopool_core`; `python3 -m unittest tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/combopool/combopool_core.py games/combopool/combopool.py`; `make cart-game GAME=combopool PYTHON=python3`.
- Reusable helper opportunities: Physics-puzzle ports need deterministic collision/merge tests and should separate visual polish from scoring/life-pressure rules.
- Backlog changes: Added top-100 Combo Pool entry as partial with FCDB/BBS/license/cart confirmation and current fidelity gaps.

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

## intoruins — 2026-06-17

- Result: partial
- What translated cleanly: The BBS-stated core goal and genre (turn-based roguelike, reach depth 16, retrieve the Wings of Yendor) map cleanly to a deterministic host-tested dungeon core with movement, bump combat, visibility/exploration, enemy turns, status timers, item pickup, descent, win, and loss states.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; the extracted PICO-8 Lua/API confirmed the rendering/status/fog/audio shape, but the original's dense Brogue-like interaction matrix is far larger than a first pass.
- Asset/audio notes: The live BBS slug cart (`https://www.lexaloffle.com/bbs/cposts/in/intoruins-7.p8.png`) extracts usable Lua/API with `scripts/pico8_cart_extract.py`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the ruins/Wings premise.
- Verification: `python3 -m unittest tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/intoruins/intoruins_core.py games/intoruins/intoruins.py games/toastarling/toastarling_core.py games/toastarling/toastarling.py`; `make cart-game GAME=intoruins PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: A shared turn-based dungeon helper could consolidate grid visibility, status ticking, bump combat, item pickup, enemy pursuit/ranged line checks, and staircase/depth progression across roguelike ports.
- Backlog changes: Added rank 32 Into Ruins as partial with confirmed FCDB/BBS/license/cart metadata, upstream GitHub source trail, API extraction result, and current first-playable fidelity gaps.

## toastarling — 2026-06-17

- Result: partial
- What translated cleanly: The extracted platformer movement model maps cleanly to a host-tested core with acceleration/friction, buffered/coyote jump, glide/fast-fall, collectibles, keys, doors, switches, checkpoint respawn, hazards, and goal clear.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; authored room maps, camera transitions, teleport/portal systems, merchants, cartdata persistence, and detailed animation/music are intentionally outside this first playable pass.
- Asset/audio notes: The live BBS slug cart (`https://www.lexaloffle.com/bbs/cposts/to/to_a_starling-0.p8.png`) extracts usable Lua/API with `scripts/pico8_cart_extract.py`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the bird/platforming premise.
- Verification: `python3 -m unittest tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/intoruins/intoruins_core.py games/intoruins/intoruins.py games/toastarling/toastarling_core.py games/toastarling/toastarling.py`; `make cart-game GAME=toastarling PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Platformer ports would benefit from a shared pure core for acceleration/friction, coyote/buffered jump, tile collision, collectibles, switch/door state, checkpoint respawn, and camera-friendly room fixtures.
- Backlog changes: Added rank 35 To a Starling as partial with confirmed FCDB/BBS/license/cart metadata, API extraction result, and current first-playable fidelity gaps.

## woodworm — 2026-06-17

- Result: partial
- What translated cleanly: The extracted movement loop and BBS comments map cleanly to a host-tested Snakebird-like core: a fixed-length worm inserts a new head per move, blocks immediate reverse, eats wood tiles, supports undo, resolves gravity for blocks/worm, and clears on reaching the goal.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; authored puzzle list, level-select save progress, custom font, jar/cabinet presentation, falling animation timing, and cake ending are outside this first playable pass.
- Asset/audio notes: The live BBS slug cart (`https://www.lexaloffle.com/bbs/cposts/wo/woodworm-0.p8.png`) extracts usable Lua/API with `scripts/pico8_cart_extract.py`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the wood/cake/worm premise.
- Verification: `python3 -m unittest tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/intoruins/intoruins_core.py games/intoruins/intoruins.py games/toastarling/toastarling_core.py games/toastarling/toastarling.py games/woodworm/woodworm_core.py games/woodworm/woodworm.py`; `make cart-game GAME=woodworm PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Puzzle ports would benefit from shared fixture parsing, undo snapshots, grid gravity, and move-buffer helpers.
- Backlog changes: Added rank 36 Woodworm as partial with confirmed FCDB/BBS/license/cart metadata, API extraction result, and current first-playable fidelity gaps.

## bas — 2026-06-17

- Result: partial
- What translated cleanly: The extracted game loop and BBS description map cleanly to a host-tested endless wall-jump core: jump left/right, retarget mid-air, predict and collide with saws, chase the player with a rising trap, score on successful jumps, update highscore on death, and restart.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; polished easing curves, transition scenes, sprite animations, music, exact column/saw pacing, and cartdata persistence are outside this first playable pass.
- Asset/audio notes: The live BBS slug cart (`https://www.lexaloffle.com/bbs/cposts/ba/bas-9.p8.png`) extracts usable Lua/API with `scripts/pico8_cart_extract.py`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the wall-jump/saw/trap premise.
- Verification: `python3 -m unittest tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/bas/bas_core.py games/bas/bas.py games/intoruins/intoruins_core.py games/intoruins/intoruins.py games/toastarling/toastarling_core.py games/toastarling/toastarling.py games/woodworm/woodworm_core.py games/woodworm/woodworm.py`; `make cart-game GAME=bas PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Endless one-button/highscore ports could share obstacle spawning, local highscore state, and compact action-arc cores.
- Backlog changes: Added rank 37 BAS as partial with confirmed FCDB/BBS/license/cart metadata, author-owned demake note, GitHub source trail, API extraction result, and current first-playable fidelity gaps.

## ufoswamp — 2026-06-17

- Result: partial
- What translated cleanly: The extracted Lua and BBS premise map cleanly to a host-tested platform-adventure core: D-pad movement, A jump, swamp-water buoyancy, score and zapper pickups, EMP stun, portal teleport, grapple pull, and a sustained EMP zap to disable the cannon.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; authored world layout, friend dialogue timing, cinematic title/ending transitions, exact water/sinking behavior, palette animation, sprite animation, SFX/music, and map-driven progression are outside this first playable pass.
- Asset/audio notes: FCDB's numeric cart URL 404s, but the BBS thread exposes the live cart `https://www.lexaloffle.com/bbs/cposts/uf/ufo-0.p8.png`, which extracts usable Lua/API with `scripts/pico8_cart_extract.py`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the UFO/swamp/zapper premise.
- Verification: `python3 -m unittest tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/bas/bas_core.py games/bas/bas.py games/intoruins/intoruins_core.py games/intoruins/intoruins.py games/toastarling/toastarling_core.py games/toastarling/toastarling.py games/ufoswamp/ufoswamp_core.py games/ufoswamp/ufoswamp.py games/woodworm/woodworm_core.py games/woodworm/woodworm.py`; `make cart-game GAME=ufoswamp PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Platform-adventure ports could share tile-fixture parsing, coyote/jump movement, pickup unlock progression, line-of-sight action tools, and simple portal/grapple primitives.
- Backlog changes: Added rank 41 UFO Swamp Odyssey as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, API extraction result, and current first-playable fidelity gaps.

## picoracer2048 — 2026-06-17

- Result: partial
- What translated cleanly: The BBS/thread-described race model maps cleanly to a host-tested core with speed classes, acceleration, braking, boost pads, curve drift, brake-assisted steering, off-track wall slowdown, three-lap finish timing, and AI race pressure.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; the live cart downloads but local extraction returns empty Lua/API, and the BBS source snippet depends on browser-side Lexaloffle cart tooling. Exact 8 tracks, ghost data, AI racers, track editor/storage, vector effects, music, and handling feel are outside this first playable pass.
- Asset/audio notes: FCDB's numeric cart URL 404s, but the BBS thread exposes the live cart `https://www.lexaloffle.com/bbs/cposts/1/16305.p8.png`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the vector-racer premise.
- Verification: `python3 -m unittest tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_picoracer2048_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/bas/bas_core.py games/bas/bas.py games/intoruins/intoruins_core.py games/intoruins/intoruins.py games/picoracer2048/picoracer2048_core.py games/picoracer2048/picoracer2048.py games/toastarling/toastarling_core.py games/toastarling/toastarling.py games/ufoswamp/ufoswamp_core.py games/ufoswamp/ufoswamp.py games/woodworm/woodworm_core.py games/woodworm/woodworm.py`; `make cart-game GAME=picoracer2048 PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Racing ports could share track-section expansion, lap wrapping, lane/width collision, boost pads, brake-assisted steering, and simple rival progress logic.
- Backlog changes: Added rank 42 PICORACER-2048 as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, source-extraction blocker, and current first-playable fidelity gaps.

## airdelivery — 2026-06-17

- Result: partial
- What translated cleanly: The BBS-documented controls and premise map cleanly to a host-tested platform-delivery core: D-pad movement/climbing, coyote jump, B interaction, glider reward, letter/package collection, recipient delivery, drill-secret passage, hazard respawn, and final airship completion after deliveries.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; local extraction sees title/prologue, palette setup, sprite/string data, and a small rendering API surface but not the full gameplay implementation. The original dense world, all 9 packages, NPC dialogue, exact glider handling, secrets, music, sprite animation, death transition, and ending screen are outside this first playable pass.
- Asset/audio notes: FCDB's numeric cart URL 404s, but the BBS thread exposes the live cart `https://www.lexaloffle.com/bbs/cposts/ai/air_delivery_1-3.p8.png`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the sky-island delivery premise.
- Verification: `python3 -m unittest tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_picoracer2048_core tests.test_airdelivery_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/airdelivery/airdelivery_core.py games/airdelivery/airdelivery.py games/bas/bas_core.py games/bas/bas.py games/intoruins/intoruins_core.py games/intoruins/intoruins.py games/picoracer2048/picoracer2048_core.py games/picoracer2048/picoracer2048.py games/toastarling/toastarling_core.py games/toastarling/toastarling.py games/ufoswamp/ufoswamp_core.py games/ufoswamp/ufoswamp.py games/woodworm/woodworm_core.py games/woodworm/woodworm.py`; `make cart-game GAME=airdelivery PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Platform-metroidvania ports could share tile fixtures, ladder climb, coyote/buffered jump, glide fall caps, proximity interaction, delivery/reward progression, and checkpoint/hazard respawn.
- Backlog changes: Added rank 44 Air Delivery as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, partial extraction result, BBS controls/changelog, and current first-playable fidelity gaps.

## demoncastle — 2026-06-17

- Result: blocked-ip-risk
- Evidence: FCDB tags include `castlevania`; the BBS description says "Demon Castle is a Castlevania-style game for PICO-8"; controls center on a whip; comments compare the game directly to multiple Castlevania entries. The policy blocks commercial-IP demakes/mods or close derivative recreations without an explicit approved rights chain.
- Tooling notes: FCDB numeric cart URL 404s; the BBS thread exposes the live cart `https://www.lexaloffle.com/bbs/cposts/de/demon_castle-1.p8.png`, but no port was attempted because the IP-risk block is sufficient.
- Backlog changes: Added rank 45 Demon Castle as blocked and updated `scripts/pico8_top100_status.py` so `castlevania` tags classify as derivative-IP risk.

## marballs2 - 2026-06-17

- Result: partial
- What translated cleanly: The BBS description and extracted level table map cleanly to a host-tested rolling-ball core: D-pad acceleration/friction, jump pads, orb collection, orb-gated goal, wall-bounce momentum, timer/medal pressure, restart, and optional 45-degree controls.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; local extraction yields title data and level metadata but no useful API scan. Official level geometry, custom level pack support, exact wall/corner collision, level select, save data, music, intro, and ace routing are outside this first playable pass.
- Asset/audio notes: FCDB's numeric cart URL 404s, but the BBS thread exposes the live cart `https://www.lexaloffle.com/bbs/cposts/ma/marballs_2-0.p8.png`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the marble/orb/jump-pad premise.
- Verification: `python3 -m unittest tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_picoracer2048_core tests.test_airdelivery_core tests.test_marballs2_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/airdelivery/airdelivery_core.py games/airdelivery/airdelivery.py games/bas/bas_core.py games/bas/bas.py games/intoruins/intoruins_core.py games/intoruins/intoruins.py games/marballs2/marballs2_core.py games/marballs2/marballs2.py games/picoracer2048/picoracer2048_core.py games/picoracer2048/picoracer2048.py games/toastarling/toastarling_core.py games/toastarling/toastarling.py games/ufoswamp/ufoswamp_core.py games/ufoswamp/ufoswamp.py games/woodworm/woodworm_core.py games/woodworm/woodworm.py`; `make cart-game GAME=marballs2 PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Rolling/puzzle-action ports could share axis transforms, acceleration/friction speed caps, wall bounce, collectible-gated exits, timer medals, and simple fixture-driven levels.
- Backlog changes: Added rank 46 Marballs 2 as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, partial extraction result, BBS controls/custom-level notes, and current first-playable fidelity gaps.

## freezingknights - 2026-06-17

- Result: partial
- What translated cleanly: The BBS thread and upstream source docs map cleanly to a host-tested core for snowy path selection, two-knight party stats, turn-based attacks, timed defense, potions, gold rewards, rest/safe-zone recovery, upgrades, and party-wipe fallback.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; the original is a 14-cart RPG with many encounters, authored maps, menus, two-player-specific controls, hard mode, persistence, soundtrack, custom sprites, and ending flow. This pass intentionally avoids branded third-party RPG names/assets and uses generic knight/mountain/enemy presentation.
- Asset/audio notes: FCDB's numeric cart URL is stale, but the BBS thread exposes the live cart `https://www.lexaloffle.com/bbs/cposts/fr/freezing_knights-9.p8.png`; upstream source is available at `https://github.com/tinyevilwizard/FreezingKnights` under CC BY-NC-SA 4.0. Gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the snowy two-knight premise.
- Verification: `python3 -m unittest tests.test_freezingknights_core tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_picoracer2048_core tests.test_airdelivery_core tests.test_marballs2_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/freezingknights/freezingknights_core.py games/freezingknights/freezingknights.py games/airdelivery/airdelivery_core.py games/airdelivery/airdelivery.py games/bas/bas_core.py games/bas/bas.py games/intoruins/intoruins_core.py games/intoruins/intoruins.py games/marballs2/marballs2_core.py games/marballs2/marballs2.py games/picoracer2048/picoracer2048_core.py games/picoracer2048/picoracer2048.py games/toastarling/toastarling_core.py games/toastarling/toastarling.py games/ufoswamp/ufoswamp_core.py games/ufoswamp/ufoswamp.py games/woodworm/woodworm_core.py games/woodworm/woodworm.py`; `make cart-game GAME=freezingknights PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Turn-based RPG ports could share party/enemy dataclasses, menu cursors, timed-defense meters, rest/safe-zone state, upgrade costs, and host-testable battle progression helpers.
- Backlog changes: Added rank 48 Freezing Knights as partial with confirmed FCDB/BBS/license metadata, live cart URL, GitHub source trail, inspiration/IP-risk note, and current first-playable fidelity gaps.

## lostnight - 2026-06-17

- Result: partial
- What translated cleanly: The extracted Lua/API and BBS evidence map cleanly to a host-tested room RPG/shooter core with room transitions, encounter triggers, bullet-dodging battle-box movement, player shots, HP/tea healing, candy rewards, shop upgrades, cleared-room tracking, and dawn unlock.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; original authored rooms, enemy/bullet patterns, dialogue, music, persistence, visual effects, and exact shop/menu presentation are outside this first playable pass. FCDB/BBS tags include `earthbound`, so the port intentionally uses generic night/candy/shadow presentation and no third-party branded names/assets.
- Asset/audio notes: The live BBS cart `https://www.lexaloffle.com/bbs/cposts/th/the_lost_night-6.p8.png` extracts usable Lua/API with `scripts/pico8_cart_extract.py`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the night/shooter premise.
- Verification: `python3 -m unittest tests.test_lostnight_core tests.test_freezingknights_core tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_picoracer2048_core tests.test_airdelivery_core tests.test_marballs2_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/lostnight/lostnight_core.py games/lostnight/lostnight.py games/freezingknights/freezingknights_core.py games/freezingknights/freezingknights.py games/airdelivery/airdelivery_core.py games/airdelivery/airdelivery.py games/bas/bas_core.py games/bas/bas.py games/intoruins/intoruins_core.py games/intoruins/intoruins.py games/marballs2/marballs2_core.py games/marballs2/marballs2.py games/picoracer2048/picoracer2048_core.py games/picoracer2048/picoracer2048.py games/toastarling/toastarling_core.py games/toastarling/toastarling.py games/ufoswamp/ufoswamp_core.py games/ufoswamp/ufoswamp.py games/woodworm/woodworm_core.py games/woodworm/woodworm.py`; `make cart-game GAME=lostnight PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Battle-box ports could share bounded player movement, hostile/friendly bullet lists, HP/item economy, room-clear progression, and compact shop upgrade state.
- Backlog changes: Added rank 49 The Lost Night Release as partial with confirmed FCDB/BBS/license metadata, live cart URL, API extraction result, IP-vibe caveat, and current first-playable fidelity gaps.

## nanoman - 2026-06-17

- Result: blocked-ip-risk
- Evidence: FCDB tags include `megaman`; the BBS description says Nanoman is "a fan game heavily inspired by the early Mega Man series" and tells Mega Man fans they should feel at home; comments compare the game directly to Mega Man. This is too close to a commercial-IP fan game for the current migration policy.
- Tooling notes: FCDB/BBS license metadata is CC BY-NC-SA 4.0, but that does not clear third-party IP rights. The numeric cart URL currently returns HTML/stale content, but the IP-risk block is already sufficient.
- Backlog changes: Added rank 51 Nanoman as blocked and updated `scripts/pico8_top100_status.py` so `megaman`, `mega man`, and `rockman` terms classify as derivative-IP risk.

## picocheckmate - 2026-06-17

- Result: partial
- What translated cleanly: Classic chess rules map cleanly to a host-tested core: legal piece movement, king-safety filtering, check/checkmate/stalemate state, castling, en passant, promotion, and simple capture-biased AI move selection.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; local extraction returns empty Lua/API for the live cart. Original animation juice, exact AI evaluation/search depth, two-human mode, soundtrack, sprite art, and full menu presentation are outside this first playable pass.
- Asset/audio notes: The live BBS cart is `https://www.lexaloffle.com/bbs/cposts/5/54038.p8.png`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the chess-board premise.
- Verification: `python3 -m unittest tests.test_picocheckmate_core tests.test_lostnight_core tests.test_freezingknights_core tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_picoracer2048_core tests.test_airdelivery_core tests.test_marballs2_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/picocheckmate/picocheckmate_core.py games/picocheckmate/picocheckmate.py games/lostnight/lostnight_core.py games/lostnight/lostnight.py games/freezingknights/freezingknights_core.py games/freezingknights/freezingknights.py games/airdelivery/airdelivery_core.py games/airdelivery/airdelivery.py games/bas/bas_core.py games/bas/bas.py games/intoruins/intoruins_core.py games/intoruins/intoruins.py games/marballs2/marballs2_core.py games/marballs2/marballs2.py games/picoracer2048/picoracer2048_core.py games/picoracer2048/picoracer2048.py games/toastarling/toastarling_core.py games/toastarling/toastarling.py games/ufoswamp/ufoswamp_core.py games/ufoswamp/ufoswamp.py games/woodworm/woodworm_core.py games/woodworm/woodworm.py`; `make cart-game GAME=picocheckmate PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Board-game ports could share cursor selection, legal-move highlighting, AI delay/turn handoff, and compact status panels around a pure rules core.
- Backlog changes: Added rank 52 Pico Checkmate as partial with confirmed FCDB/BBS/license metadata, live cart URL, BBS rule notes, extraction blocker, and current first-playable fidelity gaps.

## littledragon - 2026-06-17

- Result: partial
- What translated cleanly: The BBS premise and comments map cleanly to a host-tested platform-adventure core with running, jump/double-jump, fireballs, enemy hits, egg rescue, checkpoint respawn, hazards, boss gate, and clear state.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; local extraction returns empty Lua/API for the live cart. The authored metroidvania map, original boss patterns, challenge mode, exact enemy movement, checkpoint placement, music, sprite art, and ending surprise are outside this first playable pass.
- Asset/audio notes: The live BBS cart is `https://www.lexaloffle.com/bbs/cposts/5/53895.p8.png`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the dragon/egg rescue premise.
- Verification: `python3 -m unittest tests.test_littledragon_core tests.test_picocheckmate_core tests.test_lostnight_core tests.test_freezingknights_core tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_picoracer2048_core tests.test_airdelivery_core tests.test_marballs2_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/littledragon/littledragon_core.py games/littledragon/littledragon.py games/picocheckmate/picocheckmate_core.py games/picocheckmate/picocheckmate.py games/lostnight/lostnight_core.py games/lostnight/lostnight.py games/freezingknights/freezingknights_core.py games/freezingknights/freezingknights.py games/airdelivery/airdelivery_core.py games/airdelivery/airdelivery.py games/bas/bas_core.py games/bas/bas.py games/intoruins/intoruins_core.py games/intoruins/intoruins.py games/marballs2/marballs2_core.py games/marballs2/marballs2.py games/picoracer2048/picoracer2048_core.py games/picoracer2048/picoracer2048.py games/toastarling/toastarling_core.py games/toastarling/toastarling.py games/ufoswamp/ufoswamp_core.py games/ufoswamp/ufoswamp.py games/woodworm/woodworm_core.py games/woodworm/woodworm.py`; `make cart-game GAME=littledragon PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Platform-adventure ports could share movement/double-jump, projectile hit checks, checkpoint respawn, collectible gates, and compact boss-health loops.
- Backlog changes: Added rank 55 Little Dragon Adventure as partial with confirmed FCDB/BBS/license metadata, live cart URL, BBS premise/control/combat notes, extraction blocker, and current first-playable fidelity gaps.

## trialsorcerer - 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described dungeon-FPS loop maps cleanly to a host-tested core: deterministic dungeon setup, turn/forward/strafe movement, staff line-of-sight shots, monster defeat, loot, key pickup, locked doors, crystal staff upgrades, level exits, and final boss clear state.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; source extraction works from the live slug cart, but the original raycaster, procedural room generator, GUI/menu system, mouse/control options, enemy variety, exact layouts, music, and renderer tricks are too large for a first playable pass.
- Asset/audio notes: FCDB's numeric cart URL 404s, but the BBS thread exposes `https://www.lexaloffle.com/bbs/cposts/mo/mot_sorcerer-11.p8.png`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the staff/dungeon premise.
- Verification: `python3 -m unittest tests.test_trialsorcerer_core tests.test_littledragon_core tests.test_picocheckmate_core tests.test_lostnight_core tests.test_freezingknights_core tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_picoracer2048_core tests.test_airdelivery_core tests.test_marballs2_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/trialsorcerer/trialsorcerer_core.py games/trialsorcerer/trialsorcerer.py games/littledragon/littledragon_core.py games/littledragon/littledragon.py games/picocheckmate/picocheckmate_core.py games/picocheckmate/picocheckmate.py games/lostnight/lostnight_core.py games/lostnight/lostnight.py games/freezingknights/freezingknights_core.py games/freezingknights/freezingknights.py games/airdelivery/airdelivery_core.py games/airdelivery/airdelivery.py games/bas/bas_core.py games/bas/bas.py games/intoruins/intoruins_core.py games/intoruins/intoruins.py games/marballs2/marballs2_core.py games/marballs2/marballs2.py games/picoracer2048/picoracer2048_core.py games/picoracer2048/picoracer2048.py games/toastarling/toastarling_core.py games/toastarling/toastarling.py games/ufoswamp/ufoswamp_core.py games/ufoswamp/ufoswamp.py games/woodworm/woodworm_core.py games/woodworm/woodworm.py`; `make cart-game GAME=trialsorcerer PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: First-person dungeon ports could share tile-grid cardinal movement, held-strafe semantics, simple line-of-sight combat, pickup/door progression, minimap rendering, and pseudo-ray wall panel drawing.
- Backlog changes: Added rank 59 Trial of the Sorcerer as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, source extraction result, BBS controls/mechanics, inspiration/IP-risk note, and current first-playable fidelity gaps.

## motionrec - 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described action-puzzle concept maps cleanly to a host-tested platformer core with movement, jump/landing, start/stop recording, stored relative motion paths, reusable forward playback, reverse playback, clone/switch pressure, goal unlock, clear state, and reset after bad recordings.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; the live slug cart extracts source and confirms the Advanced Micro Platformer Starter Kit attribution, but exact level layouts, puzzle timing, softlock prevention, visual mode colors, animation, music, speedrun route polish, and commercial release presentation are outside this first playable pass.
- Asset/audio notes: FCDB's numeric cart URL 404s, but the BBS thread exposes `https://www.lexaloffle.com/bbs/cposts/mo/motionrec-3.p8.png`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the record/replay premise.
- Verification: `python3 -m unittest tests.test_motionrec_core tests.test_trialsorcerer_core tests.test_littledragon_core tests.test_picocheckmate_core tests.test_lostnight_core tests.test_freezingknights_core tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_picoracer2048_core tests.test_airdelivery_core tests.test_marballs2_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/motionrec/motionrec_core.py games/motionrec/motionrec.py games/trialsorcerer/trialsorcerer_core.py games/trialsorcerer/trialsorcerer.py games/littledragon/littledragon_core.py games/littledragon/littledragon.py games/picocheckmate/picocheckmate_core.py games/picocheckmate/picocheckmate.py games/lostnight/lostnight_core.py games/lostnight/lostnight.py games/freezingknights/freezingknights_core.py games/freezingknights/freezingknights.py games/airdelivery/airdelivery_core.py games/airdelivery/airdelivery.py games/bas/bas_core.py games/bas/bas.py games/intoruins/intoruins_core.py games/intoruins/intoruins.py games/marballs2/marballs2_core.py games/marballs2/marballs2.py games/picoracer2048/picoracer2048_core.py games/picoracer2048/picoracer2048.py games/toastarling/toastarling_core.py games/toastarling/toastarling.py games/ufoswamp/ufoswamp_core.py games/ufoswamp/ufoswamp.py games/woodworm/woodworm_core.py games/woodworm/woodworm.py`; `make cart-game GAME=motionrec PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Time/ghost-action ports could share relative path recording, replay/reverse playback, clone collision/switch pressure, bad-recording reset, and ghost path visualization.
- Backlog changes: Added rank 60 MOTION.REC as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, source extraction result, BBS controls/mechanics, Steam/itch/template context, and current first-playable fidelity gaps.

## pcraft - 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described island survival loop maps cleanly to a host-tested core with seeded resources, gathering trees/stone/fiber, workbench recipes, axe wood-yield progression, sword-gated cave exploration, crystal reward, boat recipe, shore escape, and restart.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; FCDB's numeric URL 404s and the live cart downloads but local extraction returns no usable Lua/API text. Original procedural map generation, full inventory/menu system, many items, hunger/stamina/combat, cave/boss sequence, Deluxe multicartridge additions, music, and exact sprite work are outside this first playable pass.
- Asset/audio notes: The live BBS cart is `https://www.lexaloffle.com/bbs/cposts/2/24981.p8.png`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the island/workbench/boat premise. The thread cites Minicraft inspiration, so the port uses generic island survival presentation and no external release assets.
- Verification: `python3 -m unittest tests.test_pcraft_core tests.test_motionrec_core tests.test_trialsorcerer_core tests.test_littledragon_core tests.test_picocheckmate_core tests.test_lostnight_core tests.test_freezingknights_core tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_picoracer2048_core tests.test_airdelivery_core tests.test_marballs2_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/pcraft/pcraft_core.py games/pcraft/pcraft.py games/motionrec/motionrec_core.py games/motionrec/motionrec.py games/trialsorcerer/trialsorcerer_core.py games/trialsorcerer/trialsorcerer.py games/littledragon/littledragon_core.py games/littledragon/littledragon.py games/picocheckmate/picocheckmate_core.py games/picocheckmate/picocheckmate.py games/lostnight/lostnight_core.py games/lostnight/lostnight.py games/freezingknights/freezingknights_core.py games/freezingknights/freezingknights.py games/airdelivery/airdelivery_core.py games/airdelivery/airdelivery.py games/bas/bas_core.py games/bas/bas.py games/intoruins/intoruins_core.py games/intoruins/intoruins.py games/marballs2/marballs2_core.py games/marballs2/marballs2.py games/picoracer2048/picoracer2048_core.py games/picoracer2048/picoracer2048.py games/toastarling/toastarling_core.py games/toastarling/toastarling.py games/ufoswamp/ufoswamp_core.py games/ufoswamp/ufoswamp.py games/woodworm/woodworm_core.py games/woodworm/woodworm.py`; `make cart-game GAME=pcraft PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Survival/crafting ports could share tile-resource maps, counter-based inventory recipes, workbench gating, tool-yield modifiers, cave/goal progression, and compact HUD recipe selection.
- Backlog changes: Added rank 61 P.Craft as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, extraction blocker, BBS controls/mechanics, Minicraft inspiration context, Deluxe/Stranded Isle context, and current first-playable fidelity gaps.

## eightlegslove - 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described spider-web arcade loop maps cleanly to a host-tested core with bounded spider movement, hold/release web strand placement, bug collision against web segments, fly scoring, beetle web damage, rare butterfly scoring, timed levels, and level advancement.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; local extraction returns no useful Lua/API text for the live cart. Original six-level pacing, exact web physics, climbing/collision feel, authored layouts, bug spawn tuning, sprite art, music, and visual effects are outside this first playable pass.
- Asset/audio notes: FCDB's numeric cart URL is stale, but the BBS thread exposes `https://www.lexaloffle.com/bbs/cposts/4/41422.p8.png`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the web/spider premise.
- Verification: `python3 -m unittest tests.test_eightlegslove_core tests.test_pcraft_core tests.test_motionrec_core tests.test_trialsorcerer_core tests.test_littledragon_core tests.test_picocheckmate_core tests.test_lostnight_core tests.test_freezingknights_core tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_picoracer2048_core tests.test_airdelivery_core tests.test_marballs2_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/eightlegslove/eightlegslove_core.py games/eightlegslove/eightlegslove.py`; `make cart-game GAME=eightlegslove PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Web/physics-lite arcade ports could share point-to-segment collision, transient segment durability, timed level goals, edge-spawned actors, and compact procedural web rendering.
- Backlog changes: Added rank 62 8 Legs to Love as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, extraction blocker, BBS controls/mechanics, beetle/butterfly scoring notes, and current first-playable fidelity gaps.

## guncho - 2026-06-17

- Result: partial
- What translated cleanly: The extracted source and BBS notes map cleanly to a host-tested tactical core with six-direction hex movement, revolver chambers, directional shooting/reloading, punch/stun, bullet hail, dynamite countdown/explosion, simple bandit turns, camp clears, and five-camp boss victory.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; original map generation, enemy AI nuance, sprint subturn mode, walls/fences/traps, action menu presentation, exact revolver animation, music, sprite art, and balance tuning are outside this first playable pass.
- Asset/audio notes: The live BBS cart `https://www.lexaloffle.com/bbs/cposts/gu/guncho-3.p8.png` extracts usable Lua/API with `scripts/pico8_cart_extract.py`; gameplay uses procedural replacement art/audio and an original 240x240 cover. The BBS cart credits the original 7DRL game by Arnold Rauers and Terri Vellman and links later commercial releases, so this pass avoids later release assets.
- Verification: `python3 -m unittest tests.test_guncho_core tests.test_eightlegslove_core tests.test_pcraft_core tests.test_motionrec_core tests.test_trialsorcerer_core tests.test_littledragon_core tests.test_picocheckmate_core tests.test_lostnight_core tests.test_freezingknights_core tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_picoracer2048_core tests.test_airdelivery_core tests.test_marballs2_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/guncho/guncho_core.py games/guncho/guncho.py games/eightlegslove/eightlegslove_core.py games/eightlegslove/eightlegslove.py`; `make cart-game GAME=guncho PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Hex tactics ports could share axial-coordinate cells, directional rays, line-of-sight target scans, turn queues, cooldown/chamber UI, and small enemy-behavior strategies.
- Backlog changes: Added rank 64 Guncho as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, source extraction result, BBS controls/mechanics, original 7DRL credit trail, commercial-release caveat, and current first-playable fidelity gaps.

## rolly - 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described precision-platformer loop maps cleanly to a host-tested core with walking acceleration/friction, jump, roll/hop boost, orb recharge, spike death/respawn counts, bouncy/breakable tiles, friend rescue, and exit clear.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; local extraction returns no usable Lua/API text for the live cart. Original authored screens, exact platformer physics, wall-grab/jump sensitivity, roll animation/squish, music, death effect, save/progress behavior, and full challenge curve are outside this first playable pass.
- Asset/audio notes: FCDB's numeric cart URL 404s, but the BBS thread exposes `https://www.lexaloffle.com/bbs/cposts/5/54262.p8.png`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the cave/platformer premise. Thread evidence credits Davbo and Rory, with Rory making music.
- Verification: `python3 -m unittest tests.test_rolly_core tests.test_guncho_core tests.test_eightlegslove_core tests.test_pcraft_core tests.test_motionrec_core tests.test_trialsorcerer_core tests.test_littledragon_core tests.test_picocheckmate_core tests.test_lostnight_core tests.test_freezingknights_core tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_picoracer2048_core tests.test_airdelivery_core tests.test_marballs2_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/rolly/rolly_core.py games/rolly/rolly.py games/guncho/guncho_core.py games/guncho/guncho.py games/eightlegslove/eightlegslove_core.py games/eightlegslove/eightlegslove.py`; `make cart-game GAME=rolly PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Precision platformer ports could share tile-collision helpers, coyote/jump buffers, roll/dash recharge, spike respawn, collectible-gated exits, and camera/screen-transition adapters.
- Backlog changes: Added rank 65 Rolly as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, extraction blocker, BBS controls/mechanics, itch/controller context, and current first-playable fidelity gaps.

## pigments - 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described tile-painting chase loop maps cleanly to a host-tested grid core with D-pad movement, pigment spending, droplet refills, razor-disc pursuit, grass blocking discs, water hiding the player, trigger dash behavior, and full-board clear state.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; FCDB's numeric cart URL 404s and the live slug cart extracts readable but obfuscated Lua/mechanic strings. Fruit unlocks, highscore/metascore persistence, exact disc physics, tile palettes, music, save formatting, and full level variants are outside this first playable pass.
- Asset/audio notes: The live BBS cart is `https://www.lexaloffle.com/bbs/cposts/pi/pigments-0.p8.png`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the paint/droplet/disc premise.
- Verification: `python3 -m unittest tests.test_pigments_core tests.test_rolly_core tests.test_guncho_core tests.test_eightlegslove_core tests.test_pcraft_core tests.test_motionrec_core tests.test_trialsorcerer_core tests.test_littledragon_core tests.test_picocheckmate_core tests.test_lostnight_core tests.test_freezingknights_core tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_picoracer2048_core tests.test_airdelivery_core tests.test_marballs2_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/pigments/pigments_core.py games/pigments/pigments.py`; `make cart-game GAME=pigments PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Tile-painting/pursuit ports could share grid coverage scoring, collectible respawn selection, obstacle-aware chaser steps, special-tile effects, and compact coverage HUDs.
- Backlog changes: Added rank 68 pigments as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, BBS goal/special-tile mechanics, extraction result, and current first-playable fidelity gaps.

## cherrybomb - 2026-06-17

- Result: partial
- What translated cleanly: The BBS docs and extracted Lua map cleanly to a host-tested arcade-shooter core with D-pad ship movement, fire cooldown, enemy waves, attacking enemies, enemy bullets, life loss/game over, cherry pickups, 10-cherry heart/bonus rules, cherry bomb threat clearing, score, and 9-wave victory.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite. Exact enemy formations, tutorial code organization, logo/title animation, highscore persistence, original sprite art, original music, and precise scoring balance are outside this first playable pass.
- Asset/audio notes: FCDB's numeric cart URL 404s, but the BBS thread exposes `https://www.lexaloffle.com/bbs/cposts/ch/cherrybomb-0.p8.png`; gameplay uses procedural replacement art/audio and an original 240x240 cover. The BBS says the game is reminiscent of Space Invaders/Galaga, so the port keeps generic alien/ship presentation.
- Verification: `python3 -m unittest tests.test_cherrybomb_core tests.test_pigments_core tests.test_rolly_core tests.test_guncho_core tests.test_eightlegslove_core tests.test_pcraft_core tests.test_motionrec_core tests.test_trialsorcerer_core tests.test_littledragon_core tests.test_picocheckmate_core tests.test_lostnight_core tests.test_freezingknights_core tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_picoracer2048_core tests.test_airdelivery_core tests.test_marballs2_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/cherrybomb/cherrybomb_core.py games/cherrybomb/cherrybomb.py games/pigments/pigments_core.py games/pigments/pigments.py`; `make cart-game GAME=cherrybomb PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Shmup ports could share player bounds, bullet/enemy collision helpers, wave spawn tables, pickup fall/collection, bomb radius clearing, and score/life HUD logic.
- Backlog changes: Added rank 69 Cherry Bomb as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, source extraction result, BBS controls/scoring/pickup mechanics, franchise-inspiration caveat, and current first-playable fidelity gaps.

## advancedmicroplatformer - 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described starter-kit mechanics map cleanly to a host-tested platformer demo core with running friction, coyote jump, buffered jump, held variable jump height, one-way platform landing/pass-through behavior, camera threshold scrolling, and goal clear.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; local extraction returns no useful Lua/API text for the live starter-kit cart. Original animation system, collision helper architecture, camera shake, map/sprite data, tutorial code organization, and exact physics constants are outside this first playable pass.
- Asset/audio notes: FCDB's numeric cart URL is stale, but the BBS thread exposes `https://www.lexaloffle.com/bbs/cposts/3/37402.p8.png`; gameplay uses procedural replacement art/audio and an original 240x240 cover. The thread also includes a separate Super Mario Bros. cart, which this port excludes entirely.
- Verification: `python3 -m unittest tests.test_advancedmicroplatformer_core tests.test_cherrybomb_core tests.test_pigments_core tests.test_rolly_core tests.test_guncho_core tests.test_eightlegslove_core tests.test_pcraft_core tests.test_motionrec_core tests.test_trialsorcerer_core tests.test_littledragon_core tests.test_picocheckmate_core tests.test_lostnight_core tests.test_freezingknights_core tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_picoracer2048_core tests.test_airdelivery_core tests.test_marballs2_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/advancedmicroplatformer/advancedmicroplatformer_core.py games/advancedmicroplatformer/advancedmicroplatformer.py games/cherrybomb/cherrybomb_core.py games/cherrybomb/cherrybomb.py games/pigments/pigments_core.py games/pigments/pigments.py`; `make cart-game GAME=advancedmicroplatformer PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Platformer ports could share coyote/buffered jump state, variable jump hold, one-way platform crossing, camera threshold scrolling, and center-coordinate collision tests.
- Backlog changes: Added rank 72 Advanced Micro Platformer - Starter Kit as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, starter-kit mechanics, separate Mario-cart exclusion, extraction blocker, and current first-playable fidelity gaps.

## scrapboy - 2026-06-17

- Result: partial
- What translated cleanly: The extracted source and BBS comments map cleanly to a host-tested action-platformer core with running/jumping, laser shots, bomb door opening, spike damage, bomb-form spike immunity, magnet wall-jump, scrap collectibles, enemy defeat, and exit clear.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; original maps, 3 full levels, 6 complete weapons, 3 difficulties, collectibles/time attack, exact enemy behaviors, pause-menu button swapping, music, sprite art, and speedrun tuning are outside this first playable pass.
- Asset/audio notes: FCDB's numeric cart URL 404s, but the BBS thread exposes `https://www.lexaloffle.com/bbs/cposts/sc/scrap_boy-6.p8.png`; gameplay uses procedural replacement art/audio and an original 240x240 cover. BBS comments compare the game to Mega Man-like platformers, so the port uses generic robot/scrap presentation and no third-party branded assets.
- Verification: `python3 -m unittest tests.test_scrapboy_core tests.test_advancedmicroplatformer_core tests.test_cherrybomb_core tests.test_pigments_core tests.test_rolly_core tests.test_guncho_core tests.test_eightlegslove_core tests.test_pcraft_core tests.test_motionrec_core tests.test_trialsorcerer_core tests.test_littledragon_core tests.test_picocheckmate_core tests.test_lostnight_core tests.test_freezingknights_core tests.test_justoneboss_core tests.test_birdswithguns_core tests.test_highstakes_core tests.test_buns_core tests.test_porklike_core tests.test_picoware_core tests.test_picoracer2048_core tests.test_airdelivery_core tests.test_marballs2_core tests.test_maichanssweetbuns_core tests.test_xzero_core tests.test_picoworldrace_core tests.test_combopool_core tests.test_intoruins_core tests.test_toastarling_core tests.test_woodworm_core tests.test_bas_core tests.test_ufoswamp_core`; `python3 -m py_compile scripts/pico8_top100_status.py scripts/pico8_cart_extract.py scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py games/scrapboy/scrapboy_core.py games/scrapboy/scrapboy.py games/advancedmicroplatformer/advancedmicroplatformer_core.py games/advancedmicroplatformer/advancedmicroplatformer.py games/cherrybomb/cherrybomb_core.py games/cherrybomb/cherrybomb.py games/pigments/pigments_core.py games/pigments/pigments.py`; `make cart-game GAME=scrapboy PYTHON=python3`; `git diff --check`.
- Reusable helper opportunities: Robot/action-platformer ports could share tile collision, shot raycasts, bomb area checks, form/power-up switching, spike immunity state, and exit gates tied to collectibles.
- Backlog changes: Added rank 73 Scrap Boy as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, extractable source/API, mechanics comments, platformer-IP caveat, and current first-playable fidelity gaps.

## shadowsofdunwich - 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described campaign tactics loop maps cleanly to a host-tested core with three soldiers, action points, D-pad cursor movement, shooting, grenades, enemy turns, split-on-death enemies, battle clears, soldier level-ups, skill points, recruit replacement after casualties, campaign advancement, and level-16 victory.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; local extraction returns no usable Lua/API text for the live cart. Original procedural map generation, 3D sprite system, full talent tree, save data, complete enemy roster, exact 16-level pacing, music, and original sprite work are outside this first playable pass.
- Asset/audio notes: FCDB's numeric cart URL 404s, but the BBS thread exposes `https://www.lexaloffle.com/bbs/cposts/sh/shadowsofdunwich-4.p8.png`; gameplay uses procedural replacement art/audio and an original 240x240 cover. The thread describes an X-Com-like design, so this port uses generic occult squad-tactics presentation and no third-party branded assets.
- Verification: pending final command pass in the active migration session.
- Reusable helper opportunities: Grid tactics ports could share AP spending, cursor-target validation, deterministic enemy turns, area attacks, campaign promotion/recruit replacement, and compact tactical HUD/action-strip rendering.
- Backlog changes: Added rank 74 Shadows of Dunwich 2.0 as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, extraction blocker, BBS campaign/mechanics notes, X-Com-like caveat, and current first-playable fidelity gaps.

## picotennis - 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described tennis loop maps cleanly to a host-tested core with serves, rallies, left/right player movement, offset-based shot angle, power meter buildup, power shots, faults, out calls, tennis points, games, sets, and match victory.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; local extraction returns no usable Lua/API text for the live cart. Original 3D rendering, up-to-4-player mode, exact AI, exact hit distance tuning, visual effects, label art, and music are outside this first playable pass.
- Asset/audio notes: FCDB's numeric cart URL 404s, but the BBS thread exposes `https://www.lexaloffle.com/bbs/cposts/pi/picotennis2-0.p8.png`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the court/rally premise.
- Verification: pending final command pass in the active migration session.
- Reusable helper opportunities: Sports ports could share court bounds, paddle/racket hit windows, offset-to-angle mapping, power meters, simple AI tracking, and compact score HUD formatting.
- Backlog changes: Added rank 75 Pico Tennis as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, extraction blocker, BBS controls/mechanics/update notes, and current first-playable fidelity gaps.

## driftmania - 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described time-trial racing loop maps cleanly to a host-tested core with acceleration, braking/reverse, left/right steering, drift-brake faster rotation, grass traction loss without heavy speed loss, boost tiles, checkpoint gates, lap completion, elapsed time, and medal thresholds.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; extracted Lua is minified and not useful for line-by-line translation. Full 15-track campaign, exact track layouts, ghost replay, garage customization, pause/options menus, 3D sprite-stacking rendering, exact drift tuning, music, and original asset presentation are outside this first playable pass.
- Asset/audio notes: The live BBS cart `https://www.lexaloffle.com/bbs/cposts/dr/driftmania-5.p8.png` extracts minified Lua/API with `scripts/pico8_cart_extract.py`; gameplay uses procedural replacement art/audio and an original 240x240 cover. The BBS credits music by Vav, cars based on art by PixelArtM, cover art by TerracotaScarf, and community helpers/inspirations, so the manifest/credits/attribution preserve that chain.
- Verification: pending final command pass in the active migration session.
- Reusable helper opportunities: Racing ports could share car heading/speed integration, surface traction modifiers, boost timers, checkpoint/lap progression, medal timing, and compact track rendering.
- Backlog changes: Added rank 76 Driftmania as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, extractable minified source/API, BBS controls/track/medal/contributor notes, and current first-playable fidelity gaps.

## wobblepaint - 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described gamepad mode maps cleanly to a host-tested drawing core with D-pad cursor movement, brush dabs, brush size adjustment, color cycling, undo by stroke group, clear/new doodle behavior, and wobbling animated points.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite; local extraction returns no usable Lua/API text for the live cart. Original pull-down menu, presets, pattern/shape attributes, multiple doodles, copy/paste/export format, GIF capture, self-saving cart data, secondary/background color controls, and exact wobble rendering are outside this first playable pass.
- Asset/audio notes: The live BBS cart is `https://www.lexaloffle.com/bbs/cposts/wo/wobblepaint-6.p8.png`; gameplay uses procedural replacement art/audio and an original 240x240 cover inspired by the doodle/wobble premise.
- Verification: pending final command pass in the active migration session.
- Reusable helper opportunities: Creative-tool ports could share cursor-brush input, grouped undo stacks, animated stroke renderers, palette cycling, and compact controller modifier prompts.
- Backlog changes: Added rank 79 Wobblepaint 1.6 as partial with confirmed FCDB/BBS/license metadata, live cart URL, extraction blocker, BBS gamepad controls/tool features, and current first-playable fidelity gaps.

## whiplashtaxi - 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described taxi loop maps cleanly to a host-tested core with forward acceleration, deliberate stop-before-reverse switching, left/right steering, crash bounce, stopping next to passengers, destination dropoff, fare scoring, delivery count, active target indicators, and five-minute shift timer.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite. Original 3D renderer, full Motsville map, AI traffic, all customers, free-explore/race modes, lap records, suspension lean, music, and exact driving/drift tuning are outside this first playable pass.
- Asset/audio notes: The live BBS cart `https://www.lexaloffle.com/bbs/cposts/mo/mot_taxi-7.p8.png` extracts readable Lua/API with `scripts/pico8_cart_extract.py`; gameplay uses procedural replacement art/audio and an original 240x240 cover. BBS comments compare it to Crazy Taxi/GTA, so the port keeps generic taxi-delivery presentation and no third-party branded assets.
- Verification: pending final command pass in the active migration session.
- Reusable helper opportunities: City-driving ports could share car heading/speed integration, stop-zone interactions, delivery target queues, timer/fare scoring, minimap/arrow indicators, and simple grid-city rendering.
- Backlog changes: Added rank 80 Whiplash Taxi Co as partial with confirmed FCDB/BBS/license metadata, live cart URL, extractable source/API, BBS pickup/destination/timer/free-explore/race notes, IP-comparison caveat, and current first-playable fidelity gaps.

## nightride - 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described night-driving escalation maps cleanly to a host-tested core with lane changes, traffic hazards, health, distance-based level progression, weapon unlock, bullets, enemy vehicle clearing, boss hit points, score, game over, and sunrise victory.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite. Original authored level beats, precise vehicle movement, car rotation art, particles, music, shooting set pieces, boss patterns, and sunrise ending art are outside this first playable pass.
- Asset/audio notes: The live BBS cart `https://www.lexaloffle.com/bbs/cposts/ni/nightride-0.p8.png` extracts readable Lua/API with `scripts/pico8_cart_extract.py`; gameplay uses procedural replacement art/audio and an original 240x240 cover. BBS comments compare it to Spy Hunter, so the port keeps generic night-road shooter presentation and no third-party branded assets.
- Verification: pending final command pass in the active migration session.
- Reusable helper opportunities: Lane-driving shooter ports could share lane hazards, bullet/traffic collision, level-distance pacing, boss HP gates, and compact road-perspective rendering.
- Backlog changes: Added rank 81 Night Ride as partial with confirmed FCDB/BBS/license metadata, live cart URL, extractable source/API, BBS driving/shooter/boss notes, IP-comparison caveat, and current first-playable fidelity gaps.

## pico8tunesvol1 - 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described album premise maps cleanly to a host-tested player core with 12 tracks, next/previous wrapping, direct selection, play/pause, reset-to-first-track behavior, automatic advance by beat length, progress reporting, and deterministic visualizer points.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite. This is a music/demo cartridge rather than a game, and local extraction returns no Lua/API/audio data for the live cart, so exact PICO-8 SFX/music, original animation code, and track slot mapping are outside this first playable pass.
- Asset/audio notes: The live BBS cart is `https://www.lexaloffle.com/bbs/cposts/3/38440.p8.png`; gameplay uses procedural replacement cover art, visualizer graphics, and simple generated Pyxel sound motifs. The BBS post says the music is intended for reuse, and Krajzeg confirms code/sprites/assets share the Creative Commons umbrella.
- Verification: pending final command pass in the active migration session.
- Reusable helper opportunities: Music/demo carts could share album-player state, setlist rendering, auto-advance, progress bars, and deterministic visualizer generation while waiting for stronger PICO-8 audio extraction.
- Backlog changes: Added rank 85 Pico-8 Tunes Volume 1 as partial with confirmed FCDB/BBS/license metadata, corrected live cart URL, explicit reuse-license evidence, extraction blocker, and current first-playable fidelity gaps.

## cabride - 2026-06-17

- Result: partial
- What translated cleanly: The BBS/source-described train-sim loop maps cleanly to a host-tested core with gradual throttle/brake acceleration, slow stopping, station-distance approach prompts, door gating while moving or away from a signal, passengers boarding/disembarking, stop ratings, scoring, express mode, last-station announcement, journey completion, and weather/scenery state.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite. Original pseudo-3D track/city/tunnel generation, second track/train, long-run memory fixes, very-chilled mode, pause menu, exact station rating tuning, soundtrack, and all sprite/palette effects are outside this first playable pass.
- Asset/audio notes: The live BBS cart is `https://www.lexaloffle.com/bbs/cposts/ca/cab_ride-7.p8.png` and extracts readable Lua/API with `scripts/pico8_cart_extract.py`; gameplay uses procedural replacement train-cab art/audio and an original 240x240 cover. Attribution preserves Powersaurus, Stephen `rych-t` Jones, and Mot's CC BY-NC-SA pseudo-3D racer tutorial credit chain.
- Verification: pending final command pass in the active migration session.
- Reusable helper opportunities: Relaxed sim ports could share inertial throttle/brake models, station approach/rating logic, passenger stop transactions, express/autopilot toggles, and simple perspective-track rendering.
- Backlog changes: Added rank 89 Cab Ride as partial with confirmed FCDB/BBS/license metadata, live cart URL, extractable source/API, BBS controls/version/credit notes, and current first-playable fidelity gaps.

## twohikingcats - 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described art-toy behavior maps cleanly to a host-tested core with speed changes, reset-to-default state, deterministic palette randomization, continuous scroll, alternating meow cadence, manual cat meows, and bobbing cat positions.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite. The live cart downloads but local extraction returns only a tiny invalid fragment, so original line/circle/modulo composition, exact camera shift, cat animation, footstep SFX, and palette formulas are outside this first playable pass.
- Asset/audio notes: The live BBS cart is `https://www.lexaloffle.com/bbs/cposts/1/16151.p8.png`; gameplay uses procedural replacement hills/cats/audio and an original 240x240 cover. A/B meow buttons are a controller-friendly extension inspired by BBS comments about making each cat talk.
- Verification: pending final command pass in the active migration session.
- Reusable helper opportunities: Non-game/art-toy carts could share speed/palette controls, layered procedural scenery, small deterministic animation cores, and optional puppet-style input hooks.
- Backlog changes: Added rank 90 Two Hiking Cats as partial with confirmed FCDB/BBS/license metadata, live cart URL, BBS author controls, extraction blocker, and current first-playable fidelity gaps.

## haroldsbad - 2026-06-17

- Result: partial
- What translated cleanly: The extracted-source platformer premise maps cleanly to a host-tested core with acceleration/friction, jump/gravity, death consuming a life, corpse creation, corpse bridge collision, water drowning, spike death, goal detection, saved-Harold scoring, and reset/next-level flow.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite. Original 32 authored levels, exact physics constants, map/tile collision, wind/fire/arrow/door variants, palette fading, water audio muffling, particles, speedrun timer, and complete ending polish are outside this first playable pass.
- Asset/audio notes: The live BBS cart is `https://www.lexaloffle.com/bbs/cposts/ha/harold-6.p8.png` and extracts readable Lua/API with `scripts/pico8_cart_extract.py`; gameplay uses procedural replacement art/audio and an original 240x240 cover. Attribution records biovoid and thefreakar.
- Verification: pending final command pass in the active migration session.
- Reusable helper opportunities: Precision puzzle-platformers could share dead-body platforms, life-as-resource scoring, water timers, hazard reasons, reset/next-level flow, and compact tileless collision helpers.
- Backlog changes: Added rank 91 Harold's Bad Day as partial with confirmed FCDB/BBS/license metadata, live cart URL, extractable source/API, BBS 32-level/speedrun notes, and current first-playable fidelity gaps.

## brutalpicorace - 2026-06-17

- Result: partial
- What translated cleanly: The extracted-source racing premise maps cleanly to a host-tested core with heavy/normal/light ship classes, class-dependent acceleration/top speed/health, gas/brake, boost meter consumption/recharge, curved-road steering pressure, wall damage, drafting boost, AI progress, lap counting, finish state, and rank calculation.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite. Original six tracks, split-screen multiplayer, full AI levels, pseudo-3D road blocks, 3D layered ship rasterizer, collisions with other ships, timeboards, ship editor/history, music, and exact HUD presentation are outside this first playable pass.
- Asset/audio notes: The live BBS cart is `https://www.lexaloffle.com/bbs/cposts/br/brutalpicorace_104-0.p8.png` and extracts readable Lua/API with `scripts/pico8_cart_extract.py`; gameplay uses procedural replacement racing art/audio and an original 240x240 cover. Attribution records Damien Hostin / dhostin and the BBS community/technical thanks.
- Verification: pending final command pass in the active migration session.
- Reusable helper opportunities: Racing ports could share ship/car class stats, boost meters, track progress/lap accounting, AI progress/rank calculations, drafting windows, wall damage, and perspective-road renderers.
- Backlog changes: Added rank 93 Brutal Pico Race as partial with confirmed FCDB/BBS/license metadata, live cart URL, extractable source/API, BBS controls/features/changelog notes, and current first-playable fidelity gaps.

## subsurface - 2026-06-17

- Result: partial
- What translated cleanly: The extracted-source metroidvania premise maps cleanly to a host-tested core with upgrade flags, health upgrades, jump/double-jump/wall-jump/glide affordances, swim-gated water hazard, shooting, bullet/enemy hits, energy rewards, boss damage, victory state, and reset flow.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite. Original 40-screen authored map, save data, story-caption routing, switch rooms, enemy variants, final platforming section, boss tuning, minimap, music, and sprite/palette effects are outside this first playable pass.
- Asset/audio notes: The live BBS cart is `https://www.lexaloffle.com/bbs/cposts/su/subsurface-2.p8.png` and extracts readable Lua/API with `scripts/pico8_cart_extract.py`; gameplay uses procedural replacement cavern art/audio and an original 240x240 cover. Attribution records JulianR / Julian Reid.
- Verification: pending final command pass in the active migration session.
- Reusable helper opportunities: Metroidvania ports could share upgrade-flag dictionaries, movement ability gates, water/hazard gating, bullet/enemy interactions, boss HP gates, and compact room progression scaffolds.
- Backlog changes: Added rank 94 subsurface as partial with confirmed FCDB/BBS/license metadata, live cart URL, extractable source/API, BBS controls/40-screen/upgrade notes, and current first-playable fidelity gaps.

## dungeonbang - 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described roguelite platformer loop maps cleanly to a host-tested core with wall jumping, movement, enemies, contact damage, attacks, coins, shop purchases, powerups, depth/zone progression, portal exits, and final rescue.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite. Local extraction exposes a compressed/minified fragment and item/dialogue strings rather than practical full source parity. Original random course selection, full preset room set, all enemy variants, all shop items, dialogue/quips, zone music, and ending sequence are outside this first playable pass.
- Asset/audio notes: The live BBS cart is `https://www.lexaloffle.com/bbs/cposts/du/dungeon-0.p8.png`; gameplay uses procedural replacement dungeon art/audio and an original 240x240 cover. Attribution records deklaswas and the BBS playtester/compression-helper thanks in the source thread.
- Verification: pending final command pass in the active migration session.
- Reusable helper opportunities: Roguelite platformers could share wall-jump state, shop item/cost dictionaries, enemy contact/attack loops, depth/zone progression, portal exits, and compact HUD/shop cycling controls.
- Backlog changes: Added rank 95 DUNGEON! as partial with confirmed FCDB/BBS/license metadata, live cart URL, BBS controls/features/shop notes, partial extraction blocker, and current first-playable fidelity gaps.

## mot8ballpool - 2026-06-17

- Result: partial
- What translated cleanly: The extracted-source/BBS 8-ball rules map cleanly to a host-tested core with aim adjustment, cue power, cue-ball shot velocity, table bounces, ball contact/pocket resolution, first sunk color assignment, wrong-color fouls, free balls, black-ball win/forfeit, and two-player turn state.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite. Original 3D camera/rendering, AI opponents, ball-ball collision fidelity, place-ball mode, full shot legality edge cases, ticker UI, menu presentation, and HUD polish are outside this first playable pass.
- Asset/audio notes: The live BBS cart is `https://www.lexaloffle.com/bbs/cposts/mo/mot_pool-23.p8.png` and extracts readable Lua/API with `scripts/pico8_cart_extract.py`; gameplay uses procedural replacement pool-table art/audio and an original 240x240 cover. Attribution records Mot.
- Verification: pending final command pass in the active migration session.
- Reusable helper opportunities: Physics/sports ports could share aim-power controls, simplified projectile/table bounces, turn/foul/free-ball state, color/team assignment, and compact sports HUD rendering.
- Backlog changes: Added rank 96 Mot's 8-Ball Pool as partial with confirmed FCDB/BBS/license metadata, live cart URL, extractable source/API, BBS rules/UI notes, and current first-playable fidelity gaps.

## villager - 2026-06-17

- Result: partial
- What translated cleanly: The extracted-source/BBS city-builder premise maps cleanly to a host-tested core with generated resources, cursor movement, gathering wood/stone/food, building houses/farms/workshops/taverns, pending arrivals, population, food consumption, happiness, production, and peeple leaving when sad/hungry.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite. Original generated island/map/object system, Cluly-inspired tile presentation, full building/object set, peeple pathing, UI polish, particle ambience, world mutation edge cases, and no-save creative session philosophy are outside this first playable pass.
- Asset/audio notes: The live BBS cart is `https://www.lexaloffle.com/bbs/cposts/na/nano_villager-0.p8.png` and extracts readable Lua/API with `scripts/pico8_cart_extract.py`; gameplay uses procedural replacement island art/audio and an original 240x240 cover. Attribution records partnano and the Cluly tile-set inspiration.
- Verification: pending final command pass in the active migration session.
- Reusable helper opportunities: Creative/city-builder ports could share grid cursor controls, resource/cost dictionaries, production intervals, population happiness/consumption loops, and compact tile-map renderers.
- Backlog changes: Added rank 97 Villager as partial with confirmed FCDB/BBS/license metadata, live cart URL, extractable source/API, BBS resource/building/peeple notes, no-save context, and current first-playable fidelity gaps.

## picosnail - 2026-06-17

- Result: partial
- What translated cleanly: The extracted-source/BBS platform-adventure premise maps cleanly to a host-tested core with movement, jumps, star collection, star-spending double jumps, wand shots, centered thwack attacks, star-as-shield hazard handling, switches, doors, warps, a gated cat boss, and final dream-clear state.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite. Original authored rooms, save-data unlock buttons, story-book text, background renderers, sprite/map presentation, object variants, camera transitions, exact animation timing, and music are outside this first playable pass.
- Asset/audio notes: The live BBS cart is `https://www.lexaloffle.com/bbs/cposts/sn/snail-9.p8.png` and extracts readable Lua/API with `scripts/pico8_cart_extract.py`; gameplay uses procedural replacement castle/garden art/audio and an original 240x240 cover. Attribution records GiantLNT / Floofinator and the source credit for Ujico / Snail's House music-character inspiration.
- Verification: pending final command pass in the active migration session.
- Reusable helper opportunities: Platform-adventure ports could share star/ammo resource loops, coyote/double-jump affordances, switch-door-warp gates, hazard shield handling, compact boss gates, and small procedural room renderers.
- Backlog changes: Added rank 98 Pico Snail!: Dream Castle as partial with confirmed FCDB/BBS/license metadata, live cart URL, extractable source/API, BBS remix permission, source credit notes, and current first-playable fidelity gaps.

## starjump - 2026-06-17

- Result: partial
- What translated cleanly: The BBS-described vector platformer maps cleanly to a host-tested core with ground jump, double/triple jump charges, breakable bounce platforms, color-toggled solid platforms, cannon/red-balloon launch, staged progression, timer counting, wobble-style presentation state, and final return-to-start clear.
- What needed shims/manual rewrite: Full manual Pyxel/Python rewrite. Local extraction exposes only helper math/API fragments, so exact authored rooms, screen skip/progress menu, disappearing platform wave timings, save behavior, vector point data, full wobble math, and external soundtrack sync are outside this first playable pass.
- Asset/audio notes: The live BBS cart is `https://www.lexaloffle.com/bbs/cposts/st/starjump-0.p8.png`; gameplay uses procedural replacement vector art/audio and an original 240x240 cover. Attribution records lucatron / Luca Harris and BBS soundtrack/source notes.
- Verification: pending final command pass in the active migration session.
- Reusable helper opportunities: Vector platformer ports could share wobble-grid drawing, jump-charge logic, color-toggle solid masks, breakable platform bounce/collapse behavior, cannon launch helpers, and timer/progress presentation.
- Backlog changes: Added rank 100 Starjump as partial with confirmed FCDB/BBS/license metadata, live cart URL, BBS controls/options/mechanics notes, partial extraction caveat, and current first-playable fidelity gaps.

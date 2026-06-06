# PICO-8 to PyxelPico Porting Workflow

This workflow is for honest 128x128 PICO-8 Lua/cart ports into `projects/pyxelpico-games` as Pyxel/PyxelPico Python games.

It is intentionally conservative: preserve gameplay/assets when allowed, document attribution, and reject unclear rights chains.

## Scope

In scope:

- PICO-8 carts with clear source/license metadata.
- Manual Lua-to-Pyxel Python gameplay ports.
- Preserving 128x128 gameplay, art, SFX, music, and timing where practical.
- PyxelPico packaging through the existing `pyxelpico-games` build scripts.

Out of scope by default:

- Blind conversion of unlicensed carts.
- Commercially risky NC-SA redistribution unless the target distribution permits it.
- Derivative demakes/mods with unclear original rights.
- Treating native PICO-8 runtime execution as a port; that belongs to PyxelPico/Pico8Go cart execution.

## Source of Truth

Read these before porting:

- `projects/pyxelpico-games/AGENTS.md`
- `projects/pyxelpico-games/games.toml`
- `projects/pyxelpico/pyxelpico/spec/game_migration_guide_spec.md`
- `projects/pyxelpico/pyxelpico/spec/game_manifest_spec.md`
- `projects/pyxelpico/pyxelpico/spec/pyxel_game_execution_spec.md`
- `projects/pyxelpico/pyxelpico/spec/pico8_sound_engine_spec.md`
- `projects/fcdb/sources/pico8/bbs_release.json`

Useful local tools/libraries:

- `projects/picovibe/deps/picotool/` for inspecting/listing PICO-8 cart code and data.
- `projects/pyxelpico/pyxelpico/pico8_audio/` for PICO-8 SFX/music parsing references.
- `projects/pyxelpico/crates/pyxel-core/src/pico8_audio.rs` for Rust/p8mod-backed audio behavior.

## Candidate Gate

For each candidate, record:

- Title, author, source URL, cart URL.
- License and redistribution constraints.
- Whether the game is derivative of third-party IP.
- Gameplay genre and controls.
- Asset complexity: sprites, map, label, palette, effects.
- Audio complexity: SFX-only, music patterns, custom instruments/effects.
- PICO-8 API surface used.
- Port risk: low, medium, high, or reject.

Reject or defer if:

- License is missing/unclear.
- The cart is a mod/demake of commercial IP without a clear rights chain.
- It depends heavily on undocumented PICO-8 quirks that are not worth reproducing.
- The gameplay feel is physics-heavy and no simpler candidates have been proven yet.

## Recommended Starter Candidates

Initial local-FCDB shortlist, easy to hard:

1. `2048` — grid puzzle; low asset/audio complexity; CC BY-NC-SA.
2. `XMAS Pong` — tiny arcade loop; low complexity; CC BY-NC-SA.
3. `Floppy Canary` — one-button runner; low complexity; CC BY-NC-SA.
4. `PicoSorter` — likely manageable; inspect cart first; CC BY-NC-SA.
5. `LightWalk` — grid/maze puzzle with GitHub trail; CC BY-NC-SA unless upstream grants more.
6. `Santaban` — Sokoban-like puzzle; medium asset/map work; CC BY-NC-SA.
7. `Field Jump` — side-scroller; tuning-heavy; CC BY-NC-SA.
8. `Office Hell` — puzzle-platformer; higher polish burden; CC BY-NC-SA.
9. `PICO-BALL` — sports/physics; hard because feel matters; CC BY-NC-SA.
10. `Pico Valley` — large Stardew-style demake; high technical and IP risk; avoid as baseline.

## Port Workflow

### 1. Preflight

1. Find candidate in `projects/fcdb/sources/pico8/bbs_release.json`.
2. Confirm license/source URL/cart URL.
3. Download or locate the cart only if permitted by the workflow.
4. Use `picotool` or equivalent extraction to list Lua and inspect cart sections.
5. Write a short candidate note before implementation.

### 2. API Audit

Scan the cart for PICO-8 APIs, especially:

- Lifecycle: `_init`, `_update`, `_update60`, `_draw`
- Input: `btn`, `btnp`
- Graphics: `cls`, `spr`, `sspr`, `map`, `mget`, `mset`, `pget`, `pset`, `line`, `rect`, `rectfill`, `circ`, `circfill`, `print`, `pal`, `palt`, `camera`, `clip`
- Audio: `sfx`, `music`
- Data/flags: `fget`, `fset`, cartdata/dset/dget
- Math/random: `rnd`, `flr`, `mid`, `sin`, `cos`, fixed-step assumptions

Classify each as:

- `direct` — easy Pyxel equivalent.
- `shim` — needs helper wrapper.
- `manual` — rewrite required.
- `missing/risky` — investigate before porting.

### 3. Scaffold

Create:

- `games/<game-id>/<game-id>.py`
- `games/<game-id>/cover.png`
- asset files only if needed and license-compatible.

Follow `projects/pyxelpico-games/AGENTS.md`:

- one game per directory,
- main script name matches game id,
- shared helpers belong in `lib/`,
- metadata goes in `games.toml`, sorted alphabetically by `id`,
- generated outputs stay under `dist/`.

### 4. Translate

Port in this order:

1. Constants, palette, tile/sprite IDs.
2. State model and deterministic update loop.
3. Input handling using Pyxel/PyxelPico controls.
4. Rendering primitives and sprite/map drawing.
5. Collision/gameplay rules.
6. SFX/music last, after gameplay is stable.

Prefer small PICO-8-style shims when they preserve intent, but avoid building a giant compatibility runtime unless multiple ports need it.

### 5. Audio

Use one audio path per port.

Current caution: PyxelPico has both Python and Rust/p8mod PICO-8 audio paths. Verify parser consistency before relying on either for exact preservation.

Recommended follow-up tests:

- Decode same cart through Python parser and Rust/p8mod path.
- Compare extracted SFX/music structures.
- Render small SFX/music snippets and compare waveform-level stats.

### 6. Attribution and Metadata

Update:

- `games.toml`
- `ATTRIBUTION.md` if present/needed
- `CREDITS.md` if present/needed

Metadata should include:

- original title,
- original author,
- source URL,
- license,
- original resolution `128x128`,
- scaling strategy,
- controls,
- migration date,
- any asset/audio preservation notes.

### 7. Verify

From `projects/pyxelpico-games` run at least:

```bash
python3 -m py_compile scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py lib/input_helper.py
make cart-game GAME=<game-id> PYTHON=python3
```

When practical, also run:

```bash
make native-game GAME=<game-id> PYTHON=python3
make web-game GAME=<game-id> PYTHON=python3
```

For gameplay fidelity, prefer:

- screenshot comparison,
- deterministic input replay for puzzle games,
- side-by-side timing checks for action games,
- manual smoke test on target device/runtime when available.

## Agent Workflow

Recommended first dedicated agent: `pyxelpico-porter`.

Use one focused porter before splitting into a team. The agent should:

1. perform candidate/license audit,
2. run API and asset/audio scan,
3. write a port plan,
4. implement one game in `projects/pyxelpico-games/games/<id>/`,
5. update metadata/attribution,
6. run packaging verification,
7. report remaining fidelity gaps.

Only split later if throughput demands it:

- scout: candidate/license research,
- porter: implementation,
- reviewer: fidelity/legal/build review.

## Notes

- Native PICO-8 cart execution is already supported elsewhere in PyxelPico/Pico8Go; this workflow is for editable Pyxel/PyxelPico Python ports.
- CC BY-NC-SA candidates are useful for learning and non-commercial compatible contexts, but are not commercial-clean.
- For commercially reusable games, prefer MIT/Apache/BSD/public-domain sources or get explicit permission/relicense from the author.

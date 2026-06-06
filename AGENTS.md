# AGENTS.md

This file provides guidance to AI coding agents when working in this repository.

## What This Is

`pyxelpico-games` contains open-source Pyxel community games adapted for the
Pico8Go handheld target. It is a sibling project to `../pyxelpico`, which
provides the custom Pyxel engine, launcher, native runtime, and browser WASM
runtime.

## Project Contract

- Each game lives in `games/<game-id>/`.
- The main script MUST be `games/<game-id>/<game-id>.py`.
- Covers live at `games/<game-id>/cover.png` unless a game-specific asset path
  is required by the launcher.
- Shared helper code lives in `lib/`.
- Game metadata lives in `games.toml`; keep entries alphabetically sorted by
  `id`.
- Generated build output lives under `dist/` and is ignored by git.

The PyxelPico launcher discovers native games from `/opt/pyxelpico-games/games`
on device and from the sibling development path `../pyxelpico-games/games`.

## Build Commands

Use `python3` explicitly if the PyxelPico virtualenv is not available.

```bash
# Single-file FCDB cart ZIPs
make carts
make cart-game GAME=asteroids

# Native staging for device/image packaging
make native
make native-game GAME=asteroids
make native DESTDIR=/tmp/pkgroot

# Web/static browser builds using ../pyxelpico/wasm
make web
make web-game GAME=asteroids

# Clean generated output
make clean
```

FCDB cart ZIPs are staged at `dist/carts/pyxelpico/`, with the shared browser
runtime staged once at `dist/runtimes/pyxelpico/web/`. Native output is staged
at `dist/native/opt/pyxelpico-games/`. Web output is staged at `dist/web/`, with
shared PyxelPico WASM runtime files in `dist/web/_pyxel/`.

FCDB treats each PyxelPico game as a single-file cart artifact. The cart file is
`dist/carts/pyxelpico/<game-id>.zip`; it contains `pyxelpico-cart.json`, a
`native/` payload, browser-ready `web/index.html`, and `cover.png` when
available. The cart references the release-level `runtimes/pyxelpico/web/`
runtime instead of duplicating it per game.

To serve web output locally:

```bash
python3 -m http.server 8000 --directory dist/web
```

Then open `http://localhost:8000/<game-id>/`.

## Runtime Assumptions

- Native games run with the PyxelPico engine from `../pyxelpico`, not stock
  upstream Pyxel.
- FCDB shipping uses one `.zip` cart per game, not loose game directories.
- Web builds MUST use the local WASM runtime from `../pyxelpico/wasm`; do not
  point generated game pages at the upstream Pyxel CDN.
- Games target a 240x240 square display and handheld controls: D-pad, A, B,
  Start, Select.
- Prefer gamepad-compatible input helpers or direct Pyxel keyboard/gamepad
  checks already used by nearby games.

## Relevant Specs

This repository does not currently have its own `docs/specs/` directory. Before
changing behavior, read the owning specs in `../pyxelpico/pyxelpico/spec/`:

- `game_manifest_spec.md` for `games.toml` schema and maintenance rules.
- `game_migration_guide_spec.md` for game adaptation expectations.
- `pyxel_game_execution_spec.md` for native launcher/runtime behavior.
- `engine_game_menu_spec.md` for the built-in START menu behavior inherited by
  games that call `pyxel.run()`.

If a change modifies game metadata, native discovery, web packaging, controls,
or runtime assumptions, update this file and/or `README.md` in the same task.

## Development Guidance

- Keep game-source edits scoped to the affected game directory unless the shared
  helper in `lib/` is intentionally being changed.
- Preserve upstream attribution and license files in each game directory.
- Do not remove `ATTRIBUTION.md`, `LICENSE`, or source URLs from `games.toml`.
- Build scripts should remain dependency-light and runnable with standard
  Python plus the sibling PyxelPico checkout.
- Do not commit generated `dist/` output.

## Verification

For build-system changes, run:

```bash
python3 -m py_compile scripts/build_native.py scripts/build_web.py scripts/build_cart_zips.py
make clean && make carts PYTHON=python3 && make native PYTHON=python3 && make web PYTHON=python3
```

For single-game changes, run the narrow target first:

```bash
make cart-game GAME=<game-id> PYTHON=python3
make native-game GAME=<game-id> PYTHON=python3
make web-game GAME=<game-id> PYTHON=python3
```

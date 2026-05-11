# PyxelPico Games

Open-source Pyxel community games adapted for the **Pico8Go** handheld device.

## Device Specs

- **Display**: 240x240 pixels (square, 1:1)
- **Input**: 8 buttons — D-pad (4-way) + A + B + Start + Select
- **Engine**: Pyxel (Python retro game engine)

## Directory Structure

```
games/
  <game-name>/          # One folder per game
    <game>.py           # Main entry point
    assets/             # .pyxres and other assets
    LICENSE             # Original license
    ATTRIBUTION.md      # Author credit and source
```

## Running a Game

```bash
source /path/to/pyxelpico/.venv/bin/activate
cd games/<game-name>
python <game>.py
```

## Build Targets

### Native

Native builds stage the files exactly where the PyxelPico launcher expects them
on device: `/opt/pyxelpico-games/games/<game-id>/<game-id>.py`.

```bash
# Build every game into dist/native/opt/pyxelpico-games/
make native

# Build one game
make native-game GAME=asteroids

# Stage into a package root instead of dist/native
make native DESTDIR=/tmp/pkgroot
```

The staged tree can be copied into a package or image root. The launcher scans
`/opt/pyxelpico-games/games` on device and the sibling `../pyxelpico-games/games`
path during development.

### Web

Web builds use the local PyxelPico WASM runtime from `../pyxelpico/wasm`, not
the upstream Pyxel CDN. Each game is packaged as a `.pyxapp` and wrapped in a
static `index.html` under `dist/web/<game-id>/`.

```bash
# Build every game
make web

# Build one game
make web-game GAME=asteroids
```

The generated files must be served over HTTP because Pyodide and the Pyxel WASM
wheel are loaded by the browser runtime. For a quick local check:

```bash
python3 -m http.server 8000 --directory dist/web
```

Then open `http://localhost:8000/asteroids/`.

## Credits

See individual `ATTRIBUTION.md` files in each game folder and `CREDITS.md` for the global index.

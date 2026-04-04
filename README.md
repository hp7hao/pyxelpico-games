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

## Credits

See individual `ATTRIBUTION.md` files in each game folder and `CREDITS.md` for the global index.

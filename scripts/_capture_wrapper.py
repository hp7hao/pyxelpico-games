"""Internal wrapper: monkey-patches pyxel for headless screenshot capture.

Called by capture_covers.py as:
  python _capture_wrapper.py <game_main.py>

Environment variables:
  PYXEL_CAPTURE_OUTPUT - path to save the screenshot
  PYXEL_CAPTURE_FRAME  - frame number on which to capture (default 5)
"""
import os
import sys
import runpy

output_path = os.environ["PYXEL_CAPTURE_OUTPUT"]
capture_frame = int(os.environ.get("PYXEL_CAPTURE_FRAME", "5"))

# Patch pyxel before any game code imports it
import pyxel

_real_init = pyxel.init
_real_run = pyxel.run


def _patched_init(*args, **kwargs):
    kwargs["headless"] = True
    kwargs.pop("display_scale", None)
    return _real_init(*args, **kwargs)


def _patched_run(update_fn, draw_fn):
    frame_count = 0

    def wrapped_update():
        nonlocal frame_count
        frame_count += 1
        update_fn()

    def wrapped_draw():
        draw_fn()
        if frame_count == capture_frame:
            pyxel.screenshot(output_path, scale=1)
        if frame_count > capture_frame:
            pyxel.quit()

    _real_run(wrapped_update, wrapped_draw)


pyxel.init = _patched_init
pyxel.run = _patched_run

# Now run the game's main script
game_path = sys.argv[1]
game_dir = os.path.dirname(os.path.abspath(game_path))
game_name = os.path.splitext(os.path.basename(game_path))[0]

# Add game dir and lib dir to path
sys.path.insert(0, game_dir)
lib_dir = os.path.join(os.path.dirname(game_dir), "..", "lib")
sys.path.insert(0, os.path.abspath(lib_dir))

# Change to game dir so relative paths work
os.chdir(game_dir)

# Use runpy to execute the game module safely
runpy.run_path(game_path, run_name="__main__")

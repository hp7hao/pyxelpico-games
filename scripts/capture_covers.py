#!/usr/bin/env python3
"""Capture cover screenshots for all games by running them headlessly.

Usage: python capture_covers.py [game_id ...]
  No args = capture all games. Pass game IDs to capture specific ones.

Each game runs headlessly for CAPTURE_FRAME frames, then a screenshot is
saved as games/<id>/cover.png.
"""
import os
import sys
import importlib
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
GAMES_DIR = os.path.join(PROJECT_DIR, "games")

# How many frames to let the game run before capturing.
# Title screens are typically drawn on the first frame, so a few frames
# is enough for assets to load and the initial draw to complete.
CAPTURE_FRAME = 5

ALL_GAMES = [
    "aclm",
    "asteroids",
    "bakudankun",
    "bubbles",
    "cheaperdepth",
    "chottocopter",
    "flatbird",
    "frogger",
    "growygardens",
    "kanixian",
    "kektris",
    "pinball",
    "poker",
    "stellarblazer",
]


def capture_game(game_id: str) -> bool:
    """Capture a cover for a single game by running it in a subprocess."""
    game_dir = os.path.join(GAMES_DIR, game_id)
    main_py = os.path.join(game_dir, f"{game_id}.py")
    cover_path = os.path.join(game_dir, "cover.png")

    if not os.path.isfile(main_py):
        print(f"  SKIP {game_id}: {main_py} not found")
        return False

    # Run the game in a subprocess with the capture wrapper
    env = os.environ.copy()
    env["PYXEL_CAPTURE_OUTPUT"] = cover_path
    env["PYXEL_CAPTURE_FRAME"] = str(CAPTURE_FRAME)

    wrapper = os.path.join(SCRIPT_DIR, "_capture_wrapper.py")
    result = subprocess.run(
        [sys.executable, wrapper, main_py],
        env=env,
        cwd=game_dir,
        timeout=30,
        capture_output=True,
        text=True,
    )

    if os.path.isfile(cover_path):
        size = os.path.getsize(cover_path)
        print(f"  OK   {game_id}: cover.png ({size} bytes)")
        return True
    else:
        print(f"  FAIL {game_id}: no cover.png produced")
        if result.stderr:
            for line in result.stderr.strip().split("\n")[-5:]:
                print(f"       {line}")
        return False


def main():
    games = sys.argv[1:] if len(sys.argv) > 1 else ALL_GAMES
    print(f"Capturing covers for {len(games)} games...\n")

    ok, fail = 0, 0
    for game_id in games:
        success = capture_game(game_id)
        if success:
            ok += 1
        else:
            fail += 1

    print(f"\nDone: {ok} captured, {fail} failed")


if __name__ == "__main__":
    main()

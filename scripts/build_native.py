#!/usr/bin/env python3
"""Build PyxelPico games into a launcher-compatible native tree."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
GAMES_DIR = ROOT_DIR / "games"
LIB_DIR = ROOT_DIR / "lib"
DIST_DIR = ROOT_DIR / "dist" / "native"
INSTALL_ROOT = Path("opt") / "pyxelpico-games"


def _parse_games_toml(path: Path) -> dict[str, dict[str, str]]:
    try:
        import tomllib

        data = tomllib.loads(path.read_text(encoding="utf-8"))
        return {entry["id"]: entry for entry in data.get("games", [])}
    except ModuleNotFoundError:
        pass

    games: dict[str, dict[str, str]] = {}
    current: dict[str, str] | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line == "[[games]]":
            current = {}
            continue
        if current is None or not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"')
        current[key] = value
        if key == "id":
            games[value] = current
    return games


def _ignore(_dir: str, names: list[str]) -> set[str]:
    ignored = {"__pycache__"}
    ignored.update(name for name in names if name.endswith(".pyc"))
    return ignored


def _main_script(game_id: str) -> Path:
    script = GAMES_DIR / game_id / f"{game_id}.py"
    if not script.exists():
        raise SystemExit(f"missing startup script: {script}")
    return script


def _copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=_ignore)


def _build_game(game_id: str, output_root: Path) -> None:
    _main_script(game_id)
    src = GAMES_DIR / game_id
    dst = output_root / "games" / game_id
    _copy_tree(src, dst)
    print(f"staged {dst}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game", help="build one game id from games.toml")
    parser.add_argument(
        "--destdir",
        default=os.environ.get("DESTDIR"),
        help="optional output root; defaults to dist/native",
    )
    args = parser.parse_args()

    games = _parse_games_toml(ROOT_DIR / "games.toml")
    selected = [args.game] if args.game else sorted(games)
    missing = [game_id for game_id in selected if game_id not in games]
    if missing:
        raise SystemExit(f"unknown game id: {', '.join(missing)}")

    destdir = Path(args.destdir).resolve() if args.destdir else DIST_DIR
    output_root = destdir / INSTALL_ROOT
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "games").mkdir(parents=True, exist_ok=True)

    for name in ["games.toml", "CREDITS.md", "README.md"]:
        src = ROOT_DIR / name
        if src.exists():
            shutil.copy2(src, output_root / name)

    if LIB_DIR.exists():
        _copy_tree(LIB_DIR, output_root / "lib")

    for game_id in selected:
        _build_game(game_id, output_root)

    print(f"native tree: {output_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Build PyxelPico games as static Pyxel web apps."""

from __future__ import annotations

import argparse
import base64
import html
import os
from pathlib import Path
import shutil
import sys
import zipfile


ROOT_DIR = Path(__file__).resolve().parents[1]
GAMES_DIR = ROOT_DIR / "games"
LIB_DIR = ROOT_DIR / "lib"
DIST_DIR = ROOT_DIR / "dist" / "web"
APP_ROOT = "pyxelpico-games"
STARTUP_FILE = ".pyxapp_startup_script"
APP_EXT = ".pyxapp"

METADATA_FIELDS = ["title", "author", "license", "source_url", "migration_date"]
RUNTIME_FILES = ["pyxel.js", "pyxel.css", "import_hook.py"]


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


def _iter_files(path: Path) -> list[Path]:
    files: list[Path] = []
    for file in path.rglob("*"):
        if not file.is_file():
            continue
        parts = set(file.parts)
        if "__pycache__" in parts or file.suffix == ".pyc":
            continue
        files.append(file)
    return sorted(files)


def _metadata_comment(game: dict[str, str]) -> str:
    lines = []
    for field in METADATA_FIELDS:
        value = game.get(field)
        if value:
            lines.append(f"{field} : {value}")
    return "\n".join(lines)


def _main_script(game_id: str) -> Path:
    script = GAMES_DIR / game_id / f"{game_id}.py"
    if script.exists():
        return script

    candidates = sorted((GAMES_DIR / game_id).glob("*.py"))
    if len(candidates) == 1:
        return candidates[0]
    raise SystemExit(f"cannot determine startup script for game '{game_id}'")


def _write_pyxapp(game_id: str, game: dict[str, str], output_dir: Path) -> Path:
    script = _main_script(game_id)
    pyxapp_path = output_dir / f"{game_id}{APP_EXT}"
    startup_path = f"games/{game_id}/{script.name}"
    comment = _metadata_comment(game)

    with zipfile.ZipFile(pyxapp_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.comment = comment.encode("utf-8")
        zf.writestr(f"{APP_ROOT}/{STARTUP_FILE}", startup_path)

        for file in _iter_files(GAMES_DIR / game_id):
            arcname = f"{APP_ROOT}/{file.relative_to(ROOT_DIR).as_posix()}"
            zf.write(file, arcname)

        if LIB_DIR.exists():
            for file in _iter_files(LIB_DIR):
                arcname = f"{APP_ROOT}/{file.relative_to(ROOT_DIR).as_posix()}"
                zf.write(file, arcname)

    return pyxapp_path


def _write_html(game_id: str, game: dict[str, str], pyxapp_path: Path, output_dir: Path) -> None:
    encoded_app = base64.b64encode(pyxapp_path.read_bytes()).decode("ascii")
    title = html.escape(game.get("title", game_id))
    app_name = html.escape(pyxapp_path.name)
    output = f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no\">
    <title>{title}</title>
    <script src=\"../_pyxel/pyxel.js\"></script>
  </head>
  <body>
    <script>
      launchPyxel({{
        command: "play",
        name: "{app_name}",
        gamepad: "enabled",
        base64: "{encoded_app}",
      }});
    </script>
  </body>
</html>
"""
    (output_dir / "index.html").write_text(output, encoding="utf-8")


def _copy_runtime(pyxelpico_dir: Path) -> None:
    wasm_dir = pyxelpico_dir / "wasm"
    runtime_dir = DIST_DIR / "_pyxel"
    runtime_dir.mkdir(parents=True, exist_ok=True)

    for name in RUNTIME_FILES:
        src = wasm_dir / name
        if not src.exists():
            raise SystemExit(f"missing Pyxel web runtime file: {src}")
        shutil.copy2(src, runtime_dir / name)

    wheels = sorted(wasm_dir.glob("pyxel-*-emscripten_*.whl"))
    if len(wheels) != 1:
        raise SystemExit(f"expected exactly one Pyxel WASM wheel in {wasm_dir}")
    shutil.copy2(wheels[0], runtime_dir / wheels[0].name)

    images_src = wasm_dir / "images"
    images_dst = runtime_dir / "images"
    if images_dst.exists():
        shutil.rmtree(images_dst)
    shutil.copytree(images_src, images_dst)


def _build_game(game_id: str, game: dict[str, str]) -> None:
    output_dir = DIST_DIR / game_id
    output_dir.mkdir(parents=True, exist_ok=True)
    pyxapp_path = _write_pyxapp(game_id, game, output_dir)
    _write_html(game_id, game, pyxapp_path, output_dir)
    pyxapp_path.unlink()
    print(f"built {output_dir.relative_to(ROOT_DIR)}/index.html")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game", help="build one game id from games.toml")
    parser.add_argument(
        "--pyxelpico-dir",
        default=os.environ.get("PYXELPICO_DIR", "../pyxelpico"),
        help="path to the PyxelPico engine checkout",
    )
    args = parser.parse_args()

    pyxelpico_dir = (ROOT_DIR / args.pyxelpico_dir).resolve()
    if not pyxelpico_dir.exists():
        raise SystemExit(f"missing PyxelPico directory: {pyxelpico_dir}")

    games = _parse_games_toml(ROOT_DIR / "games.toml")
    selected = [args.game] if args.game else sorted(games)
    missing = [game_id for game_id in selected if game_id not in games]
    if missing:
        raise SystemExit(f"unknown game id: {', '.join(missing)}")

    _copy_runtime(pyxelpico_dir)
    for game_id in selected:
        _build_game(game_id, games[game_id])
    return 0


if __name__ == "__main__":
    sys.exit(main())

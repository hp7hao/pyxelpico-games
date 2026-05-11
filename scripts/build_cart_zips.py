#!/usr/bin/env python3
"""Build one-file PyxelPico cart ZIPs for FCDB distribution."""

from __future__ import annotations

import argparse
import base64
import html
import io
import json
import os
from pathlib import Path
import shutil
import sys
import zipfile


ROOT_DIR = Path(__file__).resolve().parents[1]
GAMES_DIR = ROOT_DIR / "games"
LIB_DIR = ROOT_DIR / "lib"
DIST_DIR = ROOT_DIR / "dist" / "carts" / "pyxelpico"
RUNTIME_DIST_DIR = ROOT_DIR / "dist" / "runtimes" / "pyxelpico" / "web"
APP_ROOT = "pyxelpico-games"
STARTUP_FILE = ".pyxapp_startup_script"
APP_EXT = ".pyxapp"
RUNTIME_FILES = ["pyxel.js", "pyxel.css", "import_hook.py"]


def _parse_games_toml(path: Path) -> dict[str, dict[str, object]]:
    try:
        import tomllib

        data = tomllib.loads(path.read_text(encoding="utf-8"))
        return {entry["id"]: entry for entry in data.get("games", [])}
    except ModuleNotFoundError:
        pass

    games: dict[str, dict[str, object]] = {}
    current: dict[str, object] | None = None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line == "[[games]]":
            current = {}
            continue
        if current is None or not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        raw_value = value.strip()
        if raw_value in {"true", "false"}:
            parsed_value: object = raw_value == "true"
        else:
            parsed_value = raw_value.strip('"')
        current[key] = parsed_value
        if key == "id":
            games[str(parsed_value)] = current
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


def _main_script(game_id: str) -> Path:
    script = GAMES_DIR / game_id / f"{game_id}.py"
    if not script.exists():
        raise SystemExit(f"missing startup script: {script}")
    return script


def _metadata_comment(game: dict[str, object]) -> str:
    fields = ["title", "author", "license", "source_url", "migration_date"]
    lines = []
    for field in fields:
        value = game.get(field)
        if value not in (None, ""):
            lines.append(f"{field} : {value}")
    return "\n".join(lines)


def _build_pyxapp_bytes(game_id: str, game: dict[str, object]) -> bytes:
    script = _main_script(game_id)
    startup_path = f"games/{game_id}/{script.name}"
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.comment = _metadata_comment(game).encode("utf-8")
        zf.writestr(f"{APP_ROOT}/{STARTUP_FILE}", startup_path)

        for file in _iter_files(GAMES_DIR / game_id):
            arcname = f"{APP_ROOT}/{file.relative_to(ROOT_DIR).as_posix()}"
            zf.write(file, arcname)

        if LIB_DIR.exists():
            for file in _iter_files(LIB_DIR):
                arcname = f"{APP_ROOT}/{file.relative_to(ROOT_DIR).as_posix()}"
                zf.write(file, arcname)

    return buffer.getvalue()


def _manifest(game_id: str, game: dict[str, object]) -> dict[str, object]:
    script = _main_script(game_id)
    return {
        "format": "pyxelpico-cart",
        "format_version": 1,
        "id": game_id,
        "title": game.get("title", game_id),
        "author": game.get("author"),
        "license": game.get("license"),
        "source_url": game.get("source_url"),
        "native": {
            "root": "native",
            "entrypoint": f"native/{game_id}/{script.name}",
            "install_games_path": "/opt/pyxelpico-games/games",
        },
        "web": {
            "root": "web",
            "entrypoint": "web/index.html",
            "runtime": "runtimes/pyxelpico/web",
            "runner": "pyxelpico-wasm",
        },
        "cover": "cover.png" if (GAMES_DIR / game_id / "cover.png").exists() else None,
    }


def _web_index(game_id: str, game: dict[str, object]) -> str:
    encoded_app = base64.b64encode(_build_pyxapp_bytes(game_id, game)).decode("ascii")
    title = html.escape(str(game.get("title", game_id)))
    app_name = html.escape(f"{game_id}{APP_EXT}")
    return f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no\">
    <title>{title}</title>
    <script src=\"../../../runtimes/pyxelpico/web/pyxel.js\"></script>
  </head>
  <body>
    <script>
      launchPyxel({{
        command: \"play\",
        name: \"{app_name}\",
        gamepad: \"enabled\",
        base64: \"{encoded_app}\",
      }});
    </script>
  </body>
</html>
"""


def _write_web_runtime(pyxelpico_dir: Path) -> None:
    wasm_dir = pyxelpico_dir / "wasm"
    if RUNTIME_DIST_DIR.exists():
        shutil.rmtree(RUNTIME_DIST_DIR)
    RUNTIME_DIST_DIR.mkdir(parents=True, exist_ok=True)

    for name in RUNTIME_FILES:
        src = wasm_dir / name
        if not src.exists():
            raise SystemExit(f"missing PyxelPico web runtime file: {src}")
        shutil.copy2(src, RUNTIME_DIST_DIR / name)

    wheels = sorted(wasm_dir.glob("pyxel-*-emscripten_*.whl"))
    if len(wheels) != 1:
        raise SystemExit(f"expected exactly one Pyxel WASM wheel in {wasm_dir}")
    shutil.copy2(wheels[0], RUNTIME_DIST_DIR / wheels[0].name)

    images_dir = wasm_dir / "images"
    if not images_dir.exists():
        raise SystemExit(f"missing Pyxel web runtime images directory: {images_dir}")
    shutil.copytree(images_dir, RUNTIME_DIST_DIR / "images")


def _write_cart_zip(game_id: str, game: dict[str, object]) -> Path:
    output_path = DIST_DIR / f"{game_id}.zip"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        manifest = _manifest(game_id, game)
        zf.writestr("pyxelpico-cart.json", json.dumps(manifest, indent=2) + "\n")

        cover = GAMES_DIR / game_id / "cover.png"
        if cover.exists():
            zf.write(cover, "cover.png")

        for file in _iter_files(GAMES_DIR / game_id):
            arcname = f"native/{file.relative_to(GAMES_DIR).as_posix()}"
            zf.write(file, arcname)

        if LIB_DIR.exists():
            for file in _iter_files(LIB_DIR):
                arcname = f"native/{file.relative_to(ROOT_DIR).as_posix()}"
                zf.write(file, arcname)

        zf.writestr("web/index.html", _web_index(game_id, game))

    return output_path


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

    _write_web_runtime(pyxelpico_dir)
    print(f"built {RUNTIME_DIST_DIR.relative_to(ROOT_DIR)}")

    for game_id in selected:
        output_path = _write_cart_zip(game_id, games[game_id])
        print(f"built {output_path.relative_to(ROOT_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

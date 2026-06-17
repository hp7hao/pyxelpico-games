#!/usr/bin/env python3
"""Report PICO-8 BBS top-100 migration status for PyxelPico.

The ranked candidate set is derived from FCDB rather than copied into a second
tracker. Per-port state still lives in games.toml and the porting backlog.
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import re
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
MONOREPO_DIR = ROOT_DIR.parents[1]
FCDB_BBS_RELEASE = MONOREPO_DIR / "projects" / "fcdb" / "sources" / "pico8" / "bbs_release.json"
GAMES_TOML = ROOT_DIR / "games.toml"

IP_RISK_PATTERNS = {
    "celeste": "commercial/third-party IP demake",
    "terraria": "commercial/third-party IP demake",
    "poom": "commercial/third-party IP demake",
    "superhot": "commercial/third-party IP demake",
    "picohot": "commercial/third-party IP demake",
    "sonic": "commercial/third-party IP demake",
    "fnf": "commercial/third-party IP demake",
    "pvz": "commercial/third-party IP demake",
    "chrome": "commercial/third-party IP demake",
    "castlevania": "commercial/third-party IP demake",
    "tetris": "commercial/third-party IP demake",
    "suika": "commercial/third-party IP demake",
    "x-wing": "commercial/third-party IP demake",
    "tie fighter": "commercial/third-party IP demake",
    "star wars": "commercial/third-party IP demake",
    "dinky kong": "commercial/third-party IP demake",
    "r-type": "commercial/third-party IP demake",
    "wolfenstein": "commercial/third-party IP demake",
    "minecraft": "commercial/third-party IP demake",
    "megaman": "commercial/third-party IP demake",
    "mega man": "commercial/third-party IP demake",
    "rockman": "commercial/third-party IP demake",
    "arkanoid": "commercial/third-party IP demake",
    "breakout hero": "commercial/third-party IP demake",
}


def _load_games_toml(path: Path) -> list[dict[str, object]]:
    try:
        import tomllib

        return tomllib.loads(path.read_text(encoding="utf-8")).get("games", [])
    except ModuleNotFoundError:
        entries: list[dict[str, object]] = []
        current: dict[str, object] | None = None
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if line == "[[games]]":
                if current is not None:
                    entries.append(current)
                current = {}
                continue
            if current is None or not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            raw_value = value.strip()
            current[key.strip()] = raw_value.strip('"')
        if current is not None:
            entries.append(current)
        return entries


def _manifest_bbs_refs(entries: list[dict[str, object]]) -> tuple[set[str], set[str]]:
    tids: set[str] = set()
    pids: set[str] = set()

    for entry in entries:
        source_url = str(entry.get("source_url", ""))
        tid_match = re.search(r"[?&]tid=(\d+)", source_url)
        if tid_match:
            tids.add(tid_match.group(1))

        notes = str(entry.get("notes", ""))
        for pid_match in re.finditer(r"cposts/(?:[a-z0-9_-]+/)?(?:[a-z0-9_-]+-)?(\d+)\.p8\.png", notes):
            pids.add(pid_match.group(1))

    return tids, pids


def _ip_risk_reason(game: dict[str, object]) -> str | None:
    extension = game.get("extension") if isinstance(game.get("extension"), dict) else {}
    tags = extension.get("tags") if isinstance(extension.get("tags"), list) else []
    haystack = " ".join(
        str(game.get(key, "")) for key in ("name", "slug", "description")
    ).lower() + " " + " ".join(str(tag) for tag in tags).lower()
    for pattern, reason in IP_RISK_PATTERNS.items():
        if pattern in haystack:
            return reason
    return None


def _cart_url(game: dict[str, object]) -> str:
    extension = game.get("extension") if isinstance(game.get("extension"), dict) else {}
    thumbnail_path = str(extension.get("thumbnail_path", ""))
    match = re.search(r"/bbs/thumbs/pico8_(.+)\.png$", thumbnail_path)
    if match:
        cart_name = match.group(1)
        return f"https://www.lexaloffle.com/bbs/cposts/{cart_name[:2].lower()}/{cart_name}.p8.png"
    return str(extension.get("cart_url", ""))


def _classify(game: dict[str, object], migrated_tids: set[str], migrated_pids: set[str]) -> tuple[str, str]:
    extension = game.get("extension") if isinstance(game.get("extension"), dict) else {}
    tid = str(extension.get("tid", ""))
    pid = str(game.get("id", ""))
    if tid in migrated_tids or pid in migrated_pids:
        return "migrated", "matching BBS thread/cart reference exists in games.toml"

    license_info = game.get("license") if isinstance(game.get("license"), dict) else None
    license_type = str(license_info.get("type", "")) if license_info else ""
    if "CC4" not in license_type:
        return "blocked-license", "FCDB has no redistributable CC4 license metadata"

    ip_reason = _ip_risk_reason(game)
    if ip_reason:
        return "blocked-ip-risk", ip_reason

    return "todo", "eligible for candidate audit"


def _ranked_games(path: Path, limit: int) -> list[dict[str, object]]:
    games = json.loads(path.read_text(encoding="utf-8"))
    ranked = [
        game
        for game in games
        if isinstance(game.get("extension"), dict)
        and isinstance(game["extension"].get("likes"), int)
    ]
    ranked.sort(key=lambda game: game["extension"]["likes"], reverse=True)
    return ranked[:limit]


def _rows(limit: int) -> list[dict[str, object]]:
    entries = _load_games_toml(GAMES_TOML)
    migrated_tids, migrated_pids = _manifest_bbs_refs(entries)
    rows = []

    for rank, game in enumerate(_ranked_games(FCDB_BBS_RELEASE, limit), start=1):
        extension = game["extension"]
        status, reason = _classify(game, migrated_tids, migrated_pids)
        license_info = game.get("license") if isinstance(game.get("license"), dict) else None
        rows.append(
            {
                "rank": rank,
                "id": str(game.get("id", "")),
                "tid": str(extension.get("tid", "")),
                "likes": int(extension.get("likes", 0)),
                "name": html.unescape(str(game.get("name", ""))),
                "author": html.unescape(str(game.get("author", {}).get("name", ""))),
                "license": str(license_info.get("type", "")) if license_info else "",
                "status": status,
                "reason": reason,
                "bbs_url": f"https://www.lexaloffle.com/bbs/?tid={extension.get('tid', '')}",
                "cart_url": _cart_url(game),
            }
        )
    return rows


def _print_summary(rows: list[dict[str, object]]) -> None:
    counts: dict[str, int] = {}
    for row in rows:
        counts[str(row["status"])] = counts.get(str(row["status"]), 0) + 1

    total = len(rows)
    print(f"PICO-8 BBS top {total} -> PyxelPico migration status")
    for key in ("migrated", "todo", "blocked-license", "blocked-ip-risk"):
        print(f"  {key}: {counts.get(key, 0)}")


def _print_table(rows: list[dict[str, object]], status_filter: str | None) -> None:
    filtered = [row for row in rows if status_filter in (None, "all", row["status"])]
    print("| Rank | ID | Likes | Status | Title | Author | Reason |")
    print("|---:|---:|---:|---|---|---|---|")
    for row in filtered:
        print(
            "| {rank} | {id} | {likes} | {status} | {name} | {author} | {reason} |".format(
                **{key: str(value).replace("|", "\\|") for key, value in row.items()}
            )
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=100, help="ranked BBS candidate count")
    parser.add_argument(
        "--status",
        choices=("all", "migrated", "todo", "blocked-license", "blocked-ip-risk"),
        default="all",
        help="filter table rows by computed status",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    if not FCDB_BBS_RELEASE.exists():
        print(f"missing FCDB BBS metadata: {FCDB_BBS_RELEASE}", file=sys.stderr)
        return 2
    if not GAMES_TOML.exists():
        print(f"missing games manifest: {GAMES_TOML}", file=sys.stderr)
        return 2

    rows = _rows(args.limit)
    if args.json:
        print(json.dumps(rows, indent=2))
        return 0

    _print_summary(rows)
    print()
    _print_table(rows, args.status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

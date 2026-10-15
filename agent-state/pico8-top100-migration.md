# PICO-8 BBS Top 100 Migration Track

This track covers manual PICO-8 BBS fan-favorite ports into PyxelPico Python
games. The ranked candidate set is the top 100 by `extension.likes` in
FCDB PICO-8 bbs metadata, matching the FCDB
`bbs-fan-favorites` curated list semantics.

## Policy

- Count a game as migrated only when it has a PyxelPico game directory,
  `games.toml` metadata, attribution, and `make cart-game GAME=<id> PYTHON=python3`
  verification.
- Block candidates without redistributable license metadata instead of creating
  approximation ports from screenshots.
- Block commercial-IP demakes/mods unless there is an explicit approved rights
  chain for redistribution as a PyxelPico game.
- Prefer candidates with local source trails, upstream repositories, or carts
  that can be decoded for API audit.
- Record every candidate attempt in `agent-state/porting-backlog.md` and append
  lessons to `agent-state/porting-lessons.md`.

## Status Command

Run from this project root:

```bash
python3 scripts/pico8_top100_status.py --status all
```

Useful focused views:

```bash
python3 scripts/pico8_top100_status.py --status todo
python3 scripts/pico8_top100_status.py --status blocked-license
python3 scripts/pico8_top100_status.py --status blocked-ip-risk
```

As of 2026-06-22, the strict FCDB like-ranked top 100 has 49 migrated,
0 eligible for candidate audit, 36 blocked by missing license metadata, and
15 blocked by obvious derivative-IP risk. These counts are computed by
`scripts/pico8_top100_status.py` from FCDB plus `games.toml`; rerun the status
command instead of hand-maintaining counts.

## Current Progress

The strict top-100 queue is drained: every candidate is currently classified as
`migrated`, `blocked-license`, or `blocked-ip-risk` by the status command.
There is no current `todo` candidate. Rank 98 `Pico Snail!: Dream Castle` and
rank 100 `Starjump` are now migrated, so do not treat older notes that name
rank 98 as the next eligible candidate as current planning authority.

# PICO-8 BBS Top 100 Migration Track

This track covers manual PICO-8 BBS fan-favorite ports into PyxelPico Python
games. The ranked candidate set is the top 100 by `extension.likes` in
`projects/fcdb/sources/pico8/bbs_release.json`, matching the FCDB
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

As of 2026-06-17 after the Night Ride port, the strict FCDB
like-ranked top 100 has 38 migrated, 11 eligible for candidate audit, 36 blocked
by missing license metadata, and 15 blocked by obvious derivative-IP risk. These counts are
computed by `scripts/pico8_top100_status.py` from FCDB plus `games.toml`.

## Current Progress

Current migrated strict top-100 ports are rank 2 `Just One Boss`, rank 4
`Birds With Guns`, rank 8 `High Stakes`, rank 12 `Buns: Bunny survivor`,
rank 13 `Porklike`, rank 14 `PICOWARE`, rank 18 `Mai-Chan's Sweet Buns`,
rank 24 `X-Zero`, rank 26 `Pico World Race 1.2`, rank 27 `Combo Pool`,
rank 32 `Into Ruins`, rank 35 `To a Starling`, rank 36 `Woodworm`, and rank 37
`BAS`, rank 41 `UFO Swamp Odyssey`, rank 42 `PICORACER-2048`, and rank 44
`Air Delivery`, rank 46 `Marballs 2`, rank 48 `Freezing Knights`, rank 49
`The Lost Night Release`, rank 52 `Pico Checkmate`, rank 55 `Little Dragon Adventure`, rank 59 `Trial of the Sorcerer`, rank 60 `MOTION.REC`, rank 61 `P.Craft`, rank 62 `8 Legs to Love`, rank 64 `Guncho`, rank 65 `Rolly`, rank 68 `pigments`, rank 69 `Cherry Bomb`, rank 72 `Advanced Micro Platformer - Starter Kit`, rank 73 `Scrap Boy`, rank 74 `Shadows of Dunwich 2.0`, rank 75 `Pico Tennis`, rank 76 `Driftmania`, rank 79 `Wobblepaint`, rank 80 `Whiplash Taxi Co`, rank 81 `Night Ride`, rank 85 `Pico-8 Tunes Volume 1`, rank 89 `Cab Ride`, rank 90 `Two Hiking Cats`, rank 91 `Harold's Bad Day`, rank 93 `Brutal Pico Race`, rank 94 `subsurface`, rank 95 `DUNGEON!`, rank 96 `Mot's 8-Ball Pool`, and rank 97 `Villager`. Rank 17 `Marble Merger`, rank 45 `Demon Castle`, rank 51 `Nanoman`, and rank 71 `Breakout Hero`
are blocked for derivative-IP risk from FCDB tags/thread evidence. The next
eligible candidate is rank 98 `Pico Snail!: Dream Castle` (`id=82864`, author `GiantLNT`, license `CC4-BY-NC-SA`).

# PyxelPico Games Porting Backlog

This backlog drives proactive PICO-8 → PyxelPico porting from easy to hard.

Policy:

- Start at the first `todo` candidate.
- Before implementation, confirm license/source/cart URL.
- Mark `blocked` if the license/IP chain is unclear.
- Mark `done` only after metadata/attribution and at least cart build verification pass.
- Append implementation lessons to `porting-lessons.md` after every attempt.

## Candidates

### 1. 2048

- Status: done
- Difficulty: easiest
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=153397
- Cart: https://www.lexaloffle.com/bbs/cposts/179297.p8.png
- Why first: simple deterministic grid puzzle; low asset/audio complexity.
- Risks: NC-SA distribution constraints; verify original author/source metadata before shipping.
- 2026-05-26 port note: Confirmed FCDB metadata (`bbs_release.json` id/pid `179297`, tid `153397`, author `straversi`, license `CC4-BY-NC-SA`) and added `games/2048/2048.py`, cover, attribution, `games.toml`, and credits; `make cart-game GAME=2048 PYTHON=python3` passed.

### 2. XMAS Pong

- Status: done
- Difficulty: easy
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=153606
- Cart: https://www.lexaloffle.com/bbs/cposts/ra/ramgadofu-1.p8.png
- Why: tiny arcade loop; good input/collision/scoring smoke test.
- Risks: NC-SA distribution constraints.
- 2026-05-26 port note: Confirmed FCDB metadata (`bbs_release.json` id/pid `179971`, tid `153606`, author `ReturnOH`, license `CC4-BY-NC-SA`) and shipped `games/xmaspong/xmaspong.py`, cover, attribution, `games.toml`, and credits; `make cart-game GAME=xmaspong PYTHON=python3` passed. Cart code extraction is still unavailable locally for this newer slug-style cart, so this pass targets gameplay-equivalent Pong mechanics rather than line-by-line Lua parity.

### 3. Floppy Canary

- Status: blocked
- Difficulty: easy
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=153327
- Cart: https://www.lexaloffle.com/bbs/cposts/179054.p8.png
- Why: one-button runner; useful timing/feel exercise.
- Risks: tuning jump/gravity feel; NC-SA distribution constraints.
- 2026-05-26 block note: Same extraction/tooling issue as XMAS Pong (`https://www.lexaloffle.com/bbs/cposts/fl/floppycanary-2.p8.png` downloads, but current local parsing returns empty Lua), preventing reliable API audit before porting.

### 4. PicoSorter

- Status: blocked
- Difficulty: easy-medium
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=154317
- Cart: https://www.lexaloffle.com/bbs/cposts/da/daworunut-0.p8.png
- Why: likely manageable puzzle/arcade mechanics.
- Risks: inspect mechanics first; NC-SA distribution constraints.
- 2026-05-26 block note: Same extraction/tooling issue as XMAS Pong (`https://www.lexaloffle.com/bbs/cposts/da/daworunut-0.p8.png` downloads, but current local parsing returns empty Lua), preventing required cart/API inspection.

### 5. LightWalk

- Status: done
- Difficulty: medium
- License: CC BY-NC-SA 4.0 in local FCDB metadata; upstream GitHub repo currently has no standalone LICENSE file
- BBS: https://www.lexaloffle.com/bbs/?tid=154308
- Cart: https://www.lexaloffle.com/bbs/cposts/li/lightwalk-0.p8.png
- GitHub: https://github.com/juliusspeak/lightwalk/
- Why: strong grid/maze puzzle candidate with source trail.
- Risks: NC-SA distribution constraints; upstream license-file ambiguity (resolved by using BBS/FCDB license metadata).
- 2026-05-26 port note: Implemented `games/lightwalk/lightwalk.py` from upstream Lua sources (`cell.lua`, `grid.lua`, `game.lua`, `pointer.lua`) preserving generation, rotation, power propagation, and win checks; added attribution, cover, credits, and games manifest entry; `make cart-game GAME=lightwalk PYTHON=python3` passed.

### 6. Santaban

- Status: done
- Difficulty: medium
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=153450
- Cart: https://www.lexaloffle.com/bbs/cposts/sa/santaban-3.p8.png
- Why: deterministic Sokoban-like puzzle; good reusable grid engine exercise.
- Risks: map/level migration effort; NC-SA distribution constraints.
- 2026-05-26 port note: Confirmed FCDB metadata (`bbs_release.json` id/pid `179484`, tid `153450`, author `skutter-de`, license `CC4-BY-NC-SA`) and BBS slug cart URL (`/bbs/cposts/sa/santaban-3.p8.png`), decoded PXA-compressed cart Lua/map data for API audit, and shipped `games/santaban/santaban.py` + `santaban_data.py`, cover, attribution, `games.toml`, and credits; `make cart-game GAME=santaban PYTHON=python3` passed.

### 7. Field Jump

- Status: partial
- Difficulty: medium-hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=154315
- Cart: https://www.lexaloffle.com/bbs/cposts/fi/fieldjump-0.p8.png
- Why: side-scroller/platformer after simpler ports are proven.
- Risks: spawn pacing and collision feel; exact Lua/API parity blocked until local tooling decodes newer PICO-8 `pxa` compressed code.
- 2026-05-31 progress note: Confirmed FCDB metadata (`bbs_release.json` id/pid `181917`, tid `154315`, author `fieldjump`, license `CC4-BY-NC-SA`) and BBS cart URL. Downloaded/inspected cart shell: label and data extract, but Lua begins with PICO-8 0.2.7+ `pxa` compression unsupported by vendored `picotool`. Added first playable PyxelPico approximation (`games/fieldjump/fieldjump.py`), cover from cart label, attribution, manifest and credits; `make cart-game GAME=fieldjump PYTHON=python3` passed.

### 8. Office Hell

- Status: todo
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=154283
- Cart: https://www.lexaloffle.com/bbs/cposts/of/office_hell_1_0-0.p8.png
- Why: puzzle-platformer candidate once platformer helpers exist.
- Risks: higher polish cost.

### 9. PICO-BALL

- Status: todo
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=150620
- Cart: https://www.lexaloffle.com/bbs/cposts/171244.p8.png
- Why: physics/sports challenge after easier ports.
- Risks: physics and AI feel; higher asset/audio complexity.

### 10. Pico Valley

- Status: defer
- Difficulty: very hard
- License: CC BY-NC-SA 4.0 metadata, but derivative-IP risk
- BBS: https://www.lexaloffle.com/bbs/?tid=142915
- Cart: https://www.lexaloffle.com/bbs/cposts/150629.p8.png
- Local cart: `projects/pyxelpico/carts/picovalley-2.p8.png`
- Why deferred: large Stardew-style demake; poor baseline for clean preservation workflow.

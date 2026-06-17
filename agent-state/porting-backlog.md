# PyxelPico Games Porting Backlog

This backlog drives proactive PICO-8 → PyxelPico porting from easy to hard.

Policy:

- Start at the first `todo` candidate.
- Before implementation, confirm license/source/cart URL.
- Mark `blocked` if the license/IP chain is unclear.
- Mark `done` only after metadata/attribution and at least cart build verification pass.
- Append implementation lessons to `porting-lessons.md` after every attempt.

## Candidates

### Top 100 rank 2. Just One Boss

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=49234
- Cart: https://www.lexaloffle.com/bbs/cposts/49234.p8.png
- Local source trail: `projects/picovibe/carts/pico8pixelbomb/justoneboss-pico8gomod/justonebossmod.p8`
- Why: first eligible strict FCDB BBS top-100 candidate; local source/mod trail reduces extraction risk.
- Risks: full original has many boss phases, scripted animation/entity behaviors, sprite/audio polish, persistence, and hard mode; first port targets the core arena-boss loop rather than complete line-by-line parity.
- 2026-06-17 progress note: Added first playable PyxelPico adaptation (`games/justoneboss/justoneboss.py`) with host-tested core movement/collision/phase rules (`justoneboss_core.py`), cover, attribution, manifest, and credits; `python3 -m unittest tests.test_justoneboss_core`, `python3 -m py_compile ...`, and `make cart-game GAME=justoneboss PYTHON=python3` passed.

### Top 100 rank 4. Birds With Guns

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=45334
- Cart: https://www.lexaloffle.com/bbs/cposts/bi/birdswithguns-5.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Just One Boss; strong handheld action fit.
- Risks: original is a broad procedural train-wagon roguelike shooter with mouse/keyboard aiming, many weapons/birds/drops, particles, map generation, music, and boss logic; first pass targets a simplified handheld shooter loop.
- 2026-06-17 progress note: Extracted cart Lua/API using `scripts/pico8_cart_extract.py`; added first playable PyxelPico adaptation (`games/birdswithguns/birdswithguns.py`) with host-tested movement/shooting/weapon/wagon/boss rules (`birdswithguns_core.py`), cover, attribution, manifest, and credits; `python3 -m unittest tests.test_birdswithguns_core`, `python3 -m py_compile ...`, and `make cart-game GAME=birdswithguns PYTHON=python3` passed.

### Top 100 rank 8. High Stakes

- Status: partial
- Difficulty: medium-hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=40099
- Cart: https://www.lexaloffle.com/bbs/cposts/hi/highstakes-2.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate; card-deduction rules are a good fit for host-tested logic and handheld cursor controls.
- Risks: original has blood economy, unlock ladder, chained score mode, custom card/chip animations, bespoke sprites, and soundtrack; first pass targets the central vampire deduction round.
- 2026-06-17 progress note: Extracted cart Lua/API using `scripts/pico8_cart_extract.py`; added first playable PyxelPico adaptation (`games/highstakes/highstakes.py`) with host-tested deal/flip/hint/stab/pass rules (`highstakes_core.py`), cover, attribution, manifest, and credits; `python3 -m unittest tests.test_highstakes_core`, `python3 -m py_compile ...`, and `make cart-game GAME=highstakes PYTHON=python3` passed.

### Top 100 rank 12. Buns: Bunny survivor

- Status: partial
- Difficulty: medium-hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=48032
- Cart: https://www.lexaloffle.com/bbs/cposts/bu/bunnysurvivor-9.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after High Stakes; strong handheld fit because movement is D-pad friendly and weapons can remain automatic.
- Risks: original is a fuller survivor loop with sprite/audio polish, more enemy/weapon/upgrade variety, particles, and stage pacing; first pass targets the core bunny movement, auto-fire, gems/XP, upgrades, boss timer, win, and loss loop.
- 2026-06-17 progress note: Extracted cart Lua/API using `scripts/pico8_cart_extract.py`; added first playable PyxelPico adaptation (`games/buns/buns.py`) with host-tested movement/spawn/auto-fire/gem/upgrade/damage/boss rules (`buns_core.py`), cover, attribution, manifest, and credits; `python3 -m unittest tests.test_buns_core`, combined top-100 core tests, `python3 -m py_compile ...`, and `make cart-game GAME=buns PYTHON=python3` passed.

### Top 100 rank 13. Porklike

- Status: partial
- Difficulty: medium-hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=37045
- Cart: https://www.lexaloffle.com/bbs/cposts/po/porklike-2.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Buns; turn-based grid roguelike rules are a good fit for D-pad controls and host-tested core logic.
- Risks: FCDB numeric cart URL 404s and the live slug cart downloads but current local extraction returns empty Lua from the old `:c:` compressed code region; first pass targets a compact turn-based dungeon adaptation rather than exact map/item/enemy parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license/cart metadata and downstream FCDB consumers; added first playable PyxelPico adaptation (`games/porklike/porklike.py`) with host-tested dungeon generation, movement, bump combat, item pickup, enemy turn, and exit rules (`porklike_core.py`), cover, attribution, manifest, and credits; `python3 -m unittest tests.test_porklike_core`, combined top-100 core tests, `python3 -m py_compile ...`, and `make cart-game GAME=porklike PYTHON=python3` passed.

### Top 100 rank 14. PICOWARE

- Status: partial
- Difficulty: very hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=34751
- Cart: https://www.lexaloffle.com/bbs/cposts/pi/picoware-20.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Porklike; strong handheld fit as a short-session microgame collection.
- Risks: original is a 50+ developer collaboration with 68 microgames across subcarts, saved progress, menus, credits, and many bespoke rules; first pass targets a compact timed microgame-rush subset rather than full subcart parity.
- 2026-06-17 progress note: Extracted cart Lua/API using `scripts/pico8_cart_extract.py` and confirmed BBS thread scope; added first playable PyxelPico adaptation (`games/picoware/picoware.py`) with host-tested round start, prompt input, dodge, mash, countdown, result, score, life, and game-over rules (`picoware_core.py`), cover, attribution, manifest, and credits; `python3 -m unittest tests.test_picoware_core`, combined top-100 core tests, `python3 -m py_compile ...`, and `make cart-game GAME=picoware PYTHON=python3` passed.

### Top 100 rank 17. Marble Merger

- Status: blocked
- Difficulty: medium-hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=54837
- Cart: https://www.lexaloffle.com/bbs/cposts/ma/marble_merger-5.p8.png
- Why blocked: FCDB tags include `suika` and `watermelon`, indicating an obvious Suika Game / watermelon-game derivative risk. The migration policy blocks commercial-IP demakes/mods unless an explicit approved rights chain exists.
- 2026-06-17 block note: Updated `scripts/pico8_top100_status.py` so derivative-IP detection also scans FCDB tags, not only name/slug/description. Marble Merger now classifies as `blocked-ip-risk` instead of `todo`.

### Top 100 rank 18. Mai-Chan's Sweet Buns

- Status: partial
- Difficulty: medium
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=31864
- Cart: https://www.lexaloffle.com/bbs/cposts/5/56576.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after blocking Marble Merger; original author/license are clear and the bakery premise fits compact handheld controls.
- Risks: FCDB's stored `56575.p8.png` cart URL 404s; BBS thread exposes live cart `56576.p8.png`, which downloads but extracts as empty Lua with the current local tool. First pass targets a bakery order-matching loop rather than exact recipe/timing/sprite parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata and corrected the live cart URL from the BBS thread; added first playable PyxelPico adaptation (`games/maichanssweetbuns/maichanssweetbuns.py`) with host-tested order generation, tray matching, wrong-bun penalties, serving, timer, score, day, and game-over rules (`maichanssweetbuns_core.py`), cover, attribution, manifest, and credits; `python3 -m unittest tests.test_maichanssweetbuns_core`, combined top-100 core tests, `python3 -m py_compile ...`, and `make cart-game GAME=maichanssweetbuns PYTHON=python3` passed.

### Top 100 rank 24. X-Zero

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=36053
- Cart: https://www.lexaloffle.com/bbs/cposts/xz/xzero-3.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Mai-Chan's Sweet Buns; BBS comments confirm platforming and shooting with jump/shoot controls and map randomization.
- Risks: live slug cart downloads but extracts as empty Lua with the current local tool. First pass targets a compact side-view platform-shooter loop rather than exact prefab map, aiming, level, sprite, and soundtrack parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license/cart metadata and BBS gameplay-control clues; added first playable PyxelPico adaptation (`games/xzero/xzero.py`) with host-tested movement, jumping, shooting, enemy hits, contact damage, pickups, zone exits, and final clear rules (`xzero_core.py`), cover, attribution, manifest, and credits; `python3 -m unittest tests.test_xzero_core`, combined top-100 core tests, `python3 -m py_compile ...`, and `make cart-game GAME=xzero PYTHON=python3` passed.

### Top 100 rank 26. Pico World Race 1.2

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=46495
- Cart: https://www.lexaloffle.com/bbs/cposts/pp/ppwr-5.p8.png
- GitHub: https://github.com/PAK9/PicoWorldRace
- Why: next eligible strict FCDB BBS top-100 candidate after X-Zero; cart extracts cleanly and BBS thread documents fast racing, 8 themed races, 8 opponents, 20 tokens per race, and custom/random tracks.
- Risks: original is a polished racing game with campaign progression, custom track generation, profile saves, many tracks/opponents, token placement, sprite art, music, and tuned physics; first pass targets a compact racing loop with gas/steer/drift/laps/tokens/opponents.
- 2026-06-17 progress note: Extracted cart Lua/API using `scripts/pico8_cart_extract.py`; added first playable PyxelPico adaptation (`games/picoworldrace/picoworldrace.py`) with host-tested acceleration, steering, drift, off-track penalty, token crossing, laps, finish, and opponent progress rules (`picoworldrace_core.py`), cover, attribution, manifest, and credits; `python3 -m unittest tests.test_picoworldrace_core`, combined top-100 core tests, `python3 -m py_compile ...`, and `make cart-game GAME=picoworldrace PYTHON=python3` passed.

### Top 100 rank 27. Combo Pool

- Status: partial
- Difficulty: medium-hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=3467
- Cart: https://www.lexaloffle.com/bbs/cposts/co/combopool-0.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Pico World Race; BBS thread clearly describes colored marble merging, score combos, rebound scoring, life pressure from too many/dark balls, and fine aim controls.
- Risks: live slug cart downloads but local extraction returns only shallow output with no useful API surface. First pass targets the BBS-described merge-pool loop rather than exact physics/difficulty/sprite/audio parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license/cart metadata and BBS gameplay notes; added first playable PyxelPico adaptation (`games/combopool/combopool.py`) with host-tested aim rotation, shooting, wall rebounds, same-color merges, scoring, combo, life pressure, win, and loss rules (`combopool_core.py`), cover, attribution, manifest, and credits; `python3 -m unittest tests.test_combopool_core`, combined top-100 core tests, `python3 -m py_compile ...`, and `make cart-game GAME=combopool PYTHON=python3` passed.

### Top 100 rank 32. Into Ruins

- Status: partial
- Difficulty: very hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=49928
- Cart: https://www.lexaloffle.com/bbs/cposts/in/intoruins-7.p8.png
- GitHub: https://github.com/Woflox/intoruins
- Why: next eligible strict FCDB BBS top-100 candidate after Combo Pool; turn-based roguelike play maps well to D-pad controls and host-tested core rules.
- Risks: original is a dense Brogue-inspired hex/isometric roguelike with many weapons, staffs, orbs, creatures, terrain interactions, fire/light/freezing, pits, physics-like object behavior, music, and extensive emergent rules; first pass targets a compact ruins descent loop rather than full interaction parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license/cart metadata, BBS goal text, upstream GitHub source trail, and extractable Lua/API surface using `scripts/pico8_cart_extract.py`; added first playable PyxelPico adaptation (`games/intoruins/intoruins.py`) with host-tested movement, bump combat, visibility/exploration, burn/freeze status, ranged enemy, item, descent, win, and loss rules (`intoruins_core.py`), cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=intoruins PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 35. To a Starling

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=45958
- Cart: https://www.lexaloffle.com/bbs/cposts/to/to_a_starling-0.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Into Ruins; extracted Lua shows platformer/adventure/puzzle rules that fit handheld D-pad plus A/B controls.
- Risks: original is a room-based puzzle platform adventure with authored maps, camera transitions, teleport/portal behavior, merchants, cartdata persistence, music, animation polish, and wider progression; first pass targets a compact movement/puzzle loop rather than full map/source parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license/cart metadata and extractable Lua/API surface using `scripts/pico8_cart_extract.py`; added first playable PyxelPico adaptation (`games/toastarling/toastarling.py`) with host-tested acceleration/friction, coyote jump, glide, berry/key collection, locked door, switch/bridge, checkpoint, hazard, and clear rules (`toastarling_core.py`), cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=toastarling PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 36. Woodworm

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=142717
- Cart: https://www.lexaloffle.com/bbs/cposts/wo/woodworm-0.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after To a Starling; extracted Lua and BBS comments confirm a puzzle game well suited to D-pad movement and undo.
- Risks: original has authored puzzle levels, level select, save progress, custom font/UI, falling animation polish, jar/cabinet presentation, and cake ending; first pass targets a compact Snakebird-like wood-eating loop rather than full level/source parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license/cart metadata and extractable Lua/API surface using `scripts/pico8_cart_extract.py`; added first playable PyxelPico adaptation (`games/woodworm/woodworm.py`) with host-tested worm movement, reverse blocking, wood eating, undo, gravity, and clear rules (`woodworm_core.py`), cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=woodworm PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 37. BAS

- Status: partial
- Difficulty: medium-hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=54986
- Cart: https://www.lexaloffle.com/bbs/cposts/ba/bas-9.p8.png
- GitHub: https://github.com/yokoboko/bas-pico-8
- Why: next eligible strict FCDB BBS top-100 candidate after Woodworm; BBS describes an endless wall-jump highscore game with simple handheld-friendly left/right inputs.
- Risks: original has polished easing, sprite animation, music, transitions, highscore persistence, and procedural saw pacing; first pass targets the core wall-jump/saw/trap loop rather than full source parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license/cart metadata, author-owned demake description, GitHub source trail, and extractable Lua/API surface using `scripts/pico8_cart_extract.py`; added first playable PyxelPico adaptation (`games/bas/bas.py`) with host-tested jump targeting, mid-air retargeting, saw collision prediction/collision, trap death, saw spawning, score, highscore, and restart rules (`bas_core.py`), cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=bas PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 41. UFO Swamp Odyssey

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=38153
- Cart: https://www.lexaloffle.com/bbs/cposts/uf/ufo-0.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after BAS; short atmospheric platformer/metroidvania premise fits D-pad plus A/B controls.
- Risks: FCDB numeric cart URL 404s and the live cart path comes from the BBS thread; original has authored map flow, dialogue/story pacing, custom sprite/palette work, water/swamp effects, enemies, portals, grapple hooks, SFX/music, and transition polish. First pass targets a compact platform-adventure loop rather than full map/source parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata and corrected live cart URL from the BBS thread; extracted usable Lua/API surface with `scripts/pico8_cart_extract.py`; added first playable PyxelPico adaptation (`games/ufoswamp/ufoswamp.py`) with host-tested movement, jump, water buoyancy, score/zapper pickups, enemy stun, portal teleport, grapple pull, and EMP-cannon disable rules (`ufoswamp_core.py`), cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=ufoswamp PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 42. PICORACER-2048

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=2243
- Cart: https://www.lexaloffle.com/bbs/cposts/1/16305.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after UFO Swamp Odyssey; vector-racer premise fits D-pad plus A/B controls and host-tested deterministic racing rules.
- Risks: FCDB numeric cart URL 404s and the live cart path comes from the BBS thread; local extractor returns empty Lua/API and the source snippet endpoint depends on Lexaloffle browser cart tooling. Original has 4 speed classes, 8 looping tracks, 3 laps, narrowing tracks, boost/brake/air-brake feel, wall-impact polish, AI/ghost racers, track editor/storage, music, and vector effects; first pass targets a compact racing loop rather than full handling/source parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata and corrected live cart URL from the BBS thread; added first playable PyxelPico adaptation (`games/picoracer2048/picoracer2048.py`) with host-tested acceleration, braking, boost pads, curve drift, steering, wall-hit slowdown, lap/finish timing, and AI pressure rules (`picoracer2048_core.py`), cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=picoracer2048 PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 44. Air Delivery

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=52598
- Cart: https://www.lexaloffle.com/bbs/cposts/ai/air_delivery_1-3.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after PICORACER-2048; short sky-island delivery metroidvania premise fits D-pad plus A/B controls.
- Risks: FCDB numeric cart URL 404s and the live cart path comes from the BBS thread; local extraction exposes only partial Lua/API and mostly sprite/string data. Original has a dense world, 9 letters/packages, recipients with dialogue/rewards, coyote jump, ladder handling, glider precision, secrets/drill passage, music, sprite polish, and ending flow; first pass targets a compact delivery-platformer loop rather than full map/source parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, documented BBS controls and changelog, corrected live cart URL from the BBS thread, and extracted partial Lua/API surface with `scripts/pico8_cart_extract.py`; added first playable PyxelPico adaptation (`games/airdelivery/airdelivery.py`) with host-tested movement, ladder climb, coyote jump, glide, letter collection, recipient delivery, reward unlocks, drill passage, hazard respawn, and airship completion rules (`airdelivery_core.py`), cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=airdelivery PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 45. Demon Castle

- Status: blocked
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=34805
- Cart: https://www.lexaloffle.com/bbs/cposts/de/demon_castle-1.p8.png
- Why blocked: FCDB tags include `castlevania`, the BBS description says "Demon Castle is a Castlevania-style game for PICO-8", controls center on a whip, and comments compare it directly to multiple Castlevania entries. The migration policy blocks commercial-IP demakes/mods or close derivative recreations unless an explicit approved rights chain exists.
- 2026-06-17 block note: Updated `scripts/pico8_top100_status.py` so derivative-IP detection scans `castlevania` in FCDB tags/name/slug/description. Demon Castle now classifies as `blocked-ip-risk` instead of `todo`.

### Top 100 rank 46. Marballs 2

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=28414
- Cart: https://www.lexaloffle.com/bbs/cposts/ma/marballs_2-0.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after blocking Demon Castle; rolling-ball platformer loop fits D-pad controls and host-tested physics/progression rules.
- Risks: FCDB numeric cart URL 404s and the live cart path comes from the BBS thread; local extraction exposes title data and the level table but no useful API scan. Original has many official levels, custom cart/level packs, nuanced collision and wall-bounce routing, level select, save data, ace/gold timing, music, and intro polish; first pass targets a compact rolling/orb/jump-pad loop rather than full level/source parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, documented BBS controls and custom-level notes, corrected live cart URL from the BBS thread, and extracted partial Lua level-table data with `scripts/pico8_cart_extract.py`; added first playable PyxelPico adaptation (`games/marballs2/marballs2.py`) with host-tested rolling acceleration/friction, jump pads, orb collection, orb-gated goal, wall bounce, medal timing, and rotated-control rules (`marballs2_core.py`), cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=marballs2 PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 48. Freezing Knights

- Status: partial
- Difficulty: very hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata and upstream GitHub source
- BBS: https://www.lexaloffle.com/bbs/?tid=50683
- Cart: https://www.lexaloffle.com/bbs/cposts/fr/freezing_knights-9.p8.png
- GitHub: https://github.com/tinyevilwizard/FreezingKnights
- Why: next eligible strict FCDB BBS top-100 candidate after Marballs 2; source and BBS thread clearly document a two-knight co-op turn-based RPG with mountain progression, timed defensive inputs, rest/safe zones, upgrades, and many encounters.
- Risks: original is a large 14-cart RPG with authored map progression, two-player controls, 30 encounters, 11 enemy types, 14 music tracks, hard mode, persistence, menus, custom sprites, and ending flow. It is explicitly inspired by turn-based RPGs with timing-defense mechanics; first pass avoids third-party branded characters/assets and targets a compact generic two-knight snowy RPG loop rather than full multicart/source parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, BBS live cart URL, and author-owned GitHub source under CC BY-NC-SA 4.0; added first playable PyxelPico adaptation (`games/freezingknights/freezingknights.py`) with host-tested path selection, attacks, timed defense, rest recovery, upgrades, and party-wipe fallback (`freezingknights_core.py`), cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=freezingknights PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 49. The Lost Night Release

- Status: partial
- Difficulty: medium-hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=41791
- Cart: https://www.lexaloffle.com/bbs/cposts/th/the_lost_night-6.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Freezing Knights; live cart extracts usable Lua/API and the visible mechanics fit handheld D-pad plus A/B controls.
- Risks: FCDB tags include `earthbound`, and BBS comments mention Mother/Undertale vibes. No explicit demake/brand-copy premise was found in the BBS title/thread evidence, so this pass avoids third-party branded characters/assets and targets a generic night RPG/shooter adaptation. Original has authored maps, enemy patterns, dialogue, music, persistence, shop/menu polish, and exact battle tuning outside the first playable scope.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, live cart URL, and extractable Lua/API surface using `scripts/pico8_cart_extract.py`; added first playable PyxelPico adaptation (`games/lostnight/lostnight.py`) with host-tested room traversal, encounter start, bullet damage/dodging, enemy defeat, tea healing, candy upgrades, room clears, and dawn unlock (`lostnight_core.py`), cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=lostnight PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 51. Nanoman

- Status: blocked
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=29017
- Cart: https://www.lexaloffle.com/bbs/cposts/38516.p8.png
- Why blocked: FCDB tags include `megaman`, the BBS description says it is "a fan game heavily inspired by the early Mega Man series", says Mega Man fans "should feel right at home", and later comments compare it directly to Mega Man. The migration policy blocks commercial-IP demakes/mods or close fan-game recreations unless an explicit approved rights chain exists.
- 2026-06-17 block note: Updated `scripts/pico8_top100_status.py` so `megaman`, `mega man`, and `rockman` tags/name/slug/description classify as derivative-IP risk. Nanoman now classifies as `blocked-ip-risk` instead of `todo`.

### Top 100 rank 52. Pico Checkmate

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=31213
- Cart: https://www.lexaloffle.com/bbs/cposts/5/54038.p8.png
- Itch: https://krystman.itch.io/pico-checkmate
- Why: next eligible strict FCDB BBS top-100 candidate after blocking Nanoman; classic chess is license/IP-safe, handheld-friendly, and BBS docs explicitly call out full chess rules with basic AI and no threefold repetition.
- Risks: live cart downloads but local extraction returns empty Lua/API, so this pass is a manual rules-based adaptation. Original has polished animations, exact AI evaluation/search, two-human mode, music, and visual assets; first pass targets legal movement, check states, core special moves, and simple AI rather than full original parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, live cart URL, BBS gameplay/rule notes, and extraction blocker; added first playable PyxelPico adaptation (`games/picocheckmate/picocheckmate.py`) with host-tested legal piece movement, check safety, castling, en passant, promotion, checkmate, and simple capture-biased AI (`picocheckmate_core.py`), cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=picocheckmate PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 55. Little Dragon Adventure

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=31469
- Cart: https://www.lexaloffle.com/bbs/cposts/5/53895.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Pico Checkmate; original premise and comments describe a cute dragon metroidvania/platform adventure with eggs to rescue, fireballs, double jump, checkpoints, enemies, bosses, and low-pressure gamepad-friendly movement.
- Risks: live cart downloads but local extraction returns empty Lua/API. Original has an authored metroidvania map, reused room tricks, boss fights, challenge mode, exact enemy patterns, checkpoints, music, sprite work, and ending surprise; first pass targets a compact dragon/egg/fireball/checkpoint/boss loop rather than full source/map parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, live cart URL, BBS premise/control/combat notes, and extraction blocker; added first playable PyxelPico adaptation (`games/littledragon/littledragon.py`) with host-tested movement, double jump, fireball hits, egg rescue, checkpoint respawn, hazards, boss gating, and clear rules (`littledragon_core.py`), cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=littledragon PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 59. Trial of the Sorcerer

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=43833
- Cart: https://www.lexaloffle.com/bbs/cposts/mo/mot_sorcerer-11.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Little Dragon Adventure; original thread describes an original procedural 3D first-person dungeon shooter with staff shots, monsters, loot, keys, locked doors, exits, and power crystals, all mappable to handheld D-pad plus A/B controls.
- Risks: FCDB's numeric cart URL 404s; the BBS thread exposes the slug cart URL. Source extraction works, but the original is a dense raycast/FPS cart with custom dungeon generation, GUI/menu code, mouse/controller options, several enemy types, music, exact procedural layouts, and renderer tricks outside this first playable pass. The BBS says it is inspired by Wolfenstein 3D and Catacomb Abyss; no third-party branded characters/assets are copied, and this pass uses generic sorcerer/demon-realm presentation.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, corrected live cart URL, BBS mechanics/control notes, and extractable source; added first playable PyxelPico adaptation (`games/trialsorcerer/trialsorcerer.py`) with host-tested procedural dungeon setup, turn/forward/strafe movement, staff shots, monster defeat, loot, key pickup, locked door opening, crystal staff upgrades, exit level transitions, and final boss clear rules (`trialsorcerer_core.py`), cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=trialsorcerer PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 60. MOTION.REC

- Status: partial
- Difficulty: medium-hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=53392
- Cart: https://www.lexaloffle.com/bbs/cposts/mo/motionrec-3.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Trial of the Sorcerer; BBS describes an original action-puzzle platformer centered on recording movement, replaying it, and replaying it in reverse, which maps well to host-tested mechanics and handheld D-pad plus A/B controls.
- Risks: FCDB's numeric cart URL 404s; the BBS thread exposes the slug cart URL. Source extraction works and the source credits @matthughson's Advanced Micro Platformer Starter Kit. The BBS links commercial Steam/itch releases, so this pass uses the CC4 BBS cart metadata and avoids copying external store assets. Original authored levels, exact physics, visual mode effects, speedrun route tuning, full animation, music, and softlock-proof puzzle design are outside this first playable pass.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, corrected live cart URL, BBS controls/mechanics, Steam/itch/source-template context, and extractable source; added first playable PyxelPico adaptation (`games/motionrec/motionrec.py`) with host-tested movement, jump/landing, motion recording, infinite replay, reverse replay, recorded clone switch activation, goal unlock, clear, and level-reset rules (`motionrec_core.py`), cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=motionrec PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 61. P.Craft

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=3200
- Cart: https://www.lexaloffle.com/bbs/cposts/2/24981.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after MOTION.REC; BBS describes a deserted-island crafting/survival game where the player gathers materials, builds tools, explores a cave, crafts a sword, and crafts a boat to escape.
- Risks: FCDB's numeric cart URL 404s; the BBS thread exposes the live cart plus an older cart. Local extraction of the live cart returns no usable Lua/API text. The BBS says the game is heavily inspired by Notch's Ludum Dare game Minicraft and links later P.Craft Deluxe / Stranded Isle releases, so this pass avoids external release assets and uses generic island survival presentation. Original procedural map generation, large item/crafting list, hunger/stamina/combat/menu polish, cave/boss flow, music, sprites, and exact token-packed systems are outside this first playable pass.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, corrected live cart URL, BBS controls/mechanics, Minicraft inspiration context, later Deluxe/Stranded Isle context, and extraction blocker; added first playable PyxelPico adaptation (`games/pcraft/pcraft.py`) with host-tested seeded island resources, gathering, workbench crafting, axe wood yield, sword-gated cave crystal, boat recipe, shore escape, cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=pcraft PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 62. 8 Legs to Love

- Status: partial
- Difficulty: medium-hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=29451
- Cart: https://www.lexaloffle.com/bbs/cposts/4/41422.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after P.Craft; BBS describes an original spider web-building arcade game with simple D-pad movement, hold/tap web placement, timed levels, and bug scoring.
- Risks: FCDB's numeric cart URL is stale; the BBS thread exposes the live cart URL. Local extraction of the live cart returns no useful Lua/API text, so this pass is based on FCDB/BBS mechanics evidence. Original six-level layouts, exact web physics, climbing feel, bug spawn patterns, sprite/audio polish, and scoring/timer tuning are outside this first playable pass.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, corrected live cart URL, BBS controls/mechanics, beetle and butterfly score notes, and extraction blocker; added first playable PyxelPico adaptation (`games/eightlegslove/eightlegslove.py`) with host-tested spider movement, web strand placement, fly catch scoring, beetle web damage, butterfly high-value catch, level clear, cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=eightlegslove PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 64. Guncho

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=48452
- Cart: https://www.lexaloffle.com/bbs/cposts/gu/guncho-3.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after 8 Legs to Love; original PICO-8 cart has clear CC metadata, extractable source, and a tactical turn-based western loop that maps to handheld D-pad plus A/B controls.
- Risks: The PICO-8 cart credits an original 7DRL game by Arnold Rauers and Terri Vellman and links later commercial releases. This pass uses the CC BY-NC-SA BBS cart as source evidence and avoids copying later commercial assets. Original procedural camp generation, exact AI, full action UI, sprint subturns, walls/fences/traps, music, sprite polish, and balance tuning are outside this first playable pass.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, corrected live cart URL, extracted source/API, BBS controls/mechanics, original 7DRL credit trail, and later commercial-release caveat; added first playable PyxelPico adaptation (`games/guncho/guncho.py`) with host-tested hex movement, revolver shoot/reload, punch/stun, dynamite countdown/explosion, enemy turns, camp clear, boss victory, cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=guncho PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 65. Rolly

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=31526
- Cart: https://www.lexaloffle.com/bbs/cposts/5/54262.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Guncho; original thread describes a high-polish precision platformer with jump, roll, hop, dive, caves, friends to rescue, and controller-friendly play.
- Risks: FCDB's numeric cart URL 404s; the BBS thread exposes the live cart URL. Local extraction of the live cart returns no usable Lua/API text, so this pass is based on FCDB/BBS mechanics evidence. Original authored levels, exact physics, wall-grab/jump tuning, screen transitions, sprites, music by Rory, death timing, save/progress behavior, and full challenge curve are outside this first playable pass.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, corrected live cart URL, BBS controls/mechanics, itch/controller context, and extraction blocker; added first playable PyxelPico adaptation (`games/rolly/rolly.py`) with host-tested walking, jumping, roll/hop boost, orb recharge, spike respawn/death count, friend rescue, exit clear, cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=rolly PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 68. pigments

- Status: partial
- Difficulty: medium-hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=40490
- Cart: https://www.lexaloffle.com/bbs/cposts/pi/pigments-0.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Rolly; original tile-painting pursuit loop maps well to D-pad movement and host-tested grid rules.
- Risks: FCDB's numeric cart URL 404s; the BBS thread exposes the live slug cart URL. Local extraction produces readable but obfuscated Lua/mechanic strings, so this pass targets the BBS-described apple-style core loop rather than full fruit unlock/highscore progression, exact disc behavior, sprite/audio polish, save formatting, or all level variants.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, corrected live cart URL, BBS goal/special-tile mechanics, and extractable obfuscated source strings; added first playable PyxelPico adaptation (`games/pigments/pigments.py`) with host-tested tile painting, pigment droplets, razor disc pursuit, grass blocking, water hiding/pigment spend, trigger dashes, full-paint clear, cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=pigments PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 69. Cherry Bomb

- Status: partial
- Difficulty: medium-hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=48986
- Cart: https://www.lexaloffle.com/bbs/cposts/ch/cherrybomb-0.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after pigments; original arcade shmup has clear controls, wave/life/cherry/bomb rules, and an extractable source/API surface.
- Risks: FCDB's numeric cart URL 404s; the BBS thread exposes the live slug cart URL. Original is a tutorial game reminiscent of Space Invaders/Galaga, so this pass keeps generic alien/ship presentation and avoids copying those franchises. Exact enemy formations, title/logo animation, highscore persistence, sprite art, Sebastian Hassler's original music, and full source tutorial structure are outside this first playable pass.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, corrected live cart URL, BBS controls/scoring/pickup mechanics, and extractable Lua/API surface; added first playable PyxelPico adaptation (`games/cherrybomb/cherrybomb.py`) with host-tested movement bounds, shooting, enemy hits, enemy bullets/lives, cherry pickup heart/bonus logic, bomb clearing, wave advance/victory, cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=cherrybomb PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 71. Breakout Hero

- Status: blocked
- Difficulty: medium-hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=31484
- Cart: https://www.lexaloffle.com/bbs/cposts/5/53976.p8.png
- Why blocked: The BBS description explicitly calls the cart "a juicy remake of Breakout/Arkanoid". The migration policy blocks commercial-IP demakes/remakes unless an explicit approved rights chain exists, even when the cart itself has CC metadata.
- 2026-06-17 block note: Updated `scripts/pico8_top100_status.py` so `arkanoid` and the specific `breakout hero` title classify as `blocked-ip-risk` instead of `todo`.

### Top 100 rank 72. Advanced Micro Platformer - Starter Kit

- Status: partial
- Difficulty: medium
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=28793
- Cart: https://www.lexaloffle.com/bbs/cposts/3/37402.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after blocking Breakout Hero; although it is a starter kit rather than a full game, the ranked FCDB cart is redistributable and can be represented as a playable PyxelPico demo of the documented platformer mechanics.
- Risks: FCDB's numeric cart URL is stale; the BBS thread exposes the live starter-kit cart. The same BBS thread also includes a separate Super Mario Bros. cart, so this pass excludes that cart and all third-party branded assets. Local extraction of the starter-kit cart returns no useful Lua/API text. Original animation system, collision implementation, camera shake, map data, sprite art, and tutorial code organization are outside this first playable pass.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, corrected live cart URL, BBS starter-kit mechanics, and extraction blocker; added first playable PyxelPico demo (`games/advancedmicroplatformer/advancedmicroplatformer.py`) with host-tested running/friction, coyote jump, buffered jump, variable jump height, one-way platforms, camera threshold, goal clear, cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=advancedmicroplatformer PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 73. Scrap Boy

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=39800
- Cart: https://www.lexaloffle.com/bbs/cposts/sc/scrap_boy-6.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Advanced Micro Platformer; original action-platformer has clear author/license metadata, BBS mechanics notes, and an extractable Lua/API surface.
- Risks: FCDB's numeric cart URL 404s; the BBS thread exposes the live slug cart URL. BBS comments describe it as Mega Man-like, so this pass avoids third-party branding/assets and uses generic robot/scrap presentation. Original 3 levels, 6 complete weapons, 3 difficulties, collectibles/time attack, exact maps, sprite art, music, pause button-swap, and speedrun tuning are outside this first playable pass.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, corrected live cart URL, BBS mechanics/comments, and extractable Lua/API surface; added first playable PyxelPico adaptation (`games/scrapboy/scrapboy.py`) with host-tested movement, jumping, laser shots, bomb door opening, spike damage/immunity, magnet wall-jump, scrap pickup, exit clear, cover, attribution, manifest, and credits; combined top-100 core tests, `python3 -m py_compile ...`, `make cart-game GAME=scrapboy PYTHON=python3`, and `git diff --check` passed.

### Top 100 rank 74. Shadows of Dunwich 2.0

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=34047
- Cart: https://www.lexaloffle.com/bbs/cposts/sh/shadowsofdunwich-4.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Scrap Boy; original turn-based squad tactics maps cleanly to host-tested deterministic rules and D-pad cursor controls.
- Risks: The live cart downloads but current local extraction returns empty Lua/API text. Original procedural maps, 3D sprite system, full talent tree, 16-level balance, save behavior, exact enemies, original sprite art, music, and visual flair are outside this first playable pass. BBS text calls it X-Com-like, so this pass uses generic occult squad-tactics presentation and no third-party branded assets.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, corrected live cart URL, BBS mechanics/campaign notes, and extraction limitation; added first playable PyxelPico adaptation (`games/shadowsofdunwich/shadowsofdunwich.py`) with host-tested action points, squad movement, shooting, grenades, enemy turns, splitter spawns, soldier leveling, recruit replacement, campaign advancement, level-16 victory, cover, attribution, manifest, and credits; verification pending in this session note until the final command pass completes.

### Top 100 rank 75. Pico Tennis

- Status: partial
- Difficulty: medium-hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=31450
- Cart: https://www.lexaloffle.com/bbs/cposts/pi/picotennis2-0.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Shadows of Dunwich 2.0; tennis maps cleanly to a compact handheld loop with D-pad movement, A hit/serve, and B power shot.
- Risks: FCDB's numeric cart URL 404s; the live slug cart downloads but current local extraction returns empty Lua/API text. Original 3D rendering system, multiplayer, exact ball physics, full AI, original sprite/label art, and music are outside this first playable pass.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, corrected live cart URL, BBS controls/scoring/mechanics notes, and extraction limitation; added first playable PyxelPico adaptation (`games/picotennis/picotennis.py`) with host-tested serve, rally, offset-based shot angle, power meter, power shots, fault/out scoring, games, sets, match victory, cover, attribution, manifest, and credits; verification pending in this session note until the final command pass completes.

### Top 100 rank 76. Driftmania

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=140202
- Cart: https://www.lexaloffle.com/bbs/cposts/dr/driftmania-5.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Pico Tennis; original time-trial drift racing has clear controls, track/medal goals, and an extractable cart.
- Risks: The original credits music by Vav, cars based on art by PixelArtM, cover art by TerracotaScarf, and helper/inspiration credits; this first pass uses procedural replacement art/audio and records the upstream chain. Full 15-track campaign, ghost replay, garage customization, options, exact 3D sprite-stacking rendering, and speedrun tuning are outside this first playable pass.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, live cart URL, BBS controls/track/medal/contributor notes, and extractable minified Lua; added first playable PyxelPico adaptation (`games/driftmania/driftmania.py`) with host-tested acceleration, braking/reverse, steering, drift-brake rotation, grass traction, boost tiles, checkpoints, lap timing, medal scoring, cover, attribution, manifest, and credits; verification pending in this session note until the final command pass completes.

### Top 100 rank 79. Wobblepaint 1.6

- Status: partial
- Difficulty: medium
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=40058
- Cart: https://www.lexaloffle.com/bbs/cposts/wo/wobblepaint-6.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Driftmania; although it is a paint tool, the BBS explicitly documents gamepad controls that fit Pico8Go handheld input.
- Risks: FCDB's numeric cart URL is stale and local extraction returns empty Lua/API text for the live cart. Original menus, presets, pattern/shape system, multi-doodle storage, paste/export format, GIF capture, self-saving cart data, and exact wobble rendering are outside this first playable pass.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, live cart URL, BBS gamepad/tool controls, and extraction limitation; added first playable PyxelPico adaptation (`games/wobblepaint/wobblepaint.py`) with host-tested cursor movement, brush dabs, color cycling, brush sizing, undo, clear, wobble animation, cover, attribution, manifest, and credits; verification pending in this session note until the final command pass completes.

### Top 100 rank 80. Whiplash Taxi Co

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=53583
- Cart: https://www.lexaloffle.com/bbs/cposts/mo/mot_taxi-7.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Wobblepaint; original passenger-delivery driving loop has clear source/license evidence and an extractable cart.
- Risks: BBS comments compare it to Crazy Taxi/GTA, so this pass uses generic taxi delivery presentation and no third-party branded assets. Original 3D rendering, Motsville map, AI traffic, free-explore/race modes, lap records, music, exact driving feel, and full customer set are outside this first playable pass.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, live cart URL, BBS pickup/destination/timer/free-explore/race notes, deliberate reverse behavior, and extractable Lua/API; added first playable PyxelPico adaptation (`games/whiplashtaxi/whiplashtaxi.py`) with host-tested acceleration, steering, stop-before-reverse, crash bounce, passenger pickup, destination dropoff, fare scoring, five-minute timer, cover, attribution, manifest, and credits; verification pending in this session note until the final command pass completes.

### Top 100 rank 81. Night Ride

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=39650
- Cart: https://www.lexaloffle.com/bbs/cposts/ni/nightride-0.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Whiplash Taxi Co; original night driving/shooter/boss loop has clear source/license evidence and extractable cart code.
- Risks: BBS comments compare it to Spy Hunter, so this pass uses generic night-road shooter presentation and no third-party branded assets. Original level scripts, particles, car rotation art, traffic variety, music, exact shooting escalation, boss patterns, and sunrise ending art are outside this first playable pass.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, live cart URL, BBS night-driving/shooter/boss notes, and extractable Lua/API; added first playable PyxelPico adaptation (`games/nightride/nightride.py`) with host-tested lane changes, traffic collisions, level progression, weapon unlock, shooting, boss damage, health, score, sunrise victory, cover, attribution, manifest, and credits; verification pending in this session note until the final command pass completes.

### Top 100 rank 85. Pico-8 Tunes Volume 1

- Status: partial
- Difficulty: medium
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=29008
- Cart: https://www.lexaloffle.com/bbs/cposts/3/38440.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Night Ride; BBS author text says the 12 two-channel tunes are intended for reuse, and Krajzeg confirms the code/sprites/assets are under the same Creative Commons umbrella.
- Risks: This is a music/demo cart rather than a conventional game. The current local extractor downloads the live cart but returns no Lua/API/audio data, so this first pass targets a controller-friendly album player with generated replacement Pyxel audio/visuals rather than exact SFX/music parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, corrected live cart URL from the BBS thread, and captured the explicit reuse/Creative Commons evidence; added first playable PyxelPico adaptation (`games/pico8tunesvol1/pico8tunesvol1.py`) with host-tested 12-track setlist, next/previous selection, play/pause, reset, auto-advance, deterministic visualizer state, cover, attribution, manifest, and credits; verification pending in this session note until the final command pass completes.

### Top 100 rank 89. Cab Ride

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=41332
- Cart: https://www.lexaloffle.com/bbs/cposts/ca/cab_ride-7.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Pico-8 Tunes Volume 1; original is a relaxed train simulator with clear controls, passenger/station goals, explicit all-source/assets CC BY-NC-SA license, and extractable cart source/API.
- Risks: Original has a sophisticated pseudo-3D route renderer, long-run route generation, city/tunnel/weather variety, second train, soundtrack, pause menu, express/very-chilled presentation, and exact station scoring polish; first pass targets the core handheld train loop rather than full renderer/source parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, corrected live cart URL from the BBS thread, extracted readable Lua/API surface, and preserved the Powersaurus/rych-t/Mot credit chain; added first playable PyxelPico adaptation (`games/cabride/cabride.py`) with host-tested throttle/brake, station approach, door gating, passengers, stop ratings, express mode, last-station journey completion, cover, attribution, manifest, and credits; verification pending in this session note until the final command pass completes.

### Top 100 rank 90. Two Hiking Cats Have An In Depth Discussion About Life The Universe And Everything

- Status: partial
- Difficulty: medium
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=2719
- Cart: https://www.lexaloffle.com/bbs/cposts/1/16151.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Cab Ride; original BBS post clearly describes a non-game scrolling art toy with speed, palette, and reset controls.
- Risks: This is intentionally not a traditional game. Local extraction returns only a tiny invalid fragment for the live cart, so this pass follows BBS-described behavior rather than source/API parity. Original exact line/circle/modulo composition, cat animation timings, footstep audio, and palette math are outside this first playable pass.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, live numeric cart URL, BBS controls/author intent/commentary evidence, and extraction blocker; added first playable PyxelPico adaptation (`games/twohikingcats/twohikingcats.py`) with host-tested speed changes, deterministic palette randomization, reset, scroll advancement, alternating/manual meows, cat bobbing, cover, attribution, manifest, and credits; verification pending in this session note until the final command pass completes.

### Top 100 rank 91. Harold's Bad Day

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=45507
- Cart: https://www.lexaloffle.com/bbs/cposts/ha/harold-6.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Two Hiking Cats; original source extracts and BBS describes a precision puzzle-platformer where dying can be part of the solution, with 32 levels and speedrun/save-as-many scoring.
- Risks: Original has 32 authored levels, exact platformer physics, corpse puzzle routing, water/music muffling, wind, arrows, fire, doors, palette fading, particles, soundtrack, and speedrun timing polish; first pass targets a compact death-as-tool puzzle-platformer loop rather than full map/source parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, live cart URL, extractable Lua/API surface, BBS mechanics/level-count notes, and biovoid/thefreakar credits; added first playable PyxelPico adaptation (`games/haroldsbad/haroldsbad.py`) with host-tested movement, jumping, deaths, corpse bridge, water drowning, spikes, goal clear, saved-Harold scoring, cover, attribution, manifest, and credits; verification pending in this session note until the final command pass completes.

### Top 100 rank 93. Brutal Pico Race

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=31490
- Cart: https://www.lexaloffle.com/bbs/cposts/br/brutalpicorace_104-0.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Harold's Bad Day; original has clear BBS controls/features, live 1.0.4 cart, extractable Lua/API, and no obvious derivative-IP tag/thread evidence.
- Risks: Original has six tracks, three ship classes, split-screen multiplayer, several AI levels, pseudo-3D road/ship rendering, ship editor/history, drafting, health, boost, lap timeboards, music, and dense HUD polish; first pass targets a compact single-player futuristic racing loop rather than full renderer/source parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, live cart URL, extractable Lua/API surface, BBS controls/features/changelog notes, and dhostin/community credits; added first playable PyxelPico adaptation (`games/brutalpicorace/brutalpicorace.py`) with host-tested ship classes, acceleration/brake, boost meter, wall damage, drafting, AI progress, lap finish, ranking, cover, attribution, manifest, and credits; verification pending in this session note until the final command pass completes.

### Top 100 rank 94. subsurface

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=54080
- Cart: https://www.lexaloffle.com/bbs/cposts/su/subsurface-2.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Brutal Pico Race; original has clear BBS controls/features, live 1.0.2 cart, extractable Lua/API, and no obvious derivative-IP tag/thread evidence.
- Risks: Original has a 40-screen metroidvania map, 6 upgrades, save points, story captions, about 6 enemies, one boss, precise wall-jump/glide/swim tuning, switch routing, health upgrades, and final platforming/boss polish; first pass targets a compact upgrade-gated exploration loop rather than full map/source parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, live cart URL, extractable Lua/API surface, BBS 40-screen/upgrade/control notes, and JulianR credits; added first playable PyxelPico adaptation (`games/subsurface/subsurface.py`) with host-tested upgrades, double jump, wall jump, glide, swim gating, shooting, enemies, water hazard, boss damage, victory, cover, attribution, manifest, and credits; verification pending in this session note until the final command pass completes.

### Top 100 rank 95. DUNGEON!

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=46206
- Cart: https://www.lexaloffle.com/bbs/cposts/du/dungeon-0.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after subsurface; original has clear BBS controls/features, live cart, CC BY-NC-SA metadata, and no obvious derivative-IP tag/thread evidence.
- Risks: Original has randomly selected/preset dungeon courses, a variety of enemies, coins, gift-shop upgrades, weapons, wall jumping, zones with different visuals/music, quips/dialogue, and a final rescue sequence; local extraction exposes compressed/minified initialization and data strings rather than practical source parity, so first pass targets a compact roguelite platformer loop.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, live cart URL, BBS roguelite-platformer/shop/control notes, and partial compressed extraction; added first playable PyxelPico adaptation (`games/dungeonbang/dungeonbang.py`) with host-tested wall jumping, enemies, coins, shop powerups, attacks/weapons, depth/zone progression, portal exits, final rescue, cover, attribution, manifest, and credits; verification pending in this session note until the final command pass completes.

### Top 100 rank 96. Mot's 8-Ball Pool

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=39859
- Cart: https://www.lexaloffle.com/bbs/cposts/mo/mot_pool-23.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after DUNGEON!; original has clear BBS rules/features, live cart, extractable Lua/API, and no obvious derivative-IP tag/thread evidence.
- Risks: Original is a polished 3D 8-ball pool simulation with ball-ball physics, camera transitions, AI opponents, place-ball UI, simplified but broad rule handling, ticker messages, and HUD polish; first pass targets a compact top-down/3D-inspired two-player rule core rather than full physics/render/source parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, live cart URL, extractable Lua/API surface, BBS simplified-rule notes, and Mot credits; added first playable PyxelPico adaptation (`games/mot8ballpool/mot8ballpool.py`) with host-tested aiming, shot power, cue-ball movement, pocket resolution, color assignment, fouls, free balls, black-ball win/forfeit, turn state, cover, attribution, manifest, and credits; verification pending in this session note until the final command pass completes.

### Top 100 rank 97. Villager

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=38905
- Cart: https://www.lexaloffle.com/bbs/cposts/na/nano_villager-0.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Mot's 8-Ball Pool; original has clear BBS mechanics, live cart, extractable Lua/API, and no obvious derivative-IP tag/thread evidence.
- Risks: Original is a polished relaxing city-builder with generated island/map data, Cluly-inspired tile presentation, many objects/building types, peeple pathing, production/hunger/happiness, particles/ambience, and a two-button UI; first pass targets a compact city-builder loop rather than full world/source parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, live cart URL, extractable Lua/API surface, BBS resource/building/peeple/no-save notes, and partnano/Cluly inspiration credits; added first playable PyxelPico adaptation (`games/villager/villager.py`) with host-tested resource gathering, houses, arrivals, farms, workshops, taverns, food, happiness, production, peeple leaving, cover, attribution, manifest, and credits; verification pending in this session note until the final command pass completes.

### Top 100 rank 98. Pico Snail!: Dream Castle

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=39897
- Cart: https://www.lexaloffle.com/bbs/cposts/sn/snail-9.p8.png
- Why: next eligible strict FCDB BBS top-100 candidate after Villager; original has clear CC metadata, live cart, extractable Lua/API, explicit remix permission in the thread, and no obvious derivative-IP tag/thread evidence.
- Risks: Original is a polished platform adventure with authored rooms, saved level unlocks, books/story text, warps, switches, doors, hazards, stars, a cat encounter, original background renderers, sprite animation, and Snail's House / Ujico music-character inspiration; first pass targets a compact Dream Castle loop rather than full map/source/audio parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, live cart URL, extractable Lua/API surface, BBS modify/remix permission, and Floofinator/Ujico credits; added first playable PyxelPico adaptation (`games/picosnail/picosnail.py`) with host-tested movement, star collection, double jump, wand shots, thwack attacks, hazards, switch/door, warp, cat boss, final clear, cover, attribution, manifest, and credits; verification pending in this session note until the final command pass completes.

### Top 100 rank 100. Starjump

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB/BBS metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=41874
- Cart: https://www.lexaloffle.com/bbs/cposts/st/starjump-0.p8.png
- Why: final eligible strict FCDB BBS top-100 candidate; original has clear CC metadata, live cart, BBS controls/options/mechanics notes, and no obvious derivative-IP tag/thread evidence.
- Risks: Original is a polished vector-style precision platformer with authored screen progression, wobble options, timer/progress menu, breakable/disappearing platforms, toggled floor/wall colors, red balloon/cannon sections, external soundtrack, and save/progress behavior; first pass targets a compact vector-platformer loop rather than exact room/source/audio parity.
- 2026-06-17 progress note: Confirmed FCDB/BBS/license metadata, live cart URL, partial extractable Lua/API surface, BBS controls/options, and community mechanics notes; added first playable PyxelPico adaptation (`games/starjump/starjump.py`) with host-tested jump chain, double/triple jump charges, breakable platforms, color toggles, cannon launch, staged progression, timer, final clear, cover, attribution, manifest, and credits; verification pending in this session note until the final command pass completes.

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
- 2026-06-05 progress note: Reconfirmed FCDB/BBS metadata and cart shell (`version 43`, code region starts `00 70 78 61`, so vendored `picotool` still treats it as empty Lua). Improved the partial port with explicit multi-level progression, level-clear/win states, a progress meter, bonus scoring, and a higher-level flying obstacle; `make cart-game GAME=fieldjump PYTHON=python3` passed.

### 8. Office Hell

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=154283
- Cart: https://www.lexaloffle.com/bbs/cposts/of/office_hell_1_0-0.p8.png
- Why: puzzle-platformer candidate once platformer helpers exist.
- Risks: higher polish cost.

- 2026-06-02 progress note: Confirmed FCDB metadata (`bbs_release.json` id/pid `181808`, tid `154283`, author `OlieB123`, license `CC4-BY-NC-SA`) and BBS cart URL. Downloaded/inspected cart shell: map/gfx/sfx/music bytes extract, BBS text confirms one-button direction+jump puzzle-platformer premise, but Lua begins with newer PICO-8 `pxa` compression unsupported by vendored `picotool`. Added first playable PyxelPico adaptation (`games/officehell/officehell.py`), cover from cart label, attribution, manifest and credits; `make cart-game GAME=officehell PYTHON=python3` passed.

### 9. PICO-BALL

- Status: partial
- Difficulty: hard
- License: CC BY-NC-SA 4.0 in local FCDB metadata
- BBS: https://www.lexaloffle.com/bbs/?tid=150620
- Cart: https://www.lexaloffle.com/bbs/cposts/pi/pico_ball-5.p8.png
- Why: physics/sports challenge after easier ports.
- Risks: physics and AI feel; higher asset/audio complexity; original has multiplayer/campaign/powerups beyond a first handheld solo pass.
- 2026-06-03 progress note: Confirmed FCDB metadata (`bbs_release.json` id/pid `171244`, tid `150620`, author `Munchkin`, license `CC4-BY-NC-SA`) and corrected the live BBS cart URL from the thread (`/bbs/cposts/pi/pico_ball-5.p8.png`; the older numeric URL 404s). Downloaded/inspected cart shell: RAM/header extract shows newer PICO-8 `pxa` compressed Lua unsupported by vendored `picotool`; BBS text confirms tennis/volleyball/squash/wallball premise, two-bounce scoring rule, solo/together modes, and arrow/Z/X/controller controls. Added first playable PyxelPico solo/wallball adaptation (`games/picoball/picoball.py`), cover from cart label, attribution, manifest and credits; `make cart-game GAME=picoball PYTHON=python3` passed.

### 10. Pico Valley

- Status: defer
- Difficulty: very hard
- License: CC BY-NC-SA 4.0 metadata, but derivative-IP risk
- BBS: https://www.lexaloffle.com/bbs/?tid=142915
- Cart: https://www.lexaloffle.com/bbs/cposts/150629.p8.png
- Local cart: `projects/pyxelpico/carts/picovalley-2.p8.png`
- Why deferred: large Stardew-style demake; poor baseline for clean preservation workflow.

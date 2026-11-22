---
tags: [mod/status/testing, mod/category/environment, mc-version/1.21.1, loader/neoforge]
mod_id: thick_air
pack_version_pinned: "1.1.2 (thick_air-1.21.1-NeoForge-1.1.2.jar)"
last_verified: "2026-11-21 (dependency ranges and items read from jar; client boot into world, clean)"
---

# Thick Air

**Source:** [Modrinth](https://modrinth.com/mod/thick-air). A rewrite of Fuzss's Thin Air for NeoForge 1.21.1.

## Role in Create Wars
Owner request 2026-11-21: "something that needs us to have oxygen to go up high and deep within caves".
- You slowly **lose air below Y=0 and above Y=128**, and in the Nether. The End has **no air at all**.
- Air sources: **Create's Backtank + Diving Helmet** (Create integration), Respirator (Curios head slot),
  Air Bladder and Reinforced Air Bladder, Potion of Free Breathing (renamed Water Breathing), and soul
  fire, soul torches and soul campfires, which make small pockets of safe air.
- The Safety Lantern shows air quality. Signal Torches mark a cave exit.

**Why this one:** it's the only 1.21.1 option that explicitly limits **both** high altitude and deep
caves. The alternative, [ThinAir: ReLived](https://modrinth.com/mod/thinair-relived), is more actively
updated, but it's about underground and dimension air, not altitude. Downside of Thick Air: one release
only (1.1.2, 2025-12-29), made as a commission. If it breaks on an update, ReLived is the fallback.

## Big gameplay interaction (flagged to owner)
**Y=128 is an altitude ceiling for aircraft.** [[Create Aeronautics]] airships, planes and drones'
pilots run out of air above Y=128 unless they wear a Backtank + Diving Helmet or a Respirator. That's a
real warfare mechanic: high-altitude bombing ([[Create Warnautics|Warnautics]]) needs oxygen gear. It
also affects [[Create Aeronautics AMBUSH|AMBUSH]] fights at altitude, and mountain bases. The thresholds
are configurable.

Overlaps: [[Create Smog|Create: Smog]] also has a "Respirator" item (a different item with the same
name), and Create Deep Seas has diving and oxygen gear. Check in game which ones Thick Air accepts.

## Dependencies
- Hard requires: NeoForge `[21,)`, Minecraft `[1.21.1,1.22)`
- Optional: [[Curios]] `[9.0.0,)` (added, 9.6.0; the Modrinth page lists it as required), [[Create]] `[0.5.1,)`

## Version notes
Added via `packwiz modrinth add thick-air` on 2026-11-21; resolved to `1.1.2`. packwiz pulled in Curios.

## Quests
Oxygen branch (Copper Backtank hub) of the **Pollution and Air** chapter. Boot-tested 2026-11-21: clean.

## Known issues
None logged yet.

## Config decisions
- 2026-11-21 (owner): overworld ceiling raised **Y=128 → Y=192** (`pack/config/thick_air-common.toml`,
  `minecraft:overworld=yellow,0:green,192:yellow`), so normal flying is free and only high-altitude flights
  need gear. **Revisit** if a biome/terrain mod raises mountain heights (owner is considering one).
  Below Y=0, the Nether and the End are unchanged.

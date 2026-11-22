---
tags: [mod/status/testing, mod/category/utility, mc-version/1.21.1, loader/neoforge]
mod_id: stellarity
pack_version_pinned: "3.1.0 (+mod) (Stellarity-3.1.0.jar)"
last_verified: "2026-11-21 (client boot into existing world; new terrain needs a new world)"
---

# Stellarity

**Source:** [Modrinth](https://modrinth.com/mod/stellarity)

## Role in Create Wars
Full End overhaul (data pack packaged as a mod): new terrain and biomes, items and weapons, mobs, a boss (the Empress), the Altar of the Accursed, redesigned **strongholds**. Owner chose it alone (not with Nullscape) on 2026-11-21. Don't add it to an already-generated End.

## Dependencies
- Hard requires: none

## Version notes
Added via packwiz on 2026-11-21. 3.1.0 is the official 1.21/1.21.1 line (6.x is for newer MC).

## Known issues
- One loot table (`void_fishing/drops/warped_marsh`) used `minecraft:firefly_bush` (a newer-MC item), giving 13
  log errors. Patched by `pack/kubejs/data/stellarity/loot_table/void_fishing/drops/warped_marsh.json` (entry removed).

## Config decisions
- 2026-11-21 (owner): **keep vanilla ender pearl drops.** Stellarity makes Overworld Endermen drop chorus fruit;
  `pack/kubejs/data/minecraft/loot_table/entities/enderman.json` restores pearls outside the End (Stellarity's
  End-only pools are kept). Pearls feed waystones, quantum pearls, Tom's connector and Sophisticated links.
- 2026-11-21 (owner: "swap for valuable loot"): **no elytras** ([[../03-Design/Elytra Removal|Elytra Removal]]).
  Overrides in `pack/kubejs/data/stellarity/loot_table/`: End City vault elytra → 2-4 netherite scrap (and its
  fireworks → 2-5 diamonds); Dragon Wings and Empress Wings → a netherite ingot; Phantom Wings → 2 phantom
  membranes. `kubejs/data` takes priority over Stellarity's data (Stellarity's loot errors went 13 → 0).

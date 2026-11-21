---
tags: [mod/status/active, mod/category/utility, mc-version/1.21.1, loader/neoforge]
mod_id: waystones
pack_version_pinned: "waystones-neoforge-1.21.1-21.1.47.jar (updated 2026-11-20 from waystones-neoforge-1.21.1-21.1.42.jar)"
last_verified: "2026-11-20 (packwiz update --all; not yet boot-tested)"
---

# Waystones

**Source:** [Modrinth](https://modrinth.com/mod/waystones)

## Role in Create Wars
Base fast-travel mod (place a waystone, teleport between them). Recipes reworked by
[[Create Waystones Recipes]] to fit Create's resource economy. See that note for the fast-travel-vs-vehicles
balance question this raises for a combat-focused pack.

## Dependencies
- Required by: [[Create Waystones Recipes]]
- Itself requires: [[Balm]] (not declared on Modrinth — only surfaced as a hard crash during a headless
  server boot test; see [[Balm]]'s note and the 2026-09-01 changelog entry)

## Version notes
Auto-resolved and added by `packwiz modrinth add create-waystones-recipes` on 2026-09-01; pinned at
`21.1.42`.

## Known issues
None logged yet.

## Config decisions
- 2026-11-21: **Natural generation disabled** (project owner's call) in `pack/config/waystones-common.toml`,
  the first config file the pack ships: `chunksBetweenWildWaystones = 0` (no wild waystones) and
  `spawnInVillages = "DISABLED"` (none in villages). Waystones are still craftable (see Create Waystones
  Recipes). Only affects newly generated chunks; waystones already in explored chunks stay.
- 2026-11-21: **All Waystones recipes go through Telejuice**
  (`pack/kubejs/server_scripts/waystones_quantum.js`, one data-driven script). Built up over the day
  at the owner's request: Telejuice Buckets → Quantum Casing → Quantum Pearls → Quantum Paper → "fix all
  other waystone recipes to match". Rules:
  1. Ender Pearl → [[../03-Design/Quantum Pearl|Quantum Pearl]] (Ender Pearl + 250 mB Telejuice, mixed):
     all 10 waystone variants (3 each), Warp Stone (7), Warp Dust, Deepslate/Dormant Shard, Warp Scroll.
  2. A Quantum Casing (Railway Casing + 1,000 mB Telejuice) on each side of the Warp Stone in every
     teleport block: 10 waystone variants, 15 sharestones, 16 portstones (portstone row `QDSDQ`).
  3. Paper → Quantum Paper (Paper + 100 mB Telejuice, Spout) in all 5 scrolls.
  - **Exception:** Bound Scroll keeps a normal Ender Pearl. The owner chose to swap only the Warp
    Scroll's pearl.
  - **Sandy Waystone** uses Sandstone instead of Stone Bricks and makes 2 instead of 3 (owner's call,
    after the first in-game test of the recipes on 2026-11-21).
  - Untouched: epitaph, twinbound feather, warp plate (no pearls/paper; warp plate's Warp Dust now
    needs a Quantum Pearl anyway), dye recolors, waystone→mossy conversions.
  - Base recipes are Create Waystones Recipes' mechanical-crafting versions (they load AFTER Waystones
    and override its vanilla-crafting ones); only the listed swaps were made. Variant casings kept so
    recipes don't share identical inputs.
  - **Cost:** one Warp Stone = 7 Quantum Pearls = 1,750 mB Telejuice; one waystone craft (2 waystones) =
    1 Warp Stone + 3 pearls + 2 casings ≈ 4,500 mB. All Telejuice comes from chorus fruit, so waystones
    are firmly post-End.
  - **Re-check on Create Waystones Recipes updates:** the script re-adds its patterns by hand, so new
    upstream recipes (or a white sharestone) won't be covered automatically.

## Update history
- 2026-11-20: `waystones-neoforge-1.21.1-21.1.42.jar` -> `waystones-neoforge-1.21.1-21.1.47.jar` via `packwiz update --all`.

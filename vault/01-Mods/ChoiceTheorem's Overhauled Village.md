---
tags: [mod/status/testing, mod/category/utility, mc-version/1.21.1, loader/neoforge]
mod_id: ct-overhaul-village
pack_version_pinned: "3.6.4 ([neoforge]ctov-1.21.1-3.6.4.jar)"
last_verified: "2026-11-22 (client boot into world, clean load; new chunks not explored yet)"
---

# ChoiceTheorem's Overhauled Village (CTOV)

**Source:** [Modrinth](https://modrinth.com/mod/ct-overhaul-village)

## Role in Create Wars
Owner 2026-11-22: "better villages and more pillager things around the map". Rebuilds villages and pillager outposts
to fit each biome, and adds new village and outpost variants. Chosen over Towns and Towers (both replace the same
structures; don't run both).

## Dependencies
- [[Lithostitched]] (already in the pack for Tectonic).

## Version notes
Added via `packwiz modrinth add ct-overhaul-village` 2026-11-22. **Modrinth marks it server-only**, so packwiz wrote
`side = "server"`; changed to `both` so it runs in single-player (same issue as Lithostitched/Tectonic).

## Known issues
None in the boot log. Only affects newly generated chunks. Its loot chests are per-player through [[Lootr]].

## Config decisions
None.

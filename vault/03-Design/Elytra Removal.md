---
tags: [design]
---

# Elytra Removal

**Script:** `pack/kubejs/server_scripts/elytra_removed.js`

## Decision
2026-11-21, project owner: remove elytras. The likely reason, not stated: a personal glider undercuts
[[../01-Mods/Create Aeronautics|Create Aeronautics]] aircraft and makes ground/air defenses in PvP
pointless.

## How
- Elytras have **no recipe and no loot-table entry** in vanilla or any pack mod (checked by grepping
  every mod jar's `data/` for `minecraft:elytra`). Their only natural source is the item frame that
  generates with End City ships.
- The script empties any item frame or glow item frame holding an elytra when it joins the world
  (`EntityEvents.spawned`, which KubeJS hooks to NeoForge `EntityJoinLevelEvent`, so it also fires on
  chunk load, not just new spawns).
- Backstop: every player tick, if a player is gliding, `stopFallFlying()`. This makes any elytra that
  slips through (already in a world, `/give`, creative) useless.
- Hidden from JEI via `c:hidden_from_recipe_viewers`.

## Re-check on version bumps
- If a new mod adds an elytra recipe, loot entry or a custom elytra-like item, the item removal won't
  catch it. The gliding backstop catches anything that uses vanilla fall-flying.
- Not yet tested in game.

## Update 2026-11-21: Stellarity
[[../01-Mods/Stellarity|Stellarity]] adds elytra sources: an End City vault, Phantom Wings (phantom drop), Dragon Wings
(dragon extra drop) and Empress Wings (boss). Per the owner, all of them are swapped for loot through overrides in
`pack/kubejs/data/stellarity/loot_table/` (netherite scrap and diamonds, a netherite ingot, phantom membranes). The
gliding block in `elytra_removed.js` still covers anything that slips through. Stellarity's elytra trail, dye and
boost functions are harmless (nothing to glide with).

## Update 2026-11-22: Lootr
[[../01-Mods/Lootr|Lootr]] converts the End City elytra frame into its own per-player item frame by default, which
`elytra_removed.js` doesn't watch. Its item-frame conversions are turned off in `pack/config/lootr-common.toml`, so the
frame stays vanilla and gets emptied.


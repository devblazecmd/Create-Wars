---
tags: [mod/status/testing, mod/category/utility, mc-version/1.21.1, loader/neoforge]
mod_id: lootr
pack_version_pinned: "1.11.38.127 (lootr-neoforge-1.21.1-1.11.38.127.jar)"
last_verified: "2026-11-22 (client boot into world, clean load; not playtested)"
---

# Lootr

**Source:** [Modrinth](https://modrinth.com/mod/lootr)

## Role in Create Wars
Owner request 2026-11-22 ("add the lotr mod for chests"). Structure loot chests (and barrels, shulkers, mineshaft
minecarts, brushable blocks) become **per-player**: everyone who opens one gets their own roll, and the chest is
marked as opened for them. In a multiplayer war pack, the first team to reach a dungeon, End City or Incendium
fortress doesn't strip it for everyone. Works on modded structure loot too (Stellarity, Incendium, Terralith,
BOP) as long as the container has a loot table.

## Dependencies
- None. `side = "both"` from Modrinth (no fix needed).

## Version notes
Added via `packwiz modrinth add lootr` on 2026-11-22; resolved to `1.11.38.127`.

## Known issues
None in the boot log. Not yet opened in game.

## Config decisions
`pack/config/lootr-common.toml`:
- **`convert_elytras_to_item_frames = false`** and **`convert_item_frames = false`** (defaults: true). Lootr would
  otherwise replace the End City elytra item frame with its own per-player frame. `elytra_removed.js` only empties
  *vanilla* item frames, so every player could take an elytra (the gliding block would still stop them flying). With
  the conversion off, the frame stays vanilla and the script empties it. `convert_elytras_to_chests` stays false.
  See [[../03-Design/Elytra Removal]].
- Kept default: **per-player loot** (`team_loot = false`). Lootr's team mode uses scoreboard teams, not
  [[FTB Teams]], so turning it on would do nothing useful. Consequence: a team of 4 gets 4 rolls per chest.
- Kept default: Lootr chests can be broken (sneak to break), and explosions can break them.

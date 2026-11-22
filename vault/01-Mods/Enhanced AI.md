---
tags: [mod/status/testing, mod/category/combat, mc-version/1.21.1, loader/neoforge]
mod_id: enhanced-ai
pack_version_pinned: "4.3.2.0-beta (enhancedai-4.3.2.0-beta.jar)"
last_verified: "2026-11-20 (added via packwiz; not yet boot-tested - see Changelog)"
---

# Enhanced AI

**Source:** [Modrinth](https://modrinth.com/mod/enhanced-ai)

## Role in Create Wars
PvE tactics: creepers breach walls, zombies mine, skeletons snipe. Heavily configurable per mob.

## Dependencies
- Hard requires: [[InsaneLib]]

## Version notes
Added via `packwiz modrinth add enhanced-ai` on 2026-11-20; resolved to `4.3.2.0-beta`.

## Known issues
Beta, published the same day it was added. Overlaps with [[Improved Mobs]] (both make mobs break blocks) - config pass needed so they don't double-stack. All-Rights-Reserved license.

## Config decisions
None yet.

## Config decisions (2026-11-22, owner, after the first server test)
Players reported creepers "killing us even though they can't see us". Causes in `config/enhancedai/server.toml`:
`Creeper swell -> "Ignore walls chance" = 0.65` (explode through walls when in range) and `Mobs.Targeting ->
"Xray range override chance" = 0.5` (half of mobs sense players through walls at 4-12 blocks). Owner chose **walls
protect you**: both set to **0.0**. Kept: breaching creepers (7.5%, must see you first), launch creepers (5%), TNT-like
creepers (25%). Shipped as `pack/config/enhancedai/server.toml`.

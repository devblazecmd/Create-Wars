---
tags: [mod/status/active, mod/category/scripting, mc-version/1.21.1, loader/neoforge]
mod_id: kubejs
pack_version_pinned: "2101.7.2-build.374 (kubejs-neoforge-2101.7.2-build.374.jar)"
last_verified: "2026-09-01 (added via packwiz modrinth add)"
---

# KubeJS

**Source:** [Modrinth](https://modrinth.com/mod/kubejs)

## Role in Create Wars
Scripting layer for custom recipes, loot tables, and event-driven behavior — this is how we'll implement
pack-specific balance changes (weapon damage curves, faction-specific crafting, custom drone/radar
interactions) without forking any addon's Java source. Scripts live in `pack/kubejs/server_scripts` and
`pack/kubejs/client_scripts`.

## Dependencies
- Hard requires: [[Rhino]] and [[Better Advanced Tooltips]] — both auto-resolved and added by packwiz
- Used to script behavior across [[Create Big Cannons]], [[Create Droneworks Simulated]], etc.

## Version notes
Added via `packwiz modrinth add kubejs` on 2026-09-01; resolved to `2101.7.2-build.374`, newer than the
`2101.7.1-build.181` seen in research.

## Known issues
None logged yet.

## Config decisions
None yet.

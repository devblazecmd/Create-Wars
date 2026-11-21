---
tags: [mod/status/testing, mod/category/radar, mc-version/1.21.1, loader/neoforge]
mod_id: create-radar-fire-arc
pack_version_pinned: "1.0.0 (create_radar_firearc-1.0.0.jar)"
last_verified: "2026-11-20 (added via packwiz; not yet boot-tested - see Changelog)"
---

# Create Radar Fire Arc Filter

**Source:** [Modrinth](https://modrinth.com/mod/create-radar-fire-arc)

## Role in Create Wars
Adds no-fire sectors to [[Create Radars|Create: Radars]] cannon networks so radar-slaved turrets don't fire into your own base/ships.

## Dependencies
- Hard requires: [[Create]], [[Create Radars|Create: Radars]], [[Create Big Cannons]]

## Version notes
Added via `packwiz modrinth add create-radar-fire-arc` on 2026-11-20; resolved to `1.0.0`.

## Known issues
**Version pin risk:** adding this made packwiz silently upgrade Create: Radars `0.4.9.4` -> `5.1.1` (a major version with beta releases through Oct-Nov 2026). This mod was published 2026-05-16, against the 0.4.x line, so the upgrade was reverted to the tested `0.4.9.4`. If this mod misbehaves, the Radars version is the first suspect.

## Config decisions
None yet.

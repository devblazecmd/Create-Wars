---
tags: [mod/status/active, mod/category/utility, mc-version/1.21.1, loader/neoforge]
mod_id: xaeros-minimap
pack_version_pinned: "xaerominimap-neoforge-1.21.1-26.6.0.jar (updated 2026-11-20 from xaerominimap-neoforge-1.21.1-26.4.2.jar)"
last_verified: "2026-11-20 (packwiz update --all; not yet boot-tested)"
---

# Xaero's Minimap

**Source:** [Modrinth](https://modrinth.com/mod/xaeros-minimap) · author thexaero

## Role in Create Wars
Corner-of-screen minimap: terrain, players, mobs, entities, waypoints. Paired with
[[Xaero's World Map]] and [[FTB Chunks x Xaero's Compat]] so [[FTB Chunks]] team claims render directly on
Xaero's maps — important for a PvP/faction pack where knowing claim boundaries and enemy movement matters.

## Dependencies
- None required by packwiz at add time (standalone), but functionally pairs with [[Xaero's World Map]].

## Version notes
Added via `packwiz modrinth add xaeros-minimap` on 2026-09-01; resolved to `1.21.1-26.4.2`.

## Known issues
None logged yet.

## Config decisions
None yet. Worth deciding whether enemy-team waypoints/entity radar overlap uncomfortably with
[[Mob Radar]]/[[Create Radars|Create: Radars]] — three different "see things on a map/overlay" systems in
one pack. Revisit alongside the radar-overlap decision in [[Mob Radar]].

## Update history
- 2026-11-20: `xaerominimap-neoforge-1.21.1-26.4.2.jar` -> `xaerominimap-neoforge-1.21.1-26.6.0.jar` via `packwiz update --all`.

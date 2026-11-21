---
tags: [mod/status/active, mod/category/optimization, mc-version/1.21.1, loader/neoforge]
mod_id: entityculling
pack_version_pinned: "entityculling-neoforge-1.12.1-mc1.21.1.jar (updated 2026-11-20 from entityculling-neoforge-1.10.5-mc1.21.1.jar)"
last_verified: "2026-11-20 (packwiz update --all; not yet boot-tested)"
---

# Entity Culling

**Source:** [Modrinth](https://modrinth.com/mod/entityculling)

## Role in Create Wars
Skips rendering entities that aren't actually visible (occluded by terrain/blocks). Directly useful for
this pack's large-scale combat scenarios (drones, missiles, submarines, cannon projectiles) which can spawn
many entities at once — culling invisible ones is free FPS in exactly those moments.

## Dependencies
- None required by packwiz at add time (standalone).

## Version notes
Added via `packwiz modrinth add entityculling` on 2026-09-01; resolved to `1.10.5-mc1.21.1`.

## Known issues
None logged yet.

## Config decisions
None yet.

## Update history
- 2026-11-20: `entityculling-neoforge-1.10.5-mc1.21.1.jar` -> `entityculling-neoforge-1.12.1-mc1.21.1.jar` via `packwiz update --all`.

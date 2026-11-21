---
tags: [mod/status/testing, mod/category/vehicles, mc-version/1.21.1, loader/neoforge]
mod_id: synaxis
pack_version_pinned: "1.6.3 (synaxis-1.6.3.jar)"
last_verified: "2026-11-21 (client boot + world load)"
---

# Synaxis

**Source:** [Modrinth](https://modrinth.com/mod/synaxis)

## Role in Create Wars
Engineering/automation for Sable vehicles: Cimulink logic circuits, Lua-programmable units, motors, joints and linear actuators. **Added as a crash fix**: [[Shaolib]] 0.1.0 needs Synaxis classes on every explosion. The content is a bonus for flight-control and stabilized weapon platforms.

## Dependencies
- Hard requires: [[Create]] `>=6.0.10`, [[Sable]] `>=2.0.0`, [[LDLib2]] `>=2.2.23`, [[Sable Photomancy]] (`sable_schematic_api >=0.4.1`)
- Required (undeclared) by: [[Shaolib]]
- Optional: Create Tweaked Controllers (not in pack)
- Modrinth metadata lists **no** dependencies. Found by reading the jar's `neoforge.mods.toml`.

## Version notes
Added via `packwiz modrinth add synaxis` on 2026-11-21.

## Known issues
- [[../02-Bugs/Explosions crash - Shaolib missing Synaxis]]

## Config decisions
None yet.

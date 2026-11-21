---
tags: [mod/status/active, mod/category/storage, mc-version/1.21.1, loader/neoforge]
mod_id: sophisticated-storage
pack_version_pinned: "sophisticatedstorage-1.21.1-1.6.20.2239.jar (updated 2026-11-20 from sophisticatedstorage-1.21.1-1.5.91.2127.jar)"
last_verified: "2026-11-20 (packwiz update --all; not yet boot-tested)"
---

# Sophisticated Storage

**Source:** [Modrinth](https://modrinth.com/mod/sophisticated-storage)

## Role in Create Wars
Upgradeable storage barrels/chests with filtering, auto-crafting, and stack-upgrade support — the logistics
backbone for supplying [[Create Big Cannons]] ammo production and [[Create Aeronautics]]/
[[Create Droneworks Simulated]] parts at scale. Pairs with [[Sophisticated Backpacks]] (same author, shared
core) for portable versions of the same system.

## Dependencies
- Hard requires: [[Sophisticated Core]] (auto-resolved and added by packwiz)

## Version notes
Added via `packwiz modrinth add sophisticated-storage` on 2026-09-01; resolved to `1.21.1-1.5.91.2127`.

## Known issues
None logged yet.

## Config decisions
None yet. Worth deciding whether Create's own logistics (depots, funnels, brass tunnels) and Sophisticated
Storage's filtering/upgrades are meant to compose (storage as the endpoint of a Create line) or compete —
document that choice here once we've playtested a supply chain.

## Update history
- 2026-11-20: `sophisticatedstorage-1.21.1-1.5.91.2127.jar` -> `sophisticatedstorage-1.21.1-1.6.20.2239.jar` via `packwiz update --all`.

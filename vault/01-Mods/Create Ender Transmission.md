---
tags: [mod/status/active, mod/category/utility, mc-version/1.21.1, loader/neoforge]
mod_id: create-ender-transmission
pack_version_pinned: "2.1.1-1.21.1 (createendertransmission-2.1.1-1.21.1.jar)"
last_verified: "2026-09-01 (added via packwiz modrinth add)"
---

# Create: Ender Transmission

**Source:** [Modrinth](https://modrinth.com/mod/create-ender-transmission)

## Role in Create Wars
Makes distance and dimensions irrelevant for Create machines — wireless power/item/fluid transmission
across any range or dimension. Logistics enabler: lets a base's [[Sophisticated Storage]] supply lines and
[[Create Big Cannons]] ammo production reach remote outposts/front lines without physical belts/pipes
spanning the whole map.

## Dependencies
- Hard requires: [[Create]] (auto-resolved and added by packwiz, already present)

## Version notes
Added via `packwiz modrinth add create-ender-transmission` on 2026-09-01; resolved to `2.1.1-1.21.1`,
matching exactly what was requested.

## Known issues
None logged yet.

## Config decisions
None yet. Worth a balance discussion once installed — infinite-range wireless transmission is powerful and
may need range/throughput limits for multiplayer war balance (someone shouldn't be able to trivially supply
a front-line base from an untouchable home base).
- 2026-11-22 (owner: "ender trans should be a quantum thing and its recipes need to be adjusted to call for
  more quantum items to make it hard to get"): `pack/kubejs/server_scripts/ender_transmission_quantum.js`.
  Each transmitter: 5x5 mechanical crafting of 8 Quantum Casings, 6 Quantum Pearls, 2 Advanced Components, a
  Quantum Mechanism, 6 obsidian and 2 of the chute/pump/shaft (was ender pearls, an ender eye and precision
  mechanisms). Chunk Loader: beacon + 4 Quantum Casings + 4 Quantum Pearls + a Quantum Mechanism (was 8
  obsidian around a beacon). Quests: Quantum Expansion, after the Entity Teleporter.

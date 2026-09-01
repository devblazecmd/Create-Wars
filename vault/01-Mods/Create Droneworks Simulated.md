---
tags: [mod/status/active, mod/category/drones, mc-version/1.21.1, loader/neoforge]
mod_id: create-droneworks-simulated
pack_version_pinned: "0.1.1 (droneworks-0.1.1.jar)"
last_verified: "2026-09-01 (added via packwiz modrinth add)"
---

# Create: Droneworks Simulated

**Source:** [Modrinth](https://modrinth.com/mod/create-droneworks-simulated)

## Role in Create Wars
This is the actual "drones" mod for the pack: an addon to [[Create Aeronautics]] that lets you build
aircraft from redstone-controlled parts and pilot them remotely. Ships a **Drone Camera** (first-person
video feed) and a **Drone Remote Controller** (wireless control up to 1500 blocks away per its own
description — verify in-game, mod descriptions overstate ranges often).

## Dependencies
- Hard requires: [[Create Aeronautics]] (this is an addon to it, not standalone) and [[Carbon Config]]
  (auto-resolved and added by packwiz)

## Version notes
Added via `packwiz modrinth add create-droneworks-simulated` on 2026-09-01; resolved to `0.1.1` — a very
early version number, worth watching closely for breaking changes on updates.

## Known issues
None logged yet.

## Config decisions
None yet. The 1500-block remote range figure needs a balance decision once we have a real map size in mind
— see [[Design Doc Template|design doc]] for drone range/counterplay (e.g. does [[Mob Radar]] or something
similar let you detect an incoming drone?).

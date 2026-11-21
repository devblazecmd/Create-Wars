---
tags: [mod/status/testing, mod/category/combat, mc-version/1.21.1, loader/neoforge]
mod_id: create-the-air-war
pack_version_pinned: "5.00 (create_the_air_wars-5.00.jar)"
last_verified: "2026-11-20 (added via packwiz; not yet boot-tested - see Changelog)"
---

# Create The Air War

**Source:** [Modrinth](https://modrinth.com/mod/create-the-air-war)

## Role in Create Wars
Weapons designed for aerial vehicles ([[Create Aeronautics]]).

## Dependencies
- Hard requires: none declared

## Version notes
Added via `packwiz modrinth add create-the-air-war` on 2026-11-20; resolved to `5.00`.

## Known issues
- [[../02-Bugs/Client model load errors|Client model load errors]]: the FAB-1500 model uses an invalid rotation.

## Config decisions
- 2026-11-21: **Launchers and their ammo removed from survival** (project owner's call) by
  `pack/kubejs/server_scripts/air_war_launchers_removed.js`. Recipes are removed and the items hidden from
  JEI: Anti-Aircraft Launcher + C-75 Rocket (these had no recipe upstream, so they were creative-only
  already), Vihr Missile Launcher + Vihr Missile, Heat Trap Launcher + Heat Charge. Still available:
  the standalone missile blocks (Tomahawk, AIM-9X, RIM-7, X-25ML, Kh-101, 9K119M, C-25), bombs, guns and
  drones. Side effect: with Heat Traps gone, there are no flares to decoy AIM-9X missiles.

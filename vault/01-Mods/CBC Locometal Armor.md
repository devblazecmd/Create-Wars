---
tags: [mod/status/testing, mod/category/vehicles, mc-version/1.21.1, loader/neoforge]
mod_id: cbc-locometal-armor
pack_version_pinned: "2.0.0 (locometal_armor-2.0.0.jar)"
last_verified: "2026-11-22 (side switched to both; client boot into world, clean load)"
---

# CBC Locometal Armor

**Source:** [Modrinth](https://modrinth.com/mod/cbc-locometal-armor)

## Role in Create Wars
Gives [[Steam 'n' Rails]] locometal blocks armor properties against [[Create Big Cannons]] - armored trains.

## Dependencies
- Hard requires: [[Steam 'n' Rails]], [[Create Big Cannons]]

## Version notes
Added via `packwiz modrinth add cbc-locometal-armor` on 2026-11-20; resolved to `2.0.0`.

## Known issues
- Until 2026-11-22 it was `side = "server"` (Modrinth marks it server-only). The client installer skipped it,
  so it **never ran in single-player** (single-player uses an integrated server). **Owner 2026-11-22: switched to
  `side = "both"`**. It now installs on clients too and loads clean.

## Config decisions
None yet.

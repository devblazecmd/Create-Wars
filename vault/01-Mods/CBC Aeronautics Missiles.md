---
tags: [mod/status/active, mod/category/combat, mc-version/1.21.1, loader/neoforge]
mod_id: create-simulated-missiles-create-aeronautics
pack_version_pinned: "0.2.0 (cbcaeronauticsmissiles-0.2.0.jar)"
last_verified: "2026-09-01 (added via packwiz curseforge add)"
---

# CBC Aeronautics Missiles

**Source:** [CurseForge](https://www.curseforge.com/minecraft/mc-mods/create-simulated-missiles-create-aeronautics) — full title "Create: Simulated Missiles | Create Aeronautics | Create Big Cannons Compat | Create: Radars Compat"

## Role in Create Wars
Compat/glue mod tying together [[Create Big Cannons]], [[Create Aeronautics]], and [[Create: Radars]]:
missile fins, thrusters, and a targeting interface for building guided missiles on Aeronautics contraptions,
with Big Cannons and Radars compatibility baked in. This is the mod that actually connects "guns,"
"vehicles," and "radar" into one system rather than three separate features.

## Dependencies
- Hard requires: [[Create Aeronautics]], [[Create: Radars]], [[Create]], [[Sable]] — all four auto-resolved
  and added by packwiz in one shot when this was added, confirming it's the connective tissue mod for the
  combat/vehicle/radar side of the pack.

## Version notes
Requested at `0.1.0`; `packwiz curseforge add` resolved to the current latest, `0.2.0`
(`cbcaeronauticsmissiles-0.2.0.jar`), published 2026-08-27. Same pattern as every other mod in this pack —
packwiz always grabs latest at add time.

## Known issues
None logged yet.

## Config decisions
None yet. This is a strong candidate for the drone/radar counterplay design doc mentioned in
[[Create Droneworks Simulated]] and [[Mob Radar]] — guided missiles change what "radar" needs to warn you
about.

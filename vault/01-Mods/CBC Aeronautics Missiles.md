---
tags: [mod/status/active, mod/category/combat, mc-version/1.21.1, loader/neoforge]
mod_id: create-simulated-missiles-create-aeronautics
pack_version_pinned: "0.1.0 (\"CBCAeronautics Missiles 0.1.0.jar\", file-id 8658979)"
last_verified: "2026-09-01 (re-pinned to 0.1.0 for the server smoke test; see version notes)"
---

# CBC Aeronautics Missiles

**Source:** [CurseForge](https://www.curseforge.com/minecraft/mc-mods/create-simulated-missiles-create-aeronautics) — full title "Create: Simulated Missiles | Create Aeronautics | Create Big Cannons Compat | Create: Radars Compat"

## Role in Create Wars
Compat/glue mod tying together [[Create Big Cannons]], [[Create Aeronautics]], and [[Create: Radars]]:
missile fins, thrusters, and a targeting interface for building guided missiles on Aeronautics contraptions,
with Big Cannons and Radars compatibility baked in — **in the `0.2.0` build.** At the currently-pinned
`0.1.0`, packwiz's dependency resolution only found [[Create Aeronautics]] and [[Create]] as requirements —
no [[Create: Radars]] or [[Sable]] — meaning the Radars-targeting integration this note originally praised
may not actually be present at this version. Worth re-checking in-game before assuming missile-targeting via
radar works, and worth considering the 0.2.0 upgrade once its manual-download requirement (see below) is
worth clearing again.

## Dependencies
- At `0.1.0`: [[Create Aeronautics]] and [[Create]] (confirmed via packwiz dependency resolution).
- At `0.2.0` (not currently pinned): also pulls in [[Create: Radars]] and [[Sable]].

## Version notes
Originally added at `0.2.0` (packwiz always resolves to current latest at add time), but this project has
**third-party downloads disabled on CurseForge** — neither packwiz, Prism, nor any automated tool can fetch
it; only a browser can, and CurseForge's Cloudflare bot-challenge blocks even a direct `curl` of the
download page. The project owner already had a `0.1.0` file on hand from manually browsing CurseForge, so
the pack was re-pinned to that specific file (`--file-id 8658979`) via `packwiz curseforge add --file-id
8658979 create-simulated-missiles-create-aeronautics` on 2026-09-01, rather than asking for a repeat manual
download of `0.2.0`. **Anyone setting this pack up fresh (including via Prism) will need to manually
download this exact file from CurseForge and place it in `mods/` themselves** — this is a hard external
constraint of this specific mod's distribution settings, not a bug in the pack.

## Known issues
None logged yet in-game — confirmed to load without error in a headless server boot test on 2026-09-01
(see [[../04-Changelog/Changelog|changelog]]).

## Known issues
None logged yet.

## Config decisions
None yet. This is a strong candidate for the drone/radar counterplay design doc mentioned in
[[Create Droneworks Simulated]] and [[Mob Radar]] — guided missiles change what "radar" needs to warn you
about.

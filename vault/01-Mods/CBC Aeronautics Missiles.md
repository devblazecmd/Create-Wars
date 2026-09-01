---
tags: [mod/status/active, mod/category/combat, mc-version/1.21.1, loader/neoforge]
mod_id: create-simulated-missiles-create-aeronautics
pack_version_pinned: "0.2.0 (cbcaeronauticsmissiles-0.2.0.jar, file-id 8746555)"
last_verified: "2026-09-01 (re-pinned to 0.2.0 once the project owner obtained that file)"
---

# CBC Aeronautics Missiles

**Source:** [CurseForge](https://www.curseforge.com/minecraft/mc-mods/create-simulated-missiles-create-aeronautics) — full title "Create: Simulated Missiles | Create Aeronautics | Create Big Cannons Compat | Create: Radars Compat"

## Role in Create Wars
Compat/glue mod tying together [[Create Big Cannons]], [[Create Aeronautics]], and [[Create: Radars]]:
missile fins, thrusters, and a targeting interface for building guided missiles on Aeronautics contraptions,
with Big Cannons and Radars compatibility baked in. This is the mod that actually connects "guns,"
"vehicles," and "radar" into one system rather than three separate features.

## Dependencies
- Hard requires: [[Create Aeronautics]], [[Create]], [[Sable]] (all confirmed via packwiz dependency
  resolution at this version) and [[Create: Radars]] (added the first time this mod was pinned; still
  present in the pack, so later re-adds don't re-list it as "new").

## Version notes
Pinned three times so far, all via `packwiz curseforge add --file-id <id>
create-simulated-missiles-create-aeronautics`:
1. First added 2026-09-01, resolved to latest (`0.2.0`, file-id 8746555).
2. Re-pinned same day to `0.1.0` (file-id 8658979) for the headless server smoke test, since that's the
   file the project owner had on hand at the time. At `0.1.0`, dependency resolution only found
   [[Create Aeronautics]] and [[Create]] — no [[Create: Radars]] or [[Sable]] — meaning the
   Radars-targeting integration may not have actually been present at that version.
3. Re-pinned back to `0.2.0` (file-id 8746555) same day once the project owner obtained that file too —
   this is the version now active in the pack, restoring the Create: Radars/Sable integration.

**Distribution note (applies at every version):** this project has **third-party downloads disabled on
CurseForge** — neither packwiz, Prism, nor any automated tool can fetch it; only a browser can, and
CurseForge's Cloudflare bot-challenge blocks even a direct `curl` of the download page. **Anyone setting
this pack up fresh (including via Prism) will need to manually download this exact file from CurseForge and
place it in `mods/` themselves** — this is a hard external constraint of this mod's distribution settings,
not a bug in the pack.

**Recurring side-effect to watch for:** every time this mod has been re-pinned via `packwiz curseforge add`,
it has caused packwiz to re-resolve the shared [[Create Aeronautics]] (and transitively [[Sable]])
dependency through CurseForge metadata instead of their working Modrinth sources — and those CurseForge
copies are *also* distribution-disabled. Both times this was caught and fixed by running
`packwiz modrinth add create-aeronautics` immediately afterward. **Do this again after any future re-pin of
this mod.**

## Known issues
None. `0.1.0` was confirmed to load without error in a headless server boot test on 2026-09-01, and `0.2.0`
(the version now pinned) was confirmed via a real client launch through Prism Launcher the same day — the
project owner reported the full instance ("all looks good"). See
[[../04-Changelog/Changelog|changelog]] for both test writeups.

## Config decisions
None yet. This is a strong candidate for the drone/radar counterplay design doc mentioned in
[[Create Droneworks Simulated]] and [[Mob Radar]] — guided missiles change what "radar" needs to warn you
about.

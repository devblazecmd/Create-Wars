---
tags: [mod/status/active, mod/category/radar, mc-version/1.21.1, loader/neoforge]
mod_id: mob-radar
pack_version_pinned: "1.1.0 (mob_radar-1.1.0-neoforge-1.21.1.jar)"
last_verified: "2026-09-01 (added via packwiz curseforge add)"
---

# Mob Radar

**Open decision (2026-09-01):** [[CBC Aeronautics Missiles]] pulled in [[Create Radars|Create: Radars]] as a
hard dependency, which is a Create-native radar addon with explicit missile-targeting compat. We now have
two overlapping "radar" mods. Don't remove either unilaterally — decide in-game whether they serve distinct
purposes (this one: general terrain-penetrating mob/player detection; Create: Radars: missile
guidance/detection) or whether one makes the other redundant.

**Source:** [CurseForge](https://www.curseforge.com/minecraft/mc-mods/mob-radar)

## Role in Create Wars
Candidate "radar" mod: reveals outlines of nearby mobs (players included, depending on gamerule config)
within 30 blocks for a 10-second window, even through terrain. Configurable via gamerules for which entity
types it detects.

## Dependencies
- Hard requires: none beyond NeoForge (standalone, no Create dependency)

## Version notes
v1.1.0 for NeoForge 1.21.1, updated 2026-02-10 per CurseForge listing. Small download count (~2.1K) at
research time — worth a closer look at maintenance activity/issue tracker before committing to it, or
compare against `CombatRadar` (also found in research, not yet reviewed) before deciding.

## Known issues
None logged yet.

## Config decisions
None yet — the 30-block range and 10-second duration are gamerule-configurable; balance decision once
installed, likely tied to the same design doc as [[Create Droneworks Simulated]] drone counterplay.

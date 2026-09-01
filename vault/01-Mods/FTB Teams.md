---
tags: [mod/status/active, mod/category/teams, mc-version/1.21.1, loader/neoforge]
mod_id: ftb-teams-forge
pack_version_pinned: "2101.1.11 (ftb-teams-neoforge-2101.1.11.jar)"
last_verified: "2026-09-01 (added via packwiz curseforge add)"
---

# FTB Teams (NeoForge)

**Source:** [CurseForge](https://www.curseforge.com/minecraft/mc-mods/ftb-teams-forge) — note the CurseForge
slug keeps the legacy `-forge` suffix even for the NeoForge build; don't be misled into thinking it's
Forge-only.

**Distribution note:** FTB's mods (this, [[FTB Quests]], [[FTB Chunks]], [[FTB Library]]) are **not on
Modrinth** — `packwiz modrinth add ftb-teams` silently fell back to a fuzzy text search and grabbed the
wrong project ("Better Party X FTB Teams," a compat addon) the first time around. Corrected by removing
that and using `packwiz curseforge add ftb-teams-forge` instead. If any FTB mod needs updating later, use
`packwiz curseforge`, not `packwiz modrinth`.

## Role in Create Wars
Core team/faction system — the library other FTB mods (and any custom KubeJS scripting) hook into for
team progression, ownership, and permissions. Directly relevant to the "fight each other" side of the
pack: teams are the natural unit for PvP factions.

## Dependencies
- Hard requires: [[FTB Library]] and Architectury API (both auto-resolved and added by packwiz)

## Version notes
Added via `packwiz curseforge add ftb-teams-forge` on 2026-09-01; resolved to `2101.1.11`.

## Known issues
None logged yet.

## Config decisions
None yet. This is where faction design (see [[Design Doc Template|design docs]] under `03-Design`) will
eventually need to hook in — e.g. team-based claim protection via [[FTB Chunks]], team-based quest lines
via [[FTB Quests]].

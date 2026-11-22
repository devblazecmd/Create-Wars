---
tags: [mod/status/testing, mod/category/combat, mc-version/1.21.1, loader/neoforge]
mod_id: improved-mobs
pack_version_pinned: "1.21.1-1.16.1-neoforge (improvedmobs-1.21.1-1.16.1-neoforge.jar)"
last_verified: "2026-11-20 (added via packwiz; not yet boot-tested - see Changelog)"
---

# Improved Mobs

**Source:** [Modrinth](https://modrinth.com/mod/improved-mobs)

## Role in Create Wars
PvE threat scaling: mobs gain gear and stats over time/difficulty, break and place blocks, ride each other.

## Dependencies
- Hard requires: [[TenshiLib]]

## Version notes
Added via `packwiz modrinth add improved-mobs` on 2026-11-20; resolved to `1.21.1-1.16.1-neoforge`.

## Known issues
Block-breaking mobs vs. player bases: decide whether [[FTB Chunks]] claimed areas should be immune. All-Rights-Reserved license.

## Config decisions
- 2026-11-21: Difficulty overlay (`Difficulty X.X` HUD text) moved from top-left to **bottom-right** (owner:
  it clashed with the top-left of the screen). `pack/config/improvedmobs/client.toml`,
  `"Difficulty location" = "BOTTOMRIGHT"`. Still shown; difficulty scaling itself unchanged.

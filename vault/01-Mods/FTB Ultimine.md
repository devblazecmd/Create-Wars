---
tags: [mod/status/testing, mod/category/utility, mc-version/1.21.1, loader/neoforge]
mod_id: ftb-ultimine-forge
pack_version_pinned: "2101.1.15 (ftb-ultimine-neoforge-2101.1.15.jar)"
last_verified: "2026-11-22 (client boot into world, clean load)"
---

# FTB Ultimine

**Source:** [CurseForge](https://www.curseforge.com/minecraft/mc-mods/ftb-ultimine-forge) (FTB family: CurseForge only, `-forge` slug)

## Role in Create Wars
Owner 2026-11-22: "is there a vein miner" -> chose FTB Ultimine over Veinminer (same FTB family as Quests/Teams/Chunks).
Hold the Ultimine key (default **`**, grave accent; keycode 96 read from the jar) and break a block to mine connected
blocks. Also bulk crop harvest, log stripping, tilling. Welcome chapter has a "Vein Mining" info quest.

## Dependencies
- [[FTB Library]] (already present).

## Version notes
Added via `packwiz curseforge add ftb-ultimine-forge` 2026-11-22; no other `.pw.toml` files were rewritten.

## Known issues
None in the boot log.

## Config decisions
Defaults kept (`config/ftbultimine-server.snbt`): 64 blocks max, 20 exhaustion per block, no cooldown, no tool
required. Revisit `require_tool` / `max_blocks` if it feels too strong.

---
tags: [mod/status/active, mod/category/teams, mc-version/1.21.1, loader/neoforge]
mod_id: ftb-chunks-forge
pack_version_pinned: "2101.1.21 (ftb-chunks-neoforge-2101.1.21.jar)"
last_verified: "2026-09-01 (added via packwiz curseforge add)"
---

# FTB Chunks (NeoForge)

**Source:** [CurseForge](https://www.curseforge.com/minecraft/mc-mods/ftb-chunks-forge) — same
`-forge`-suffix-on-NeoForge-slug naming as [[FTB Teams]]/[[FTB Quests]]. Also not on Modrinth.

## Role in Create Wars
Chunk claiming/protection, tied to [[FTB Teams]] — teams claim territory, protecting builds from griefing
by rival teams while still allowing the intended PvP/"war" conflict to happen through sanctioned means
(cannons, drones, missiles) rather than trivial block-breaking raids. Also provides the map/minimap.

**Note:** there's a separate addon, "FTB Chunks: Sable Aerospace," that specifically protects
[[Create Aeronautics|Sable/Aeronautics]] structures within claimed chunks — it was accidentally installed
in place of this mod on the first attempt (see [[FTB Teams]]'s distribution note) and was removed. Worth
revisiting deliberately: since Aeronautics vehicles can fly across claim boundaries, that addon may actually
be useful once base FTB Chunks is confirmed working — don't dismiss it just because it caused a mix-up.

## Dependencies
- No new dependencies at add time — [[FTB Library]] already present.

## Version notes
Added via `packwiz curseforge add ftb-chunks-forge` on 2026-09-01; resolved to `2101.1.21`.

## Known issues
None logged yet.

## Config decisions
None yet. Claim rules need to explicitly account for airborne/moving Create contraptions
([[Create Aeronautics]], [[CBC Aeronautics Missiles]]) crossing claim boundaries — default chunk-protection
mods aren't always contraption-aware.

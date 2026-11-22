---
tags: [mod/status/testing, mod/category/combat, mc-version/1.21.1, loader/neoforge]
mod_id: functional-armor-trim
pack_version_pinned: "1.21-1 (functionalarmortrim-neoforge-1.21-1.jar)"
last_verified: "2026-11-22 (client boot into world, clean load)"
---

# Functional Armor Trim

**Source:** [CurseForge](https://www.curseforge.com/minecraft/mc-mods/functional-armor-trim) (owner linked it 2026-11-22)

## Role in Create Wars
Armor trims give attribute bonuses by trim **material**, per armor piece (a full set stacks four times). Defaults
(from `config/functionalarmortrim.json`, generated on first run, now shipped in `pack/config/`):
iron +2 armor; diamond and netherite +2 armor and toughness; redstone +10% speed and step height; copper +10% swim
speed; amethyst night vision; lapis +10% XP; quartz thorns; emerald better villager prices.

## Dependencies
None. Declares Minecraft `[1.21, 1.22)`, NeoForge `[21.0.40-beta,)`; the 1.21 jar runs on 1.21.1.

## Version notes
Added via `packwiz curseforge add functional-armor-trim` 2026-11-22. No other `.pw.toml` rewritten.

## Known issues
None in the boot log.

## Config decisions
Defaults kept; shipped so the server and every client use the same values. PvP note: a full netherite-trimmed set adds
+8 armor on top of the armor itself.

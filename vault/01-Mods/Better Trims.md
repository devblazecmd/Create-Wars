---
tags: [mod/status/testing, mod/category/combat, mc-version/1.21.1, loader/neoforge]
mod_id: functionalarmortrim
pack_version_pinned: "1.21.1-1.3.0 (better-trims-armor-and-weapons-1.21.1-1.3.0.jar, raw jar in pack/mods/)"
last_verified: "2026-11-22 (1.2.1: client boot, tool trims verified in-game data; dedicated server not yet confirmed)"
---

# Better Trims: Armor & Weapons

**Source:** owner-built fork of [[Functional Armor Trim]] (Tfarcenim, Unlicense / public domain), republished as CC0
with credit. Not on Modrinth or CurseForge. Same mod ID `functionalarmortrim`, so the existing config keeps working.

## Role in Create Wars
Armor trims give stat bonuses by trim material (`config/functionalarmortrim.json`, shipped). Adds tool/weapon and
ranged-weapon trim bonuses (`config/functionalarmortrim_tools.json`), which need a tool-trims mod or datapack; none is
in the pack yet, so only armor trims do anything for now.

## The fix (why this fork exists)
The original crashed dedicated servers: `attributes()` fell back to the client-only `ModClient.MAP` whenever
`getStaticServer()` was null, which also happens on a dedicated server during startup (Improved Mobs scores gear
then), loading `ClientLevel` -> "invalid dist DEDICATED_SERVER". The fork computes
`useClient = FMLEnvironment.dist.isClient() && getStaticServer() == null` and guards all three lookups (armor,
ranged, tools) with it, so a server never touches `ModClient`. Also returns early for untrimmed items.
Reviewed 2026-11-22 with `javap`: the only other client reference is `GameRendererMixin`, which is in the mixin
config's `client` list (never applied on a server).

## Dependencies
NeoForge `[21.1.0,)`, Minecraft `[1.21.1]`.

## Version notes
Raw jar in `pack/mods/` (un-ignored in `pack/.gitignore`), indexed by hash. To update: replace the jar, `packwiz refresh`.

## Known issues
Not yet proven on a dedicated server (owner is testing on UltraServers). If it crashes, check for `ModClient` /
`ClientLevel` in the log first.

## Config decisions
Defaults (same as the original). PvP: a full netherite-trimmed set adds +8 armor.

## 1.2.1 (2026-11-22): tool and weapon trims
Owner added `data/minecraft/tags/item/trimmable_armor.json` -> `#functionalarmortrim:trimmable_tools` (vanilla swords,
axes, pickaxes, shovels, hoes, bow, crossbow, trident, mace + optional `#c:tools/*` tags), so the vanilla smithing-table
trim recipe and JEI accept tools. Verified with a temporary KubeJS check on the test instance: iron sword + redstone trim
gets +0.25 attack speed, bow + iron trim +10% arrow damage (`functionalarmortrim:arrow_damage`), diamond chestplate + iron
trim +2 armor. No icon visuals for trimmed tools (tooltip only). New configs shipped: `functionalarmortrim_tools.json`,
`functionalarmortrim_ranged.json`. Client-code scan unchanged (dist guard intact, GameRendererMixin client-only).

## 1.3.0 (2026-11-22): armor trims only (owner: intended)
Removes tool/weapon trimming again: no `trimmable_armor` / `trimmable_tools` tags, no "Weapons & Tools" smithing-template
tooltip (`ModClient.onTooltip`, `toolTrimmingEnabled` removed), no `TRIMMABLE_TOOLS` tag key. The tool/ranged bonus code
is still in the jar but unreachable without a way to trim tools. `FunctionalArmorTrimNeoForge` is byte-identical to 1.2.1,
so the dedicated-server fix is unchanged. The tools/ranged configs were dropped from the pack.


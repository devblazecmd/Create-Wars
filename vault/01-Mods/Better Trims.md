---
tags: [mod/status/testing, mod/category/combat, mc-version/1.21.1, loader/neoforge]
mod_id: functionalarmortrim
pack_version_pinned: "1.21.1-1.4.0 (better-trims-armor-and-weapons-1.21.1-1.4.0.jar, raw jar in pack/mods/)"
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

**Correction (2026-11-22):** tool/weapon trimming now comes from **Tool Trims** (Modrinth `tool-trims`, 3.0.7+1.21.1,
`pack/mods/tool-trims.pw.toml`). Its four templates (Linear, Tracks, Charge, Frost) put a vanilla `minecraft:trim` on
tools/weapons with visible icon patterns, so Better Trims' tool and ranged bonuses are reachable again. The
`functionalarmortrim_tools.json` / `functionalarmortrim_ranged.json` configs are back in the pack (mod defaults).
Vanilla armor templates stay armor-only on purpose (no weapon art exists for vanilla patterns).

## 1.4.0 (2026-11-22): Tool Trims templates in creative
When [[Tool Trims]] is loaded, adds its four templates (Linear, Tracks, Charge, Frost) to the creative Ingredients tab
(and search). Tool Trims' 1.21.1 build has no creative entries of its own. The stacks match Tool Trims'
`set_<pattern>_template` item modifiers: spawn egg + custom name, `custom_model_data` 315001, marker `entity_data`,
`custom_data {"tooltrims:item":"template"}`, lore. No behavior change without Tool Trims. Jar sha256 `62659daa…ccba`.
Not yet verified in-game.

## 1.4.0 (2026-11-22): Tool Trims compatibility
Adds `ToolTrimsCompat`: when `tool_trims` is loaded, puts its four templates (linear/tracks/charge/frost, spawn-egg
based) in the Ingredients creative tab. Only other change: the constructor registers it; `attributes()` (the dedicated-
server fix) is unchanged and the new class has no client references. Tool Trims writes the vanilla `minecraft:trim`
component (pattern `tooltrims:*`), so Better Trims' bonuses apply. Verified on the test instance: diamond sword with
`tooltrims:frost` + diamond trim gets +1 attack damage and +2 mining efficiency (tools config).


---
tags: [mod/status/testing, mod/category/combat, mc-version/1.21.1, loader/neoforge]
mod_id: functionalarmortrim
pack_version_pinned: "1.21.1-1.1.0 (better-trims-armor-and-weapons-1.21.1-1.1.0.jar, raw jar in pack/mods/)"
last_verified: "2026-11-22 (bytecode reviewed; not yet run on a dedicated server - owner testing on UltraServers)"
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

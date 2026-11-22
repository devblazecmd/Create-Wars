---
tags: [mod/status/testing, mod/category/environment, mc-version/1.21.1, loader/neoforge]
mod_id: adpother
pack_version_pinned: "9.1.15.0 (AdPother-1.21.1-9.1.15.0-NeoForge-build.1399.jar)"
last_verified: "2026-11-21 (client boot into world; one coremod hook fails, see Known issues)"
---

# Pollution of the Realms (PoTR)

**Source:** [Modrinth](https://modrinth.com/mod/pollution-of-the-realms). The jar is named **AdPother** and
its mod ID is `adpother`.

## Role in Create Wars
The pollution simulation (owner request 2026-11-21: "add some pollution mods"). Burning fuel releases
**carbon, sulfur and dust** as visible blocks. They rise, form clouds and drift with the wind. Left
alone, they cause acid rain, polluted water, reduced visibility, and damage to plants, crops, animals
and **player health**. Oil spills contaminate soil. Its built-in mitigation tools are deliberately basic,
because it expects other mods to supply the fixes. In this pack, that's [[Create Smog|Create: Smog]].

## Dependencies
- Hard requires: [[ForgeEndertech]] `[12.1.5.0,)`, NeoForge `[21.1.0,)`, Minecraft `[1.21.1]` exactly
- Optional (from Modrinth): [[Create Aeronautics]]
- Used by: [[Create Smog|Create: Smog]] (optional integration)

## Version notes
Added via `packwiz modrinth add pollution-of-the-realms` on 2026-11-21; resolved to `9.1.15.0`, which was
published that same day. packwiz pulled in ForgeEndertech.

## Known issues
- [[../02-Bugs/PoTR coremod misses TFMG coke oven and blast furnace]]: one coremod logs `FAILED: target
  node not found!` on boot. TFMG's coke oven and blast furnace don't pollute. Not a crash.

## Open questions (balance; needs playtest)
- **Harshness:** crop damage hits the [[Farmer's Delight]] food loop, and health damage hits PvP. Decide the
  config after a playtest.
- **Sources:** which machines count as polluters? Blaze Burners, TFMG engines and the coke oven are the big
  ones in this pack. Create: Smog covers "anything that burns" on the Create side. Check that the two
  don't double-count.
- Explosions and dust may also pollute, which matters a lot for [[Create Warnautics|Warnautics]] bombs.

## Config decisions
- 2026-11-21 (owner, later): **both models on**: `pack/config/smog-common.toml` sets
  `mode = "POTR_AND_BUILT_IN"` (experimental per the Smog author; the only change from defaults).
  `potionAirEffectsWithPotr` stays `false`, so players don't get both breathing debuffs. In this mode Smog's
  own model also runs: acid rain, high-air layer, waste-water ground contamination, and its source list
  (which includes TFMG's industrial blast furnace and coal burner). **Create is the standard**: PoTR's own
  tools are disabled (see the PoTR note).
- 2026-11-21 (owner: "i want it all disabled and create to be the standard"): PoTR's own pollution tools are
  **removed from play** by `pack/kubejs/server_scripts/potr_tools_removed.js`: Aerometer, Iron/Gold/Diamond
  Filter Frames, Vacuum Bags, Vacuum Tubes and Respirators. Recipes are removed (plus all `adpother`
  recipes) and the items hidden from JEI. PoTR has no chest loot for them (only block-drop tables). The
  pollution itself (carbon/sulfur/dust blocks, polluted water, cloud generator) still runs. The quest ref
  checker bans these IDs.
- 2026-11-21 (owner): **keep PoTR + Smog in `POTR` mode** (Smog's default, no config change). Requirement:
  "as long as i can just use create to handle the pollution". In this mode Smog's smokestacks, ducts,
  precipitators, scrubbers, respirator and sensors act on PoTR's pollution. Considered and rejected: dropping
  PoTR for Smog `BUILT_IN` (which would fix the TFMG coke oven and blast furnace gap and add Smog's waste-water
  side). Revisit if the [[../02-Bugs/PoTR coremod misses TFMG coke oven and blast furnace|TFMG gap]] matters.


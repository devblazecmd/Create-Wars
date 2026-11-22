---
tags: [bug/status/open, bug/severity/minor, bug/type/compat, mc-version/1.21.1, loader/neoforge]
affected_mods: ["[[../01-Mods/Pollution of the Realms|Pollution of the Realms]]", "[[../01-Mods/Create TFMG Community Edition|TFMG]]"]
date_opened: "2026-11-21"
---

# PoTR coremod misses TFMG coke oven and blast furnace

## Symptom
On boot, after adding [[../01-Mods/Pollution of the Realms|Pollution of the Realms]] 9.1.15.0:
```
[modloading-worker-0/ERROR] [net.neoforged.coremod.CoreMod.adpother/COREMODLOG]: FAILED: target node not found!
```
The game doesn't crash and the world loads normally.

## Cause
PoTR ships JavaScript coremods that hook fuel burning in other mods. The log doesn't say which hook
failed, so each Create/TFMG hook target was checked with `javap` against the installed jars:
| Hook | Target | Result |
|---|---|---|
| create/air_current, block_breaking_kinetic_tile, block_breaking_movement, fan_processing, fluid_spilling | Create 6.0.10 | ✓ all match |
| createtfmg/abstract_engine_fuel_burnout | `AbstractEngineBlockEntity.manageFuelAndExhaust` → `forceDrain` | ✓ |
| createtfmg/blast_furnace_fuel_burnout | `BlastFurnaceOutputBlockEntity.tick` → `ItemStack.shrink` | ✗ method no longer calls `shrink` |
| createtfmg/coke_oven_fuel_burnout | `CokeOvenBlockEntity.tickRecipe` | ✗ method doesn't exist |

The pack's TFMG (`tfmg-1.21.1-1.3.3a-community.jar`) was refactored after PoTR wrote these hooks.

## Effect
The TFMG **Coke Oven** and **Blast Furnace** don't produce PoTR pollution. TFMG engines, vanilla
furnaces and Create machines do. [[../01-Mods/Create Smog|Create: Smog]] may still count them as burning
sources through its own model; check in game.

## Fix options
- Wait for a PoTR update (report upstream).
- Write a KubeJS or datapack workaround if Smog doesn't cover these machines.
- Accept it: these are the two "cleanest" heavy-industry blocks for now.

## Environment
Pack after the 2026-11-21 pollution addition; NeoForge 21.1.267.

---
tags: [mod/status/testing, mod/category/environment, mc-version/1.21.1, loader/neoforge]
mod_id: smog
pack_version_pinned: "0.5.0 (smog-0.5.0+mc1.21.1.jar)"
last_verified: "2026-11-21 (dependency ranges and items read from jar; client boot into world, clean)"
---

# Create: Smog

**Source:** [Modrinth](https://modrinth.com/mod/create-smog)

## Role in Create Wars
The Create-side machinery for pollution. Owner request 2026-11-21. Anything that burns (furnaces, Blaze
Burners, engines, other mods' generators) puts smoke into its chunk. Smog adds ways to deal with it:
- **Exhaust:** Smokestacks (the `flue` block) and Exhaust Ducts. Tall stacks (12 blocks by default) send
  smoke into a high layer that drifts thinly over a wider area. Oily exhaust condenses as Waste Oil.
- **Filtering:** the Electrostatic Precipitator catches soot and industrial dust, more the faster it
  spins. Pipe water in and it also removes sulfur, which comes out as Acidic Runoff.
- **Cleanup:** the Air Scrubber is kinetic and takes Filter Cartridges (basic, brass, precision).
  Cartridges clog and are cleaned by bulk washing. Scrubbers side by side join into a panel, and a full
  5x5 panel also clears the high layer.
- **Waste treatment:** Basin recipes for wastewater, sludge, acidic runoff and waste oil. Also adds
  Respirator, Aerometer, Smog Sensor, Oil Burner, Graphite and Sludge Cake.

**Pollution model:** Smog can run its own model or work on top of [[Pollution of the Realms]]. PoTR is
installed, so check which mode it picks.

## Dependencies
- Hard requires: [[Create]] `[6.0.0,)`, NeoForge `[21.1.219,)`, Minecraft `[1.21.1,1.21.2)`
- Optional: [[Pollution of the Realms]] `[9.0.0,)` (installed, 9.1.15.0)

## Version notes
Added via `packwiz modrinth add create-smog` on 2026-11-21; resolved to `0.5.0`. It's a pre-1.0 mod, so
expect changes.

## Quests
**Pollution and Air** chapter (Infrastructure) of the [[../03-Design/Quest Book|Quest Book]].

## Known issues
None logged yet.

## Config decisions
- 2026-11-21 (owner, later): **both models on**: `pack/config/smog-common.toml` sets
  `mode = "POTR_AND_BUILT_IN"` (experimental per the Smog author; the only change from defaults).
  `potionAirEffectsWithPotr` stays `false`, so players don't get both breathing debuffs. In this mode Smog's
  own model also runs: acid rain, high-air layer, waste-water ground contamination, and its source list
  (which includes TFMG's industrial blast furnace and coal burner). **Create is the standard**: PoTR's own
  tools are disabled (see the PoTR note).
- 2026-11-21 (owner): **keep PoTR + Smog in `POTR` mode** (Smog's default, no config change). Requirement:
  "as long as i can just use create to handle the pollution". In this mode Smog's smokestacks, ducts,
  precipitators, scrubbers, respirator and sensors act on PoTR's pollution. Considered and rejected: dropping
  PoTR for Smog `BUILT_IN` (which would fix the TFMG coke oven and blast furnace gap and add Smog's waste-water
  side). Revisit if the [[../02-Bugs/PoTR coremod misses TFMG coke oven and blast furnace|TFMG gap]] matters.
- 2026-11-21: added `tfmg:firebox=20:combustion` to the emitters (it has Create's `blaze` heat property, so it
  scales and switches off). Smog's default TFMG entries (`industrial_blast_furnace`, `diesel_engine`,
  `coal_burner`) **don't exist** in TFMG Community 1.3.3a; they're skipped harmlessly.
- 2026-11-21: TFMG Coke Oven and Blast Furnace pollute via `pack/kubejs/server_scripts/tfmg_smog_sources.js`
  (they have no `lit` state, so a config entry would pollute while idle). Uses `Smog.add` while the block
  entity's `currentRecipe` is set. **Smokestacks can't vent this pollution**; scrubbers clean it. Ran 40+ s in
  game with no errors, but not yet observed with a working coke oven.

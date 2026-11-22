---
tags: [mod/status/testing, mod/category/power, mc-version/1.21.1, loader/neoforge]
mod_id: createnuclear
pack_version_pinned: "2.0.1 (createnuclear-2.0.1-neoforge.jar)"
last_verified: "2026-11-22 (client boot into world, clean load; not playtested)"
---

# Create Nuclear

**Source:** [Modrinth](https://modrinth.com/mod/createnuclear) · [CurseForge](https://www.curseforge.com/minecraft/mc-mods/createnuclear)

## Role in Create Wars
Owner request 2026-11-22: "a good nuclear mod to add to the chaos". Chosen over the other 1.21.1 options
(Nuclear Science, HBM ports, NuclearCraft) because it is a Create addon and runs on SU.

- **Fuel chain** (read from the jar's recipes): uranium ore, then Create crushing twice to uranium powder
  (crushing granite also gives a little), then liquid uranium, then compacting to **yellowcake**, then
  fanning it through an **Enriching Campfire** (soul soil + obsidian + nether star) to
  **enriched yellowcake**, then mechanical crafting into **uranium rods**. Thorium follows a similar path
  to **thorium rods**. **Graphite rods** (steel + graphene from pressed coal dust) cool the reactor.
- **Reactor:** a multiblock built to the **Reactor Blueprint**. The controller costs a nether star, netherite
  and an item vault. Tiers by size (5x5, 7x7, 9x9). A good build makes millions of SU.
- **Coolant:** nitrogen (nitrate ore, smelted, then fanned through powder snow).
- **Radiation:** radioactive items give a Radiation effect. Countered by the anti-radiation suit (brass,
  lead, graphite rods) and iodine.
- **Meltdown:** an overheated reactor makes a nuclear explosion and turns the area into an irradiated
  "Wasteland" biome. The Biome Irradiation Extractor restores it.
- Adds its own **steel**, **lead**, thorium and nitrate ores, and irradiated animals.

Uranium rods are also what [[CBC Enhanced Shells]] nukes cost. See [[../03-Design/Nuclear Weapons]].

## Dependencies
- Hard requires: [[Create]] (present).
- Optional (Modrinth): JEI and others; none needed.

## Version notes
Added via `packwiz modrinth add createnuclear` on 2026-11-22; resolved to `2.0.1` (released 2026-11-07).
The mod page warns that updating an existing world to V2 needs every reactor taken apart first. That doesn't
apply here (first install), but **read the changelog before any future major-version update**.

## Known issues
- [[../02-Bugs/Create Nuclear armor dye recipes fail to load]]: the 64 recipes that recolor anti-radiation
  armor with cloth don't load. The armor itself crafts.
- **Duplicate metals:** its steel is folded into [[../03-Design/Steel Unification]]. Its **lead** is the third
  lead in the pack (TFMG and Gunsmithing also add one). Not unified yet. Recipes that use lead mostly
  take the `c:ingots/lead` tag, so any lead works, but raw lead now has competing smelting recipes.
  Flagged to owner 2026-11-22.

## Config decisions
- `pack/config/createnuclear-server.toml`: **`warn_all_players = true`** and **`warning_distance_blocks = 256`**
  (defaults: false, 100). In a war pack a meltdown is a battlefield event. Everyone nearby gets a warning
  before the blast. (2026-11-22, owner approved "all of that".)
- Everything else is at defaults: radiation on, world generation on, and the same meltdown power.

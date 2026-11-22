---
tags: [mod/status/testing, mod/category/vehicles, mc-version/1.21.1, loader/neoforge]
mod_id: create-armored-constructs
pack_version_pinned: "1.0.0 (arcon-1.0.0.jar)"
last_verified: "2026-11-20 (added via packwiz; not yet boot-tested - see Changelog)"
---

# Create Armored Constructs

**Source:** [Modrinth](https://modrinth.com/mod/create-armored-constructs)

## Role in Create Wars
Military-themed Create addon for armored construction and vehicle building.

## Dependencies
- Hard requires: [[Create]], [[Create Big Cannons]], [[Sable]]

## Version notes
Added via `packwiz modrinth add create-armored-constructs` on 2026-11-20; resolved to `1.0.0`.

## Known issues
License is All-Rights-Reserved - fine for a packwiz pack (downloads from Modrinth CDN), but don't bundle the jar in a zip export without checking.
- **1.0.0 ships with no recipes at all** (116 items), even though the mod page says it has them. Found
  2026-11-22 by the quest audit: [[../02-Bugs/Quest items with no survival recipe]]. Also: the Rangefinder block has no item form, and several items are
  labelled "(in development)" by the mod.

## Config decisions
None yet.
- 2026-11-22 (owner: "give them recipes"): `pack/kubejs/server_scripts/missing_recipes.js` adds recipes.
  - **Hull armor**, 8 per craft, priced by the mod's own stats (`data/arcon/block_armor/tags`, toughness/mass):
    aluminum 4/0.25 (TFMG aluminum sheets), titanium 6/0.5 (Air War titanium sheets), rolled 15/2 (steel +
    TFMG heavy plate), nickel 22/2.5 (TFMG nickel + steel block), ceramic 34/1.2 (fireclay + diamond), boron
    48/1.5 (coal coke + netherite scrap, mechanical crafting). A stonecutter recolors any hull of the same
    material (item tags `createwars:arcon_hull_<material>`).
  - **Tank gun** (breech, barrels x2, intermediate muzzle, muzzle): mechanical crafting from heavy plates and
    steel; the breech needs a TFMG Steel Mechanism.
  - **BOPS round**: AP Shot + 2 brass sheets + packed guncotton, or reload a Spent Cartridge Casing.
  - **Steel Seat**: wool + steel plates.
  - Hidden: the "(in development)" items (thermal vision, power generator, aiming unit, optical unit,
    Kontakt-1 ERA) and the creative-tab banner pieces.
- Quests: Armored Vehicles chapter, hull-armor chain under the Armor hub (rolled -> nickel -> ceramic -> boron;
  aluminum -> titanium), gated on Industrial Age steel.

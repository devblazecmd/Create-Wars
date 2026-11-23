---
tags: [mod/status/testing, mod/category/food, mc-version/1.21.1, loader/neoforge]
mod_id: create-fishery-industry
pack_version_pinned: "createfisheryindustry-5.1.2.jar (CurseForge project 1245539, file 8863886)"
last_verified: "2026-11-23 (boots in Create Wars - Testing; jar requires Create [6.0.10,6.1.0), pack has 6.0.10)"
---

# Create: Fishery Industry

**Source:** [CurseForge](https://www.curseforge.com/minecraft/mc-mods/create-fishery-industry) (no Modrinth listing).
Author Adonis_Baffin, MIT license.

## Role in Create Wars
Automated fishing for Create, so fish fit the Agriculture automation chapter and the Food chapter's Fishing branch
(owner 2026-11-23: "oh we didnt add in the fishing mod", after asking whether it would complement the pack). From
the project page (web research, 2026-11-23, not yet confirmed in game):
- **Frame Trap**: contraption block that catches fish and other creatures, collects nearby items and generates
  biome-dependent fishing loot.
- **Mesh Trap**: catches small creatures and outputs their drops to adjacent containers.
- **Trap Nozzle / Smart Nozzle**: air currents that catch airborne creatures / collect filtered items.
- **Mechanical Peeler**: separates fish skin from fish steaks.
- **Smart Mesh**: production-line logistics.
- **Diving Leggings**: super jump underwater.
- **Harpoon, Harpoon Pouch, Pneumatic Harpoon Gun** (backtank-powered; page says "Sable Compat"): combat tie-in.

## Dependencies
- Hard requires: Create `[6.0.10,6.1.0)` (from the jar; CurseForge lists no dependencies).
- Soft/optional compat with: Sable (Pneumatic Harpoon Gun).

## Version notes
Added 2026-11-23 via `packwiz cf add --addon-id 1245539 -y` → 5.1.2 (NeoForge 1.21.1, Sep 2026). Its
`neoforge.mods.toml` requires Create `[6.0.10,6.1.0)`, NeoForge `[21.1.0,)`, MC `[1.21.1,1.22)`; the pack has Create
6.0.10. Boot-tested 2026-11-23: loads, 39 items registered. Recipes seen in the export: `peeling` (cod/salmon → steak +
fish skin; also rose quartz, leather armor, netherrack, obsidian) and `bait_trap` (fish/steaks/mussels/skin → lobster;
seeds → chicken + feather; carrot → rabbit + hide).

## Quest book
Food chapter Fishing branch: Frame Trap (+ Trap Bearing), Bait Trap → Lobster, Mechanical Peeler → Fish Steaks.
Agriculture: new **Seafood** group (16 items: lobster, mussels, steaks, fish skin, cooked versions, soups, chowder,
seafood steak); Raw Cod/Salmon, Chicken, Rabbit and Feather texts point at the traps.

## Known issues
- Log warning: `createfisheryindustry:item/chains` references a missing `minecraft:chains` model, so that item may
  render as a missing texture. Cosmetic; not used in any quest.

## Config decisions
None yet. The Frame Trap's catchable creatures are configurable; review for PvP (can it trap players' pets/mounts?).

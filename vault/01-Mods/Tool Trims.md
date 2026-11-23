---
tags: [mod/status/testing, mod/category/combat, mc-version/1.21.1, loader/neoforge]
mod_id: tool_trims
pack_version_pinned: "3.0.7+1.21.1 (tool-trims-v3.0.7-for-1.21.1.jar)"
last_verified: "2026-11-22 (added via packwiz modrinth add --version-id 2MVXIAn7; not yet booted in the pack)"
---

# Tool Trims

**Source:** [Modrinth](https://modrinth.com/datapack/tool-trims) (by JoeFly, All Rights Reserved: use the
Modrinth download, don't repack or bundle it)

## Role in Create Wars
Lets players trim tools and weapons (swords, axes, pickaxes, shovels, hoes, bow, crossbow, mace) at the
Smithing Table with four new templates: Linear, Tracks, Charge, Frost. Trimmed tools show the pattern on
the item icon. The trim is a vanilla `minecraft:trim` component, so [[Better Trims]] reads it and applies
its tool bonuses (`functionalarmortrim_tools.json`) or ranged bonuses (`functionalarmortrim_ranged.json`)
in the main hand.

## Dependencies
- None on NeoForge. It's a data + resource pack shipped as a `lowcodefml` mod. packwiz warns that it
  can't find "Fabric API"; that dependency is Fabric-only and correctly not added.

## Version notes
Pinned to the 1.21.1 build `3.0.7+1.21.1` (Modrinth version id `2MVXIAn7`). The project's latest versions
target 1.21.11+/26.x, so don't let packwiz update it past the 1.21.1 build.

## Known issues
- Templates are spawn eggs (tadpole, silverfish, cod, snow golem) with custom data and model data. JEI
  shows the recipes with plain spawn eggs as the template.
- Only Tool Trims' own patterns have tool art. Vanilla armor templates stay armor-only (Better Trims
  1.3.0) because no weapon art exists for vanilla patterns.

## Config decisions
None. Creative/testing: `/function tooltrims:get_items` gives all four templates.

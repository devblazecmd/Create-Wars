---
tags: [design/balance, mc-version/1.21.1, loader/neoforge]
status: active
aliases: [Steel Unification]
---

# Metal Unification

(Called "Steel Unification" until 2026-11-22, when lead was added.)

## Goal
One of each metal for the whole pack. Several mods add their own copy of the same metal, so a player could
have "steel" or "lead" that didn't work in another mod's recipe.
- **Steel** (owner 2026-11-21: **all interchangeable**): TFMG, [[../01-Mods/Create Big Cannons|CBC]],
  Create: Gunsmithing, and [[../01-Mods/Create Nuclear|Create Nuclear]] since 2026-11-22.
- **Lead** (owner 2026-11-22: "unify lead the same way as steel"): TFMG, Gunsmithing and Create Nuclear.
- **Uranium** (owner 2026-11-22: "do the same thing for uranium"): checked the live registry. Only Create
  Nuclear adds uranium. `create:crushed_raw_uranium` is Create's own compat item and a step in Create Nuclear's
  chain, not a second uranium. **Nothing to unify.** Thorium is the same (Create Nuclear only).

## Mechanics
- **Script:** `pack/kubejs/server_scripts/metal_unification.js` (was `steel_unification.js`).
- **Main copy:** [[../01-Mods/Create TFMG Community Edition|TFMG]]'s, for every form:
  - Steel: `tfmg:steel_ingot`, `steel_nugget`, `steel_block`. TFMG's blast furnace line exists to make it.
  - Lead: `tfmg:lead_ingot`, `lead_nugget`, `lead_block`, `raw_lead`, `raw_lead_block`.
- **Inputs:** every recipe that asked for a specific item now takes the shared `c:` tag (`c:ingots/…`,
  `c:nuggets/…`, `c:storage_blocks/…`, `c:raw_materials/lead`, `c:storage_blocks/raw_lead`). Steel sheet
  inputs take `c:plates/steel`.
- **Outputs:** recipes that made another mod's copy make TFMG's instead. This also settles the three
  competing smelting recipes for raw lead.
- **JEI:** the other copies are hidden. The script also adds each one to its `c:` tag, because Gunsmithing's
  lead block and Create Nuclear's raw lead block had no item tag. That way copies already in a world still
  work.
- **Lead ore:** only TFMG's lead ore generates now. Gunsmithing's (`cgs:add_lead_ore`) and Create Nuclear's
  (`createnuclear:lead_ore`) biome modifiers are replaced with `neoforge:none` in `pack/kubejs/data/`. Chunks
  that already exist keep their ores, and those ore blocks are hidden but still smelt into TFMG lead.
- CBC has no plain steel *nugget* (only nethersteel). The script first listed one and crashed the
  recipe event; fixed the same day.
- Quests: the Infantry "Steel" and "Lead" quests ask for TFMG's. `check_quest_refs.py` bans the hidden IDs.

## Wire and spool (2026-11-22)
Owner: "pick one set to be primary" -> **Create Crafts and Additions** (chosen over TFMG; recommended).
- **Copper wire:** C&A's, made only by the Rolling Mill (copper sheet). TFMG's ingot-stonecutter wire
  (`tfmg:copper_wire_from_ingots_copper_stonecutting`) and The Air War's crafted `create_the_air_wars:wires` are
  removed and hidden. Inputs take `#c:wires/copper`. Script: `pack/kubejs/server_scripts/wire_unification.js`.
  - The Air War's AIM-9X, Tomahawk and X-25ML are Create mechanical-crafting recipes, which `replaceInput` doesn't
    reach, so they're overridden as data files in `pack/kubejs/data/create_the_air_wars/recipe/` with the key
    changed to the tag.
- **Empty spool:** C&A's (iron sheets + iron rods). TFMG's wooden empty spool is removed and hidden; TFMG's copper,
  aluminum and constantan spools are wound on the C&A spool.
- **Copper spools: both kept.** Each is the wiring tool for its own mod's network (C&A connectors vs TFMG cable
  insulators) and TFMG uses its own as a part. Renamed with resource-pack lang overrides in `pack/kubejs/assets/`:
  "Copper Spool (C&A)" and "Copper Spool (TFMG Cable)".
- Aluminum and constantan wire (TFMG only) and iron, gold and electrum wire (C&A only) had no duplicates.

## Decisions log
- 2026-11-21: Steel unified (owner chose "all interchangeable").
- 2026-11-21: **Cheap early steel stays** (owner). CBC's and Gunsmithing's mixer recipes still work, so
  steel exists before the Industrial Age, and TFMG's blast furnace is the high-volume route.
- 2026-11-22: Create Nuclear's steel ingot, nugget and block added to the hidden set (it tags them into the same
  `c:` tags). Its reactor recipes already ask for `c:ingots/steel`.
- 2026-11-22: Lead unified on TFMG (owner). Duplicate lead ore generation turned off. Uranium checked; there's
  no duplicate. The Infantry "Lead" quest switched from `cgs:lead_ingot` to `tfmg:lead_ingot`. KubeJS
  modified recipes went from 16 to 49, with 0 failed.

- 2026-11-22: **Create Nuclear's mixer steel removed** (`createnuclear:mixing/steel`: iron + coal dust, *no heat*).
  It gave steel almost free and skipped the heat progression. Owner: "cut the nuclear one". Forcing a single steel
  recipe (TFMG only) was considered and **not done**: Infantry and Artillery open after the Andesite Age and need
  steel before the blast furnace. Steel routes left: CBC heated mixer (iron + coal), Gunsmithing superheated
  mixer (iron + charcoal dust), TFMG blast furnace + casting (bulk).

## Open questions
- Not yet checked in JEI that every replaced recipe shows correctly (KubeJS reported no errors).
- **Not yet confirmed that the lead ore overrides work.** Biome modifiers are world-generation data. Check in
  **new chunks** that only TFMG lead ore appears (for example with `/place feature`, or by mining). With 2 of
  the 3 lead sources gone, check that lead isn't too scarce.

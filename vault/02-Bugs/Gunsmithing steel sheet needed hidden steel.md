---
tags: [bug/status/fixed, bug/severity/major, bug/type/mod-conflict, mc-version/1.21.1, loader/neoforge]
affected_mods: ["[[../01-Mods/Create Gunsmithing]]", "[[../01-Mods/KubeJS]]"]
date_opened: "2026-11-22"
date_resolved: "2026-11-22"
---

# Gunsmithing steel sheet needed hidden steel

## Symptom
`tools/audit_quests.py` reported the Infantry "Steel Sheet" quest as a dead recipe: the only way to make
`cgs:steel_sheet` was pressing `cgs:steel_ingot`, which [[../03-Design/Metal Unification]] hides and no longer
produces. A player with TFMG steel could not make steel sheets at all.

## Cause
`metal_unification.js` swaps item inputs for `#c:ingots/steel` with `event.replaceInput`. Without a KubeJS
Create schema, that does **not** reach Create processing recipes (`create:pressing` and others store inputs
under `ingredients`). Smelting, blasting and crafting recipes were replaced correctly. Of the 9,671 loaded
recipes, this was the only one left needing a hidden item. Gunsmithing's steel nail sequenced assembly
already takes `c:nuggets/steel`.

## Fix
`metal_unification.js` removes `cgs:pressing/steel_ingot` and adds `createwars:pressing/steel_sheet`
(`#c:ingots/steel` -> `cgs:steel_sheet`).

## How to catch this next time
After any change that hides items, boot once and run `python tools/audit_quests.py`. Its DEAD RECIPE
section lists every item whose recipes all need a hidden item. Also: never assume `replaceInput` covered
Create machine recipes.

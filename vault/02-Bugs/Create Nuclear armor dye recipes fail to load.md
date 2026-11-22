---
tags: [bug/status/open, bug/severity/minor, bug/type/version-incompatibility, mc-version/1.21.1, loader/neoforge]
affected_mods: ["[[../01-Mods/Create Nuclear]]", "[[../01-Mods/KubeJS]]"]
date_opened: "2026-11-22"
date_resolved: ""
---

# Create Nuclear armor dye recipes fail to load

## Symptom
On every boot, `latest.log` has 64 warnings like:
```
KubeRecipe.java#90: Failed to parse recipe 'createnuclear:smithing/default_anti_radiation_boots_red[minecraft:smithing_transform]'!
Falling back to vanilla: Failed to read required component 'template: ingredient' ...
Item array cannot be empty, at least one item must be defined
```

## Cause
`createnuclear-2.0.1`'s 64 `data/createnuclear/recipe/smithing/*.json` recipes (recolor anti-radiation
armor with colored cloth) have `"template": []`. An empty ingredient isn't valid on 1.21.1. This is a bug
in the mod, not something the pack caused.

## Impact
You can't recolor the anti-radiation suit. Crafting the suit itself works (separate shaped recipes). Every
other recipe loads: KubeJS reports 0 failed recipes.

## Fix
None yet. If wanted: re-add the recolor recipes in KubeJS with a real template (or as shapeless
suit + cloth), or report it upstream. Recheck after updating Create Nuclear.

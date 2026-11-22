---
tags: [bug/status/fixed, bug/severity/minor, bug/type/config, mc-version/1.21.1, loader/neoforge]
affected_mods: ["[[../01-Mods/Rolled Homongenous Forked]]", "[[../01-Mods/FTB Quests]]"]
date_opened: "2026-11-21"
date_resolved: "2026-11-21"
---

# RHA hatch is not a registered item

## Symptom
When FTB Quests saved the book in game, the Armored Vehicles chapter's "Armored Hatch" task became
```
id: "ftbquests:missing_item", components: { "ftbquests:missing_item": "rha:hatcholive" }
```
so the quest could never be completed.

## Cause
`rha-1.0.3b.jar` ships an item model **and** an `item.rha.hatcholive` name for the hatch, but never
registers the item. None of the hatch colors have a recipe either; RHA's only recipes are stonecutting
an iron block into armor plates and sandbags. `tools/check_quest_refs.py` only read jar assets, so it
believed the item existed.

## Fix
- The quest was replaced with **Sandbags** (`rha:sandbaggreen`, stonecut from an iron block), and the
  armor quest text now says how armor is made.
- **Checker hardened:** `pack/kubejs/server_scripts/export_registry_ids.js` writes the live item and
  entity registry to `kubejs/exported/createwars_registry.json` on server load. The checker uses that
  file when it exists ("ID source: live registry export"). The live registry has 6,553 items, while the
  jar scan "knew" about 8,069, so roughly 1,500 IDs only looked valid.
- The checker also tells items, blocks and entities apart now, and flags block-only IDs.

## How to catch this next time
Boot the game once, then run `python tools/check_quest_refs.py` and check it says "live registry
export". Also, after any in-game save of the book, `grep -r missing_item` in the instance's quest folder
should find nothing.

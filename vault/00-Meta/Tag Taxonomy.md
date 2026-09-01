---
tags: [meta]
---

# Tag Taxonomy

Every note in this vault should carry frontmatter tags from this list. Consistent tags are what let us
find "everything broken by the 1.21.1 → 1.21.4 jump" or "every mod with a radar/combat role" in one search
instead of re-reading every note after a Minecraft update.

## Mod status — `#mod/status/...`
- `#mod/status/candidate` — researched, not yet added to the pack
- `#mod/status/active` — currently in `pack/` and expected to work
- `#mod/status/testing` — added, not yet verified in-game
- `#mod/status/disabled` — present in the pack but turned off (config or removed from index)
- `#mod/status/removed` — pulled from the pack; note kept for history

## Mod category — `#mod/category/...`
- `#mod/category/core` — Create itself and hard dependencies (Flywheel, etc.)
- `#mod/category/combat` — guns, cannons, ammo
- `#mod/category/vehicles` — planes, cars, ships, trains
- `#mod/category/drones` — remote-controlled/autonomous units
- `#mod/category/radar` — detection/awareness
- `#mod/category/storage` — inventory/logistics (backpacks, storage upgrades, etc.)
- `#mod/category/teams` — factions/claims/questing (FTB Teams/Quests/Chunks and similar)
- `#mod/category/scripting` — KubeJS/CraftTweaker and similar
- `#mod/category/utility` — QoL, performance, world-gen, etc.
- `#mod/category/dependency` — required library mod, not a "feature" by itself

## Minecraft/loader — always tag the version(s) a note applies to
- `#mc-version/1.21.1`
- `#loader/neoforge`

(Add new `#mc-version/x.y.z` tags as the pack moves versions. Never delete old ones — they're what make
"what broke when we moved from 1.21.1" answerable later.)

## Bug tracking — `#bug/...`
- `#bug/status/open`
- `#bug/status/investigating`
- `#bug/status/fixed`
- `#bug/status/wontfix`
- `#bug/severity/crash`
- `#bug/severity/major`
- `#bug/severity/minor`
- `#bug/severity/cosmetic`
- `#bug/type/mod-conflict`
- `#bug/type/version-incompatibility`
- `#bug/type/config`
- `#bug/type/performance`
- `#bug/type/balance`

## Design — `#design/...`
- `#design/faction`
- `#design/weapon`
- `#design/progression`
- `#design/balance`

Use [[Mod Note Template]], [[Bug Report Template]], and [[Design Doc Template]] so tags and frontmatter stay
consistent without having to remember the list above every time.

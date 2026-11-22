---
tags: [design/balance, mc-version/1.21.1, loader/neoforge]
status: active
---

# Steel Unification

## Goal
One steel for the whole pack. Three mods each added their own steel ingot, so a player could have
"steel" that didn't work in another mod's recipe. Owner decision 2026-11-21: **all interchangeable**.

## Mechanics
- **Script:** `pack/kubejs/server_scripts/steel_unification.js`
- **Main steel:** [[../01-Mods/Create TFMG Community Edition|TFMG]]'s (`tfmg:steel_ingot`, `steel_nugget`,
  `steel_block`). TFMG's blast furnace line exists to make it.
- **Inputs:** every recipe that asked for a specific steel item (TFMG, [[../01-Mods/Create Big Cannons|CBC]]
  or Gunsmithing) now takes the shared tag (`c:ingots/steel`, `c:nuggets/steel`,
  `c:storage_blocks/steel`). Steel sheet inputs take `c:plates/steel`.
- **Outputs:** recipes that made CBC or Gunsmithing steel now make TFMG steel.
- **JEI:** CBC and Gunsmithing steel ingots, nuggets and blocks are hidden. Copies already in a world
  still work, because they keep their `c:` tags.
- CBC has no plain steel *nugget* (only nethersteel). The script first listed one and crashed the
  recipe event; fixed the same day.
- Quests: the Infantry "Steel" quest asks for TFMG steel. `check_quest_refs.py` bans the hidden IDs.

## Decisions log
- 2026-11-21: Unified (owner chose "all interchangeable").
- 2026-11-21: **Cheap early steel stays** (owner). CBC's and Gunsmithing's mixer recipes still work, so
  steel exists before the Industrial Age, and TFMG's blast furnace is the high-volume route.

## Open questions
- Not yet checked in JEI that every replaced recipe shows correctly (KubeJS reported no errors).

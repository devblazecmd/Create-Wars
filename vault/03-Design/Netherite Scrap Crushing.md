---
tags: [design/balance, mc-version/1.21.1, loader/neoforge]
status: active
---

# Netherite Scrap Crushing

## Goal
A renewable, automatable route to netherite, so the Automation chapter's netherite goal doesn't depend
on finite Ancient Debris. Owner request 2026-11-21: "should be like a crushing of nether brick to get
scrap".

## Mechanics
- **Script:** `pack/kubejs/server_scripts/netherite_scrap_crushing.js`
- [[../01-Mods/Create|Create]] crushing: **Nether Bricks (block) → 2 Nether Brick + 5% Netherite Scrap**
  (`createwars:crushing/netherite_scrap_from_nether_bricks`, processing time 250).
- Chain: netherrack (infinite) → smelt → nether brick items → craft blocks → crushing wheels → scrap →
  Mechanical Crafters run vanilla **4 scrap + 4 gold → netherite ingot** (unchanged).
- Returning 2 of the 4 brick items means each block costs only half its bricks, so a loop can recycle
  some of them.
- Vanilla debris smelting/blasting still works (fan bulk blasting through lava).
- Taught by **Automate: Netherite** (a stack since 2026-11-23) in the [[Quest Book]] Ore Automation chapter (was Heat).

## Open questions
- Is 5% right? About 80 brick blocks (~320 netherrack) per ingot. Netherite is the top PvP gear tier,
  so tune `NETHERITE_SCRAP_CHANCE` after playtesting.

## Decisions log
- 2026-11-21: Added at 2%. Checked that no other recipe crushes nether bricks (no conflict).
- 2026-11-21: Raised to **5%** (owner).

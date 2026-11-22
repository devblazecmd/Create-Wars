---
tags: [design/balance, mc-version/1.21.1, loader/neoforge]
status: active
---

# Nuclear Weapons

## Goal
Owner 2026-11-22: "a good nuclear mod to add to the chaos", and on the trade-offs (base-erasing blasts,
claims not stopping them, possible server lag): "yes im good with all of that it is a war pack after all".

Nukes should be the **end of the warfare tree**. They cost a running nuclear industry, so you can't get
one early. A nuke is a strategic weapon, and so is a reactor (a meltdown is a nuclear blast of its own).

## Mods
- [[../01-Mods/Create Nuclear]]: uranium, reactors, radiation, meltdowns.
- [[../01-Mods/CBC Enhanced Shells]]: the nuke shells (and nothing else; the rest is hidden).

## Mechanics
Script: `pack/kubejs/server_scripts/nuclear_weapons.js`.
- Every `cbc_enhanced_shells` recipe is removed except the two H-bombs, and every item from that mod is
  hidden from JEI except the four nukes. Both rules match the mod ID, not a list, so they survive updates.
- **Nuclear Shell** (mechanical crafting, 5x5): Big Cannons HE shell + **8 uranium rods** + 9 lead ingots
  (any lead; lead is unified on TFMG's, see [[Metal Unification]]) + a nether star. Replaces "8 HE Mk.V shells + nether star", which needed the hidden tier chain.
- **Nuclear Shell Mk.II** (mechanical crafting, 5x5): a nuke shell + 8 uranium rods + 8 thorium rods +
  4 enriched yellowcake. Replaces "8 nuke shells + nether star".
- **Mini H-Bomb** (mod recipe): 4 nuke shells, 3 end crystals, 2 nether stars.
- **H-Bomb** (mod recipe): 3 Mk.II shells, 4 end crystals, 2 nether stars.
- Nether stars along the way: the enriching campfire's soul soil, the reactor controller, and one per nuke.
  The Wither is the real gate.
- Quests: **Ages** tab chapter **"Nuclear Age"** (moved from Warfare 2026-11-22, owner) (renamed from "Nuclear" 2026-11-22, owner) (unlocked by Industrial Age steel). Its finale is the H-Bomb, which
  gives 30 levels and 2 War Trophy rolls.

## Decisions log
- 2026-11-22: Create Nuclear + CBC Enhanced Shells nukes, gated on uranium, other shells hidden (owner).
- 2026-11-22: Meltdown warnings go to everyone within 256 blocks (Create Nuclear config; default is off).
- 2026-11-22: Chapter renamed "Nuclear Age". Nuke quest text hedged: "Claims *maybe* won't save anyone" (owner).

## Open questions
- **Not fired yet.** Check the real blast radius, how long the server stalls, and whether
  [[../01-Mods/FTB Chunks]] claim protection stops any of it. Enhanced Shells declares an optional FTB Chunks
  dependency, so it may respect claims, which is why the quest text says claims
  *maybe* won't save anyone (owner 2026-11-22).
- If one nuke freezes a server for too long, the fallback is keeping only the Mini H-Bomb and Mk.I.

---
tags: [design/progression, mc-version/1.21.1, loader/neoforge]
status: approved
---

# Spec: automation-ore (new Ore Automation chapter)

Follow-up of [[Quest Book v4 - automation-breakout]]. Same pattern and rules as
[[Quest Book v4 - automation-andesite]] and [[Quest Book v4 - automation-brass]] (no machines, +2 levels per item,
group capstones, a master capstone).

## Objective
Owner (2026-11-23): "now do ore and this will include diamond and netherite bcs they are ore NOT heat items".
Owner choices: Brass's Ore Processing group **moves here**; scope is **every ore except nuclear** (uranium, thorium
and nitrate stay with the Nuclear Age).

## Groups (stack each; *moved* = existing quest, same ID)
| Group | Items |
|---|---|
| **Mining** (drills on contraptions) | raw iron, raw copper, raw gold, raw zinc, raw nickel, raw lithium, raw titanium, raw amalgam, raw sulfur |
| **Crushing** (entry: *Crushing Wheels*, moved from Brass) | crushed raw iron, gold, copper, zinc, lead, nickel, lithium; crushed amalgam; nugget of experience |
| **Ingots** | copper, zinc *(moved)*, zinc nugget, lead, nickel, lithium, titanium |
| **Gems & Dusts** | redstone dust (moved from Brass's Rose Quartz group), lapis lazuli, emerald, sulfur |
| **Diamonds** | coal, block of coal, diamond *(moved from Heat)* |
| **Netherite** | nether bricks, netherite scrap, netherite ingot *(moved from Heat)* |

35 automate quests. Notes: lead is unified on TFMG and TFMG lead has no raw item; sulfur is Gunsmithing's (crushing
magma blocks; four mods add a sulfur and they aren't unified); iron and gold ingots stay in Andesite's Metals group,
nether quartz in Andesite's Washing group.

## Moves (IDs kept via `legacy`)
- From Brass: `crushing` (Crushing Wheels), `auto_zinc`, and the new crushed-ore / zinc nugget / experience nugget /
  redstone quests. Rail Warfare's Rockcutting Wheel dependency is repointed to `automation_ore/crushing`.
- From Heat: `auto_diamond`, `auto_netherite`. Heat Automation keeps Blaze Cakes and Biofuel.

## Rewards
Automate rule, +2 levels per item quest, capstones Spoils of War II, **Ore Automation Mastered** +20 levels + War
Trophy. Chapter unlock: Brass Casing (same as Brass Automation; Crushing Wheels need mechanical crafting).

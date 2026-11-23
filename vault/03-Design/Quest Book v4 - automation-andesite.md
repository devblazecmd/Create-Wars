---
tags: [design/progression, mc-version/1.21.1, loader/neoforge]
status: approved
---

# Spec: automation-andesite (deepen Andesite Automation)

Follow-up of [[Quest Book v4 - automation-breakout]] ("deepen each tier chapter"). Parent: [[Quest Book]].
Model: [[Quest Book v4 - automation-agriculture]].

## Objective
Owner (2026-11-23): "now with what weve done with ag we need to do to andesite". Today Andesite Automation is one
bubble with 6 quests. Make it the same kind of page as Agriculture: every Andesite-tier material, part and machine
as an automate quest, grouped by the machine or method that makes it, with group capstones and a finale.

## Structure
One circle (hub: the existing **Andesite Automation** quest) with method groups around it, laid out with the
Agriculture ring helpers. Each group ends in a "<group> Mastered" capstone; all of them feed **Andesite Mastered**.

| Group | Items (stack each; *kept* = existing quest, same ID) |
|---|---|
| **Stone** (generators + drill) | cobblestone *(kept)*, stone, smooth stone, andesite, diorite, granite, basalt, cobbled deepslate, obsidian, limestone, scoria |
| **Milling & Crushing** | gravel *(kept)*, sand, red sand, cinder flour, powdered obsidian |
| **Washing** (fan through water) | flint, clay ball, gold nugget, quartz |
| **Fan Processing** (fire / lava) | stone→glass, charcoal, brick, terracotta, dried kelp *(kept)* |
| **Metals** | iron nuggets/ingots/blocks *(kept)*, gold ingot, iron sheets *(kept)*, golden sheet, andesite alloy *(kept)* |
| **Kinetic Parts** | shaft (Saw cuts alloy), cogwheel, large cogwheel (Deployers), belt connector, andesite casing (alloy applied to stripped logs), gearbox, andesite tunnel, chute, basin |

40 items. Every ID above exists in the live registry. Every item has a loaded recipe or
a generator (cobble/basalt/obsidian/limestone/scoria). Descriptions come from the recipe export, as in Agriculture.

## Rewards
- Automate rule (already global): no item bonus, ×2 XP, one Engineer's Cache roll.
- Item quests: **+2 levels** (owner), same as Agriculture. The 6 kept quests drop from +3 to +2.
- Group capstone: levels = half the group (min 5) + Spoils of War I roll(s). **Andesite Mastered**: +15 levels + War
  Trophy roll.

## Keeping progress
The 6 existing quests keep their slugs (IDs come from `id_chapter="automation"`). Checked with `tools/quest_ids.py`.

## Testing
Generator layout checks; ref check 0 unknown; audit 0 hidden / order / stack; ID diff = only additions plus the
kept quests' new dependencies; boot; owner review in game.

## Decisions (owner, 2026-11-23)
- No Machines group: "leave out machines but tunnels chute and basins would be needed just like gearboxes cogs and
  casings". Andesite Tunnel, Chute and Basin join Kinetic Parts.
- +2 levels per item quest, like Agriculture.

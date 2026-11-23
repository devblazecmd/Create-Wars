---
tags: [design/progression, mc-version/1.21.1, loader/neoforge]
status: approved
---

# Spec: automation-breakout

Module of [[Quest Book v4 - Capability Map]]. Parent spec: [[Quest Book]].

## Objective
Owner (2026-11-23): "bring back the automation tab then break automation tab out and we can get deeper
into, might leave things like ore a little light but should allow for a better flow". Owner picked **one
chapter per tier**.

Today the Automation tab has one chapter with 7 bubbles. This module splits it into **one chapter per
tier**, so each can grow on its own page. It's a **restructure only**: same quests, same progress. Going
deeper into each tier is follow-up work. Ore/basics can stay light, as the owner said.

## Result (Automation tab, in this order)
| Chapter (slug) | Quests moved in | Chapter unlock (was the bubble's extra dep) |
|---|---|---|
| Andesite Automation (`auto_andesite`) | `andesite_auto` hub, cobble, gravel, alloy, iron, sheets, kelp | `kinetics/casing` |
| Brass Automation (`auto_brass_tier`) | `brass_auto` hub, brass, tubes, precision, crushing → zinc | `brass_and_precision/brass_casing` |
| Heat Automation (`auto_heat`) | `heat_auto` hub, blaze cakes, diamonds, netherite, biofuel | `heat/blaze_cake` |
| Industrial Automation (`auto_industrial`) | `industrial_auto` hub, coke, steel, gasoline | `industrial/steel` |
| Quantum Automation (`auto_quantum`) | `quantum_auto` hub, telejuice | `quantum/telejuice` |
| Enchanting Automation (`auto_enchanting`) | `enchanting_auto` hub, liquid XP | `enchanting/liquid_xp` |
| Agriculture (`agriculture`) | built by [[Quest Book v4 - automation-agriculture]] | `kinetics/casing` |

The final slugs are picked during the build so they don't collide with existing quest slugs. Each
chapter keeps the bubble's current hub-and-spoke layout, now centered on its own page.

## Keeping progress
Quest, task and reward IDs come from `qid(chapter_slug, quest_slug, ...)`. The generator gains a
per-chapter (or per-quest) **`id_chapter`** override: moved quests keep using `"automation"` for their IDs,
so team progress and claimed rewards survive. The old `automation` chapter is removed. Its chapter ID
holds no progress.

Cross-chapter references to moved quests are updated: Rail Warfare's `rockcutting_wheel` needs
`automation/crushing` → the new Brass Automation chapter (same quest ID thanks to the override).
`tools/audit_quests.py` (`ACCEPTED_ORDER`, any `automation/...` keys) is updated to match.

## Commands
```
python -I tools/quests/build_quests.py
python -I tools/check_quest_refs.py
python tools/audit_quests.py --instance "C:/Users/blake/AppData/Roaming/PrismLauncher/instances/Create Wars - Testing/minecraft"
cd pack && packwiz refresh
```
Close the game before syncing, then `cmp`.

## Testing
1. **ID equality check (scripted):** before the change, dump `{quest/task/reward id}` from
   `chapters/automation.snbt`. After it, the union of the 6 new chapter files contains exactly the same IDs
   (except the old food bubble, which moves to Agriculture with the same IDs).
2. Generator runs clean; ref check 0 unknown; audit 0 order gaps.
3. Boot: 0 FTB Quests errors. In a world with existing progress, completed automate quests stay
   completed.

## Boundaries
- Always: keep every quest/task/reward ID; update cross-references; log the change in the decisions log.
- Ask first: adding new automate quests to tier chapters (that's "go deeper" follow-up work, not this module).
- Never: let a moved quest get a new ID.

## Success criteria
- [ ] Automation tab shows 6 tier chapters (+ Agriculture from its module), in tier order.
- [ ] The old single Automation chapter is gone.
- [ ] ID equality check passes; clean boot; existing progress intact.

## Follow-ups (not in this module)
- Deepen each tier chapter (owner: "we can get deeper into", ore can stay light). Each tier gets its own
  small spec when picked up.
- Quantum (1 quest) and Enchanting (1 quest) are thin pages until deepened.

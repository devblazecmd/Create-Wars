---
tags: [design/progression, mc-version/1.21.1, loader/neoforge]
status: approved
---

# Spec: automation-brass (deepen Brass Automation)

Follow-up of [[Quest Book v4 - automation-breakout]]. Same pattern and rules as [[Quest Book v4 - automation-andesite]]
(owner 2026-11-23: "now do the same for brass"): no machines, logistics parts in, +2 levels per item quest, a
"<group> Mastered" capstone per group and a master capstone. Built with the shared grouped-chapter builder.

## Groups (stack each; *kept* = existing quest, same ID)
| Group | Items |
|---|---|
| **Ore Processing** (entry quest: the existing *Crushing Wheels*) | crushed raw iron, gold, copper, zinc, lead, nickel; zinc ingot *(kept)*; zinc nugget; nugget of experience |
| **Brass** | brass ingot *(kept)*, brass nugget, block of brass, brass sheet, block of zinc |
| **Rose Quartz** | redstone dust, rose quartz, polished rose quartz, electron tube *(kept)* |
| **Precision** | precision mechanism *(kept)*, brass hand, sand paper (16), red sand paper (16) |
| **Brass Logistics** | brass casing, brass funnel, brass tunnel, smart chute, empty blaze burner |

27 automate quests. Uranium (crushed) is left to the Nuclear Age. Sand paper stacks to 1, so it asks for 16.

## Rewards
Automate rule (no item bonus, ×2 XP, Engineer's Cache roll), +2 levels per item quest. Capstones: half the group
(min 5) + Spoils of War II. **Brass Mastered**: +20 levels + War Trophy.

## Keeping progress
`brass_auto`, `crushing`, `auto_brass`, `auto_zinc`, `auto_tubes`, `auto_precision` keep their IDs (`legacy`).
`crushing` stays a build-the-machine quest (Rail Warfare's Rockcutting Wheel depends on it) and becomes Ore
Processing's entry quest. The 4 old automate quests drop from +3 to +2 levels.

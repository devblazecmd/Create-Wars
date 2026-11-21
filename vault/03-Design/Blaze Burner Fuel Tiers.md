---
tags: [design]
---

# Blaze Burner Fuel Tiers

**Script:** `pack/kubejs/server_scripts/blaze_burner_tiers.js`

## Why fuel tiers and not heat tiers
Create has exactly four heat levels (none, Smouldering, Kindled, Seething/superheated). KubeJS can't add
a level above Seething. That needs a Java addon, which would settle the open curated-vs-custom-mods
decision. No existing 1.21.1 mod adds one either. On 2026-11-21 the project owner chose a **fuel
progression** instead: the three superheat fuels already in the pack become tiers, and each tier's fuel
needs the previous tier's superheat to produce.

[Create: Superheated](https://www.curseforge.com/minecraft/mc-mods/create-superheated) (a late-game
chain plus a heat-capping thermostat, built on Create Connected + Crafts & Additions) was considered and
not added for now.

## Tiers
| Tier | Fuel | Burner | Burn per unit | Gate |
|---|---|---|---|---|
| 1 | Blaze Cake | Blaze Burner | 3,200 ticks (2 m 40 s) per cake | None. Starting point, unchanged |
| 2 | Biofuel | Blaze Burner with Straw ([[../01-Mods/Create Crafts & Additions\|C&A]]) | 24,000 ticks (20 min) per 1,000 mB | Bioethanol mixing now **superheated** (was unheated) |
| 3 | Napalm | Blaze Burner with Straw | 72,000 ticks (1 h) per 1,000 mB (**new**) | Napalm mixing now **superheated + 250 mB biofuel** (was unheated aluminum + gasoline) |

Progression: cakes bootstrap a biofuel plant → biofuel can then run its own mixer → biofuel and
superheat feed napalm production → napalm is the longest-lasting fuel.

## Things found while building this
- TFMG ships a napalm superheat entry for blaze burners (`data/createliquidfuel/data_maps/...`), but it
  only works with the Create: Liquid Fuel mod, which **isn't in the pack**. Before this script, napalm
  could not superheat anything. The C&A `liquid_burning` recipe is what makes it a fuel now.
- TFMG's Firebox heats machines above it but runs on LPG/butane/diesel/propane/naphtha/kerosene, not
  napalm.

## Balance side effects
- Napalm is also a weapon (Napalm Bomb, Napalm Potato, flamethrower fuel). Requiring biofuel and
  superheat makes those weapons more expensive too. Watch this in PvP.
- Biofuel used to be an early, unheated product. It now needs a working blaze-cake setup first.

## Not done yet
- No recipes are gated *on* a tier yet. Create can only check "superheated", not which fuel did it.
  To make higher tiers unlock things, high-value recipes would need a tier's fuel as an ingredient (for
  example, the [[Diamond Recipe]] could require some biofuel).
- Not tested in game yet.

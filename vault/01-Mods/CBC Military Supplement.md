---
tags: [mod/status/testing, mod/category/combat, mc-version/1.21.1, loader/neoforge]
mod_id: cbc-more-shells
pack_version_pinned: "3.0.7-1.21.1 (CBC-Military-Supplement-1.21.1-3.0.7.jar)"
last_verified: "2026-11-20 (added via packwiz; not yet boot-tested - see Changelog)"
---

# CBC Military Supplement

**Source:** [Modrinth](https://modrinth.com/mod/cbc-more-shells)

## Role in Create Wars
Torpedoes, aerial bombs, and extra shell types for [[Create Big Cannons]]. Torpedoes give [[Create Deep Seas]] submarines a real weapon.

## Dependencies
- Hard requires: [[Create Big Cannons]], [[Shaolib]], [[Shaolib Munitions]]

## Version notes
Added via `packwiz modrinth add cbc-more-shells` on 2026-11-20; resolved to `3.0.7-1.21.1`.

## Known issues
Modrinth slug is `cbc-more-shells` but the display name is "CBC Military Supplement".
- 2026-11-22: `racked_torpedo`, `he_bouncing_bomb`, `aphe_bouncing_bomb`, `depth_charge`,
  `torpedo_detection_device` and `rocket_bracket` have no recipe in 3.0.7 (block loot tables only). The rocket
  bracket is also an ingredient of the Dual rockets, so those couldn't be made either. Pack recipes added in
  `missing_recipes.js`. [[../02-Bugs/Quest items with no survival recipe]]

## Config decisions
None yet.

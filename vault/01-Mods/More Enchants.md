---
tags: [mod/status/testing, mod/category/combat, mc-version/1.21.1, loader/neoforge]
mod_id: moreenchantments
pack_version_pinned: "1.2.1+mod (moreenchantments-1.2.1.jar)"
last_verified: "2026-11-22 (client boot into world, clean load; enchantments not tried)"
---

# More Enchants

**Source:** [Modrinth](https://modrinth.com/datapack/moreenchantments) (owner linked it 2026-11-22). Published as a datapack
*and* a mod jar; packwiz installed the jar.

## Role in Create Wars
21 extra enchantments (namespace `enchantments:`), read from the 1.21.1 jar: attack_speed, big_foot, block_reach,
burning_protection, curse_of_giantism, curse_of_smallism, entity_reach, frozen, glow, gravity, haste, healthy,
invisibility, jump, knockback_protection, lifesteal, shulker, speed, strength, villager_healer, wither. The newer ones
on the mod page (Banshee, Necromancer, Ghoul, Forbidden...) are **not** in the 1.21.1 build.

## Dependencies
None.

## Version notes
Added via `packwiz modrinth add moreenchantments` 2026-11-22; resolved to 1.2.1+mod. `side = "both"`.

## Known issues
None in the boot log.

## Open questions (flagged to owner) - PvP balance
- **Healthy** (armor, max 3): extra max health per piece. **Strength** (weapon, max 3): flat attack damage.
  **Speed** V / **Jump** V boots. **Attack Speed** III swords. **Entity Reach** III (turtle helmet).
- **Invisibility** (weapon): invisibility effect on hit. **Shulker** (bow): levitates the target.
- **Gravity** (armor): changes gravity; with Jump V it may let players float or glide, which works against the elytra
  ban's "air travel goes through Aeronautics" intent. Not tested.
- Stacks with Illager Invasion's Imbuing Table (over-max levels).

## Test enchantments removed from play (2026-11-22, owner: "testing enchants ... cut those")
The jar ships 8 leftover test enchantments, `enchantments:test_entity_effect/{hit_block, location_changed,
post_attack_aa, post_attack_av, post_attack_va, post_attack_vv, projectile_spawned, tick}` (each runs a debug function).
They aren't in any enchanting/trade tag, but they appeared as books in JEI and could be rolled by loot that enchants
from the whole registry. A datapack can't delete a registry entry, so each is overridden in
`pack/kubejs/data/enchantments/enchantment/test_entity_effect/` to apply to `#createwars:none` (an empty item tag) with no
effects, and `pack/kubejs/client_scripts/hide_test_enchants.js` hides their books from JEI. Verified: `canEnchant` is
false for them, the world loads, More Enchants' real enchantments (e.g. Strength) are unaffected.


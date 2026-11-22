---
tags: [mod/status/testing, mod/category/combat, mc-version/1.21.1, loader/neoforge]
mod_id: illager-invasion
pack_version_pinned: "v21.1.6-1.21.1-NeoForge (IllagerInvasion-v21.1.6-1.21.1-NeoForge.jar)"
last_verified: "2026-11-22 (client boot into world, clean load; not fought yet)"
---

# Illager Invasion

**Source:** [Modrinth](https://modrinth.com/mod/illager-invasion)

## Role in Create Wars
Owner 2026-11-22: "Yes, Illager Invasion" for new illager mob types. A port of Illager Expansion. New illagers:
Provoker, Basher, Marauder, Inquisitor, Alchemist, Firecaller, Sorcerer, Archivist, Necromancer (raises
Surrendered), Illusioner spawning, and the **Invoker** boss (boss bar). They join vanilla raids
(`participate_in_raids = true`, except the Invoker). New structures: Illager Fort, Labyrinth, Illusioner Tower,
Firecaller Hut, Sorcerer Hut. Items: platinum (trims), Hallowed Gem, Horn of Sight, magical fire charge, the
**Imbuing Table**.

Quests: Know Your Enemy, second row under Raiders: "Illager Invasion" hub (Provokers), chains for the rest, and
"The Invoker" boss (10 levels + War Trophy roll).

## Dependencies
- Puzzles Lib (added with it).

## Version notes
Added via `packwiz modrinth add illager-invasion` 2026-11-22. Last upstream release for 1.21.1 is 2025-05; check it
still loads on every NeoForge bump.

## Known issues
None in the boot log.

## Open questions (flagged to owner)
- **Imbuing Table** pushes enchantments one level past their maximum (needs a max-level book). Strong for PvP gear.
  Keep it, nerf it, or remove it? Not decided.
- Mob-side balance is a standing open decision (CLAUDE.md). Improved Mobs buffs these like any other mob.

## Config decisions
None (defaults in `config/illagerinvasion-server.toml`).

---
tags: [mod/status/testing, mod/category/tooling, mc-version/1.21.1, loader/neoforge]
mod_id: lootedit
pack_version_pinned: "1.0.0 (lootedit-1.0.0.jar, raw jar in pack/mods/)"
last_verified: "2026-11-21 (client boot + world load on NeoForge 21.1.267)"
---

# Loot Edit

**Source:** custom, written by the project owner. Not on Modrinth or CurseForge.

## Role in Create Wars
Pack tooling for viewing, exporting and editing every loot table in the game.
- On server start it exports every loot table as JSON to `config/lootedit/export/<namespace>/...` (4,969
  tables on first run).
- Overrides placed in `config/lootedit/overrides/data/<namespace>/loot_table/<path>.json` load as a
  built-in datapack (`lootedit_overrides`) at top priority.
- Adds in-game commands for browsing tables.

## Dependencies
- Hard requires: NeoForge `>=21.1.267` (this is why the pack's NeoForge was bumped from 21.1.249; see
  [[../04-Changelog/Changelog|Changelog]]), Minecraft `1.21.1`
- Code only uses long-standing NeoForge APIs (AddPackFindersEvent, OnDatapackSyncEvent,
  RegisterCommandsEvent), so the 267 minimum is just the build environment, not a real API need.

## Version notes
- Not managed by packwiz metadata. The jar sits directly in `pack/mods/` and `packwiz refresh` indexes it
  by hash. **To update:** replace the jar in `pack/mods/` and run `packwiz refresh`. `packwiz update`
  will never touch it.
- Code reviewed 2026-11-21 with `javap`: file I/O stays under `config/lootedit/`, with no network or
  process execution.

## Known issues
- Exports only loot *tables*. Global loot modifiers (how Sophisticated Backpacks and CBC More Shells
  inject into vanilla chests) don't appear inside the vanilla table's JSON, only as their own `inject/`
  or `chests/` tables. Tables that fail to parse at load (the 309 Steam 'n' Rails ones) are missing from
  the export.

## First export findings (2026-11-21)
`export/index.json` lists every table with its type, pool count and every item it can drop. 4,969
tables: 4,757 block drops, 101 entity, 78 chest, 16 gift, plus archaeology, fishing and others.
- No table drops `minecraft:elytra`, which confirms [[../03-Design/Elytra Removal]].
- No table drops the removed Air War launchers/ammo.
- Diamonds come from 17 chest/archaeology/pot tables besides ore (End City, bastion, buried
  treasure, trial chambers, village smiths, etc.). This matters for [[../03-Design/Diamond Recipe]] balance.
- Weapon content in chests: CBC More Shells puts torpedo molds and cannon combos in bastion and
  shipwreck chests (18 entries).

## Config decisions
- Loot overrides from this tool live in the *instance's* `config/lootedit/overrides`. If overrides
  become part of the pack, copy them into `pack/config/lootedit/overrides/` so packwiz ships them.
- First custom mod in the pack. That bears on the open "curated-only vs custom mods" decision in
  CLAUDE.md, which hasn't been formally closed.

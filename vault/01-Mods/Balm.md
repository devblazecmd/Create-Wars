---
tags: [mod/status/active, mod/category/dependency, mc-version/1.21.1, loader/neoforge]
mod_id: balm
pack_version_pinned: "balm-neoforge-1.21.1-21.0.67.jar (updated 2026-11-20 from balm-neoforge-1.21.1-21.0.65.jar)"
last_verified: "2026-11-20 (packwiz update --all; not yet boot-tested)"
---

# Balm

**Source:** [Modrinth](https://modrinth.com/mod/balm) · BlayTheNinth — a common cross-loader library used by
many mods.

**Why this is here:** neither Modrinth nor CurseForge listed this as a declared dependency for
[[Waystones]] or [[Create Waystones Recipes]] when they were added via packwiz — it only surfaced as a hard
crash (`ModLoadingException`) during an actual headless NeoForge server boot test. This is exactly the gap
packwiz's dependency auto-resolution can't catch: it only knows what a mod's Modrinth/CurseForge metadata
declares, not what the mod actually requires at runtime. See the changelog entry for 2026-09-01 for the
full smoke-test writeup.

## Role in Create Wars
No standalone gameplay role — required at runtime by [[Waystones]] and [[Create Waystones Recipes]].

## Dependencies
- Required by: [[Waystones]], [[Create Waystones Recipes]]

## Version notes
Added via `packwiz modrinth add balm` on 2026-09-01; resolved to `21.0.65`.

## Known issues
None logged yet.

## Config decisions
None yet.

## Update history
- 2026-11-20: `balm-neoforge-1.21.1-21.0.65.jar` -> `balm-neoforge-1.21.1-21.0.67.jar` via `packwiz update --all`.

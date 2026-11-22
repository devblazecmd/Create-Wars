---
tags: [mod/status/testing, mod/category/dependency, mc-version/1.21.1, loader/neoforge]
mod_id: lithostitched
pack_version_pinned: "1.8.1 (lithostitched-1.8.1-neoforge-21.1.jar)"
last_verified: "2026-11-21 (client boot into existing world; new terrain needs a new world)"
---

# Lithostitched

**Source:** [Modrinth](https://modrinth.com/mod/lithostitched)

## Role in Create Wars
Worldgen library. No standalone content.

## Dependencies
- Required by: [[Tectonic]], [[Terralith]]

## Version notes
Added via packwiz on 2026-11-21. **Gotcha:** Modrinth marks it server-side, so packwiz wrote `side = "server"` and the client installer skipped it. Single-player crashed (Tectonic). Fixed to `side = "both"` on 2026-11-21. See [[Mod List]] distribution gotchas.

## Known issues
None logged yet.

## Config decisions
None yet; defaults.

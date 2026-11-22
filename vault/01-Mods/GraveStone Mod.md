---
tags: [mod/status/testing, mod/category/utility, mc-version/1.21.1, loader/neoforge]
mod_id: gravestone
pack_version_pinned: "1.0.40 (gravestone-neoforge-1.21.1-1.0.40.jar)"
last_verified: "2026-11-21 (client boot into world, clean)"
---

# GraveStone Mod

## Role in Create Wars
Puts a grave with your items where you die (owner request "need a graves plugin", 2026-11-21).

## Dependencies
- Hard requires: none
- Add-ons: [[Gravestone x Curios API Compat]], [[Gravestone and Sable Compatibility Patch]]

## Version notes
Added via packwiz on 2026-11-21.

## Known issues
None logged yet.

## Config decisions
- 2026-11-21 (owner): `pack/config/gravestone-server.toml` now ships with the pack. **`only_owners_can_break = true`**: only the dead
  player (and admins) can open a grave, so a PvP death costs the trip back, never the gear. **`sneak_pickup = true`**:
  crouch on the grave (or break it) to get your items back into their slots. Everything else is default (obituary on,
  no ghost).

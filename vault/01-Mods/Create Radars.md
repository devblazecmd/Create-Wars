---
tags: [mod/status/active, mod/category/radar, mc-version/1.21.1, loader/neoforge]
mod_id: create-radars
pack_version_pinned: "0.4.9.4 (create_radar-0.4.9.4-1.21.1.jar)"
last_verified: "2026-09-01 (auto-added as a dependency of CBC Aeronautics Missiles via packwiz)"
---

# Create: Radars

**Source:** not yet directly researched — pulled in automatically as a dependency, not searched for by name.
Find its own Modrinth/CurseForge page before writing config/balance decisions here.

## Role in Create Wars
Discovered as a dependency of [[CBC Aeronautics Missiles]], not something we searched for directly. This is
a Create-native radar addon (as opposed to [[Mob Radar]], which is a standalone non-Create mod). Given that
[[CBC Aeronautics Missiles]] ships explicit "Create: Radars Compat," this is very likely the *intended*
radar system for missile targeting/detection in this pack — worth treating as more central than Mob Radar.

**Open decision:** we now have two radar mods ([[Mob Radar]] and this one) with overlapping purpose. Decide
whether to keep both (different use cases — e.g. Mob Radar for general mob/player detection, Create: Radars
for missile-guidance-specific detection) or drop one. Don't resolve this unilaterally in code — flag it and
decide deliberately once both are testable in-game.

## Dependencies
- Required by: [[CBC Aeronautics Missiles]]
- Likely requires [[Create]] itself; not yet confirmed independently.

## Version notes
Auto-resolved and added by `packwiz curseforge add create-simulated-missiles-create-aeronautics` on
2026-09-01; pinned at `0.4.9.4`.

## Known issues
None logged yet.

## Config decisions
None yet — pending the Mob Radar overlap decision above.

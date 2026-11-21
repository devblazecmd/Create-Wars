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

**Resolved 2026-11-21:** Mob Radar was removed; Create: Radars is the radar system. *(Original note:*
we had two radar mods ([[Mob Radar]] and this one) with overlapping purpose. Decide
whether to keep both (different use cases — e.g. Mob Radar for general mob/player detection, Create: Radars
for missile-guidance-specific detection) or drop one. Don't resolve this unilaterally in code — flag it and
decide deliberately once both are testable in-game.*)

## Dependencies
- Required by: [[CBC Aeronautics Missiles]]
- Likely requires [[Create]] itself; not yet confirmed independently.

## Version notes
Auto-resolved and added by `packwiz curseforge add create-simulated-missiles-create-aeronautics` on
2026-09-01; pinned at `0.4.9.4`.

## Integration map (checked 2026-11-21 from jar metadata + bytecode, not yet in game)
Create: Radars is the **hub** of one connected radar/fire-control network:
- [[CBC Aeronautics Missiles]] `0.2.0`: hard-requires Radars `[0.4.9.4, 0.5.0)` (`CreateRadarsAdapter`
  reads radar tracks for missile guidance). **This cap is why Radars must stay on 0.4.x**: the 5.x line
  would stop the game from loading.
- [[Create Radar Fire Arc Filter]] `1.0.0`: hard-requires Radars `>=0.4.4`; adds no-fire sectors to
  radar-driven cannon mounts (39 classes hook Radars).
- [[CBC Firepower Components]]: optional mixin compat that applies its mount speed upgrades to
  Radars' auto-aim controllers.
- Radars itself requires [[Create Big Cannons]] (in pack), and its jar has **built-in Sable/Aeronautics
  support** (23 classes), so radars on Aeronautics ships are expected to work. Its Valkyrien Skies
  compat is irrelevant here (VS not in pack).

**Separate systems that do NOT talk to Create: Radars** (no class references either way):
- [[Create The Air War]]: own Sonar, Monitor, Aircraft Monitor, camera/Target Gunner Gadget.
- [[Create Deep Seas]]: own Sonar (submarines).
- [[Create Misc and Things]]: a "Radar" block.
- ~~[[Mob Radar]]~~: removed 2026-11-21.
- [[Create Misc and Things]]: also a handheld "Radar" item that reveals nearby entities.
- Name clashes players will see in JEI: two "Monitor" blocks (Radars, Air War) and two "Sonar" blocks
  (Air War, Deep Seas).

## Known issues
None logged yet.

## Config decisions
None yet — pending the Mob Radar overlap decision above.

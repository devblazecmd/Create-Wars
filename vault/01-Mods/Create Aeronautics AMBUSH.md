---
tags: [mod/status/testing, mod/category/combat, mod/category/vehicles, mc-version/1.21.1, loader/neoforge]
mod_id: ambush
pack_version_pinned: "1.1.8 (ambush-1.1.8.jar)"
last_verified: "2026-11-21 (client boot into world, clean load)"
---

# Create Aeronautics: AMBUSH

**Source:** [Modrinth](https://modrinth.com/mod/ambush)

## Role in Create Wars
A datapack-driven encounter engine for PvE. It adds ambushes with triggers, multi-wave assaults, bosses,
arrow storms, enemy **airship fleets** and ground vehicles that use [[Create Aeronautics]]/Sable ships
and [[Create Big Cannons]] cannons. It makes the "war" side of the pack two-way: enemies show up with
the same tech you're building. Owner request 2026-11-21.

The jar ships these defaults (the boot log counts):
- 205 ambush definitions, 35 ship action profiles (cast-iron raider/interceptor ships, anti-air and
  artillery cars, an illager drill car, a fishing-fleet convoy boss, and more).
- 6 factions: illager, piglin, undead, End, villager, neutral. Villagers can be friendly support and
  send periodic gifts.
- 4 invasion profiles: standard, naval, ground defense, endless.
- **Natural airship spawns** (`ambush_natural_airship_curves/default.json`): enemy ships can show up
  without a command.

## Dependencies
All optional, but NeoForge still enforces each version range when that mod is installed. Checked
2026-11-21 against the pack:
| Mod | Range | Pack |
|---|---|---|
| [[Sable]] | `[2.0.3,2.1)` | 2.0.6 ✓ |
| [[Create]] | `[6.0.10,6.1)` | 6.0.10 ✓ |
| [[Create Aeronautics]] / Simulated | `[1.3.0,1.4)` | 1.3.3 (bundled) ✓ |
| [[Create Big Cannons]] | `[5.11.7,6)` | 5.11.7 ✓ |
| FTB Quests | `[2101.1.30,)` | 2101.1.39 ✓ |

**Version bump warning:** these ranges are tight (Sable 2.0.x, Aeronautics 1.3.x, Create 6.0.x). Bumping
any of those mods past the range will **stop the game from loading** until AMBUSH updates too. Recheck
this table on every bump.

Modrinth lists Guard Villagers and Lootr as optional for older versions. Neither is in the pack.

## Version notes
Added via `packwiz modrinth add ambush` on 2026-11-21; resolved to `1.1.8`. Its Modrinth metadata
declares no dependencies, so the table above was read from the jar's `neoforge.mods.toml`. The log line
"Enabled optional FTB Quests integration" means it can hook into quests (not explored yet).

## Known issues
None in the boot log. Not playtested yet.

## Config decisions
None yet; `config/ambush-common.toml` is at default and is **not** shipped in `pack/config/`.
**Open (performance and balance):** the defaults allow 64 natural airships per player and 64 globally,
and up to 50 ships and 200 entities per invasion. That's a lot of Sable physics bodies on a multiplayer
server. Tune it after a playtest. This ties into the open mob-balance decision (see [[Mod List]], PvE threat).

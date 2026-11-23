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
- 2026-11-21 (owner): `pack/config/ambush-common.toml` now ships with the pack.
  `maxNaturalActiveShipsPerPlayer` 64 → **8**, `maxNaturalActiveShipsGlobal` 64 → **16**,
  `invasionMaxSimultaneousShips` 50 → **12**, `invasionMaxLiveEntities` 200 → **80**. Everything else is default.
  Reason: each ship is a Sable physics body, and these defaults were sized for single-player.

Older note (before the caps):
**Open (performance and balance):** the defaults allow 64 natural airships per player and 64 globally,
and up to 50 ships and 200 entities per invasion. That's a lot of Sable physics bodies on a multiplayer
server. Tune it after a playtest. This ties into the open mob-balance decision (see [[Mod List]], PvE threat).

## Quest hook (used 2026-11-21)
FTB Quests integration: a quest tagged `ambush:trigger:<namespace:id>` runs `AmbushRuntime.triggerChained`
for the team's online members when the quest is **started** (IDs without a namespace get `ambush:`).
The pack defines its own ambush in `pack/kubejs/data/createwars/ambushes/quest_raiding_party.json` (6
pillagers + 2 vindicators, `chance: 0` so it never fires naturally). It's used by Know Your Enemy →
**Raiding Party** (checkmark to start, then kill 6 pillagers). It loaded (206 definitions, 0 rejected).
**Confirmed in game 2026-11-21:** clicking the checkmark logs `Ambush command id=createwars:quest_raiding_party
target=<player> force=true result=true`, and the raiders arrived (a vindicator killed a villager seconds later).
The owner's first try didn't fire because the checkmark never registered (the quest wasn't started).
Likely cause: clicking while in FTB Quests **edit mode**. Test quests with edit mode off.
- 2026-11-21: Quest-driven waves for **Defend Your Home**: custom `createwars:quest_scouting_party`,
  `quest_raiding_party` (reworked: spawns 12 blocks away, targets the quest owner, glowing, "Raid Captain" boss
  bar), `quest_warband`, `quest_siege`, plus 4 built-in vehicle/airship ambushes. All custom ones use `chance: 0`.

- 2026-11-22 (owner: mobs overwhelming): natural ambush caps lowered: `maxNaturalActiveShipsPerPlayer` 8 -> **3**,
  `maxNaturalActiveShipsGlobal` 16 -> **8**. Defend Your Home quest waves are unaffected (they're triggered).

## Grace period and raid gap (2026-11-23)
Owner: "ambush needs a grace period starting fresh hitting raids are very hard to fight", "10hrs of real playtime",
"there NEEDS to be time between raids so they cant spawn back to back", "2hrs". AMBUSH has no grace setting.
`pack/kubejs/server_scripts/ambush_grace.js` drives its one server-wide switch, `/ambush admin spawning` (a toggle that
returns the new state, 1 = on; saved with the world; quest-forced ambushes ignore it):
- OFF for the first **10 hours of play** (server ticks with at least one player online, kept in server persistent data).
- OFF while any `ambush_owned` mob is alive and for **2 hours of play** after the last one is gone.
- Players get a chat line on login while the grace lasts; everyone gets one when it ends.
Server-wide, not per player (owner asked; AMBUSH has no per-player switch). If an op toggles spawning by hand, the
script won't notice until the next state change or restart.
Boot-tested 2026-11-23: first version logged "toggle result undefined" (KubeJS `runCommandSilent` returns nothing here,
so the state couldn't be confirmed and the ambush-mob check always read 0). Fixed: commands go through the vanilla
dispatcher with a `CommandResultCallback` (`ambushRun`). Second boot: "AMBUSH natural spawning OFF (toggle result 0)" and
the login grace message in chat. Ships in the v3 server zip.

---
tags: [mod/status/testing, mod/category/combat, mc-version/1.21.1, loader/neoforge]
mod_id: cbc_more_content
pack_version_pinned: "1.1 (Create_Warnautics-1.1+mc.1.21.1.jar)"
last_verified: "2026-11-21 (client boot into world, clean load)"
---

# Create: Warnautics

**Source:** [Modrinth](https://modrinth.com/mod/create-warnautics). Owner linked
[CurseForge](https://www.curseforge.com/minecraft/mc-mods/create-warnautics); the Modrinth copy was used
because the pack prefers Modrinth.

## Role in Create Wars
A [[Create Big Cannons]] add-on: bombs and explosives that drop with CBC ballistics, plus an optional
Sable "kick" on impact. Owner request 2026-11-21.

Content (read from the jar's lang file):
- **Aerial bombs:** Small (4 variants), Medium, Large, **MOAB**, Bombsight
- **Missiles and rockets:** Cruise Missile, AIM-9 Sidewinder, Rocket Pod Section + S-8 Rocket, Target
  Designator
- **Mines and charges:** Small/Large/Bounding/Sea Mine, Sea Torpedo, M18A1 Claymore, C4 Charge +
  Detonator, Bomb Vest, Tripwire Coil, Wire Cutters
- **Other:** Air-Raid Siren, Chain Coil/Connector, a music disc
- The mod page says nukes are coming in a future version.

**Mod ID gotcha:** the internal mod ID / namespace is `cbc_more_content`, not `warnautics`. Item IDs look
like `cbc_more_content:moab`. This is not [[CBC More Shells]] (`cbcmoreshells`); no clash (checked
2026-11-21).

## Dependencies
Read from the jar; all present 2026-11-21:
| Mod | Range | Pack |
|---|---|---|
| [[Create]] | `[6.0.10,6.1.0)` | 6.0.10 ✓ |
| [[Create Big Cannons]] | `[5.11.0,6.0.0)` | 5.11.7 ✓ |
| [[Sable]] | `[2.0.3,)` | 2.0.6 ✓ |
| Simulated | `[1.3.2,)` | 1.3.3 (bundled in Aeronautics) ✓ |
| [[Create Aeronautics]] | `[1.0.0,)` | 1.3.3 ✓ |
| NeoForge | `[21.1.234,)` | 21.1.267 ✓ |
Optional: Offroad (bundled, installed), Veil, Sable Player Ragdoll, Ragdoll Reactions.

## Version notes
Added via `packwiz modrinth add create-warnautics` on 2026-11-21; resolved to `1.1`. No dependencies are
declared on Modrinth; the table above comes from `neoforge.mods.toml`.

## Known issues
None in the boot log. Not playtested yet.

## Open questions (flagged to owner)
- **Overlap with removed Air War content: resolved 2026-11-21.** [[Create The Air War|Air War]]'s launchers
  and their ammo were removed, and Warnautics adds similar things (AIM-9 Sidewinder, Rocket Pods and S-8
  rockets, Cruise Missile). The owner asked to add Warnautics to the quests, so these **stay** (Demolitions
  chapter).
- **PvP griefing:** MOAB, C4, mines and the Bomb Vest destroy a lot of terrain, and nukes are planned. Does
  this need claim protection (FTB Chunks explosion settings) or a blast-size limit?

## Quests
The **Demolitions** chapter in the Warfare section of the [[../03-Design/Quest Book|Quest Book]] (23 quests).

## Config decisions
None yet.

---
tags: [meta]
---

# Mod List (MOC)

Index of every mod note. Update this when a mod's status changes — don't rely on search alone, since this
is the one page meant to give a whole-pack view at a glance.

Researched 2026-09-01 for **Minecraft 1.21.1, NeoForge**. Pinned into `pack/` on 2026-09-01 via packwiz —
all entries below except the open questions/rejected sections are `#mod/status/active`. See
[[../../README|root README]] for the packwiz workflow.

## Core
- [[Create]] — base building/automation mod everything else hangs off of

## Combat
- [[Create Big Cannons]] — multiblock artillery, autocannons, projectiles/fuzes; explicitly built for PvP
- [[Ritchie's Projectile Library]] — dependency, required by Create Big Cannons

## Vehicles
- [[Create Aeronautics]] — planes, hot-air balloons, offroad vehicles (requires [[Sable]])
- [[Sable]] — dependency library required by Create Aeronautics
- [[Create Crafts & Additions]] — additional vehicle/decoration content for Create

## Drones
- [[Create Droneworks Simulated]] — drone camera + wireless remote controller, addon to Create Aeronautics
- [[Carbon Config]] — dependency, required by Create: Droneworks Simulated

## Radar
- [[Mob Radar]] — reveals nearby mob/player outlines through terrain for a short window

## Storage
- [[Sophisticated Storage]] — upgradeable storage barrels/chests, filtering, auto-crafting
- [[Sophisticated Backpacks]] — portable counterpart to Sophisticated Storage
- [[Sophisticated Core]] — dependency, shared by both Sophisticated mods

## Scripting
- [[KubeJS]] — server/client scripting glue for custom recipes, events, and balance tweaks
- [[Rhino]] — dependency, JS engine required by KubeJS
- [[Better Advanced Tooltips]] — dependency, required by KubeJS

## Not a separate install
- [[Flywheel]] — ships jar-in-jar inside Create's own file for current versions; see its note for why
  `packwiz modrinth add flywheel` fails and shouldn't be retried.

## Not yet researched / open questions
- Trains ([[Steam 'n' Rails]]?) — do we want rail-based logistics/combat, or is that scope creep?
- Mob-side scaling: do vanilla mobs need buffing/reworking to be a real "war" opponent, or is the PvP-style
  gear enough on its own? → open [[Design Doc Template|design doc]] once we decide.

## Rejected candidates
- [[Valkyrien Skies (unofficial port)]] — rejected 2026-09-01, superseded by [[Create Aeronautics]]. Kept
  for history; don't re-add without revisiting what Aeronautics can't cover.

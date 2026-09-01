---
tags: [meta]
---

# Mod List (MOC)

Index of every mod note. Update this when a mod's status changes — don't rely on search alone, since this
is the one page meant to give a whole-pack view at a glance.

Researched 2026-09-01 for **Minecraft 1.21.1, NeoForge**. All entries below are `#mod/status/candidate` —
none are pinned into `pack/` yet. See [[../../README|root README]] for the packwiz workflow that promotes a
candidate to active.

## Core
- [[Create]] — base building/automation mod everything else hangs off of
- [[Flywheel]] — rendering engine dependency required by Create

## Combat
- [[Create Big Cannons]] — multiblock artillery, autocannons, projectiles/fuzes; explicitly built for PvP

## Vehicles
- [[Create Aeronautics]] — planes, hot-air balloons, offroad vehicles (requires [[Sable]])
- [[Sable]] — dependency library required by Create Aeronautics
- [[Create Crafts & Additions]] — additional vehicle/decoration content for Create

## Drones
- [[Create Droneworks Simulated]] — drone camera + wireless remote controller, addon to Create Aeronautics

## Radar
- [[Mob Radar]] — reveals nearby mob/player outlines through terrain for a short window

## Scripting
- [[KubeJS]] — server/client scripting glue for custom recipes, events, and balance tweaks

## Not yet researched / open questions
- Trains ([[Steam 'n' Rails]]?) — do we want rail-based logistics/combat, or is that scope creep?
- Mob-side scaling: do vanilla mobs need buffing/reworking to be a real "war" opponent, or is the PvP-style
  gear enough on its own? → open [[Design Doc Template|design doc]] once we decide.

## Rejected candidates
- [[Valkyrien Skies (unofficial port)]] — rejected 2026-09-01, superseded by [[Create Aeronautics]]. Kept
  for history; don't re-add without revisiting what Aeronautics can't cover.

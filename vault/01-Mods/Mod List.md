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
- [[CBC Aeronautics Missiles]] — guided missiles connecting Big Cannons + Aeronautics + Radars
- [[CBC Military Supplement]] — torpedoes, aerial bombs, extra shells (deps: [[Shaolib]],
  [[Shaolib Munitions]]) *(testing, added 2026-11-20)*
- [[CBC Firepower Components]] — compact cannon mounts for vehicles *(testing)*
- [[CBC Ballistic Computer]] — trajectory calc + redstone-controlled artillery *(testing)*
- [[Create The Air War|Create: The Air War]] — aircraft weapons for Aeronautics *(testing)*

## Infantry / personal weapons
- [[Create Gunsmithing|Create: Gunsmithing]] — steampunk guns crafted via Create machines *(testing)*
- [[NTGL NukaTeam's Gun Lib|NTGL]] — dependency gun library *(testing)*

## PvE threat
- [[Trigger Mobs]] — mobs spawn with and fire Gunsmithing/NTGL guns *(testing)*
- [[Improved Mobs]] — mob gear/stat scaling, block breaking (dep: [[TenshiLib]]) *(testing)*
- [[Enhanced AI]] — breaching creepers, mining zombies, sniping skeletons (dep: [[InsaneLib]]) *(testing,
  beta)*
- Three mods all buff ranged/block-breaking mobs — needs a mob-balance design doc before release.

## Vehicles
- [[Create Aeronautics]] — planes, hot-air balloons, offroad vehicles (requires [[Sable]])
- [[Sable]] — dependency library required by Create Aeronautics
- [[Create Crafts & Additions]] — additional vehicle/decoration content for Create
- [[Create Compact Flap]] — compact flap/gearshift bearings for Aeronautics builds
- [[Hot's Aerostuff]] — link relay, levitite, copycat sails, torsion spring for Aeronautics
- [[Aeronautics Simulated Copycats|Aeronautics: Simulated Copycats]] — copycats with different physical
  properties (weight/drag) for Aeronautics vehicles
- [[Create Aeroworks|Create: Aeroworks]] — flight-control hardware (gyroscope, joystick) for Aeronautics
- [[Create Aeronautics Toolgun|Create Aeronautics: Toolgun]] — gravity gun/towing + blueprint save-print
  tool for Aeronautics contraptions
- [[Create Deep Seas]] — submarines for Aeronautics; opens up underwater combat
- [[Create Aeronautics Kinetic Grip|Create Aeronautics: Kinetic Grip]] — kinetic-powered handles for
  Aeronautics contraptions
- [[Create Aeronautics Throwable Rope Connector|Create Aeronautics: Throwable Rope Connector]] — rope
  docking for airships/submarines
- [[Rolled Homongenous Forked|Rolled Homongenous: Forked]] — armor plate blocks for Aeronautics/CBC
  *(testing)*
- [[Create Armored Constructs|Create: Armored Constructs]] — military armored-vehicle building *(testing)*
- [[Create Bits n Tracks CE|Create: Bits 'n' Tracks CE]] — Sable-driven tank treads *(testing)*

## Trains (scope decided 2026-11-20: in, as armored rail warfare)
- [[Steam 'n' Rails]] — unofficial NeoForge port, beta *(testing)*
- [[CBC Locometal Armor]] — train armor vs. Big Cannons, server-side only *(testing)*
- [[Create Who Touched My Train|Create: Who Touched My Train]] — train locking/permissions *(testing)*

## Drones
- [[Create Droneworks Simulated]] — drone camera + wireless remote controller, addon to Create Aeronautics
- [[Carbon Config]] — dependency, required by Create: Droneworks Simulated

## Radar
- [[Mob Radar]] — reveals nearby mob/player outlines through terrain for a short window
- [[Create Radars|Create: Radars]] — Create-native radar, pulled in by [[CBC Aeronautics Missiles]] for
  missile targeting. **Overlaps with Mob Radar — see [[Mob Radar]] for the open decision.**
- [[Create Radar Fire Arc Filter|Create Radar: Fire Arc Filter]] — no-fire sectors for radar-slaved
  cannons *(testing)*. Its install tried to bump Radars to 5.1.1; reverted to 0.4.9.4 — see its note.

## Storage
- [[Sophisticated Storage]] — upgradeable storage barrels/chests, filtering, auto-crafting
- [[Sophisticated Backpacks]] — portable counterpart to Sophisticated Storage
- [[Sophisticated Core]] — dependency, shared by both Sophisticated mods
- [[Tom's Simple Storage Mod|Tom's Simple Storage]] — networked terminal/connector storage system
- [[Create Contraption Terminals]] — lets Tom's Storage terminals work on moving Create contraptions

## Teams / claims / questing
- [[FTB Teams]] — faction/team system; natural unit for PvP factions
- [[FTB Quests]] — questing/progression, can gate pack progression through quest chains
- [[FTB Chunks]] — chunk claiming/protection tied to FTB Teams, plus map/minimap
- [[FTB Library]] — dependency, shared by all FTB mods above
- [[Architectury API]] — dependency, required by FTB Library
- [[Xaero's Minimap]] — corner minimap: terrain, players, mobs, waypoints
- [[Xaero's World Map]] — full-screen explored-world map, pairs with Xaero's Minimap
- [[FTB Chunks x Xaero's Compat]] — renders FTB claims on Xaero's maps; lets you claim from the map UI

## Scripting
- [[KubeJS]] — server/client scripting glue for custom recipes, events, and balance tweaks
- [[Rhino]] — dependency, JS engine required by KubeJS
- [[Better Advanced Tooltips]] — dependency, required by KubeJS

## Utility / logistics
- [[Create Ender Transmission]] — wireless cross-dimension power/item/fluid transmission for Create
- [[Create Extra Copycats]] — a couple more copycat block types (collapsible, cabinet door)
- [[Create TFMG Community Edition]] — community fork of The Factory Must Grow; heavier industry layer
  (oil, large transformers/switches, electricity). Source on GitHub, but distributed via CurseForge only —
  see its note.
- [[Just Hammers]] — area-mining hammers (3x3 up to 5x5x5 patterns)
- [[Create Waystones Recipes]] — reworks Waystones recipes to fit Create's economy
- [[Waystones]] — dependency, base fast-travel mod required by Create Waystones Recipes
- [[Balm]] — dependency, required by Waystones and Create Waystones Recipes (found via server boot test,
  not declared on Modrinth)
- [[Create Copycats Plus|Create: Copycats+]] — base copycat system; required by Aeronautics: Simulated
  Copycats (found via server boot test, not declared on Modrinth)
- [[Create Bits n Bobs|Create: Bits 'n' Bobs]] — general decorative/mechanical Create additions
- [[Strut Your Stuff (Struts)]] — dependency, required by Create: Bits 'n' Bobs
- [[Azimuth API]] — dependency, required by Create: Bits 'n' Bobs
- [[Create Connected]] — configurable Create QoL blocks; worth a config pass to avoid overlap with other
  addons already installed
- [[Just Enough Items (JEI)]] — recipe/usage viewer, essential once this many mods add recipes
- [[Create Misc and Things|Create: Misc and Things]] — general decorative/technology grab-bag addon
- [[Create New Furnitures|Create : New Furnitures]] — industrial-style furniture matching Create's aesthetic
- [[Create Teleporters]] — point-to-point teleportation; overlaps with the Waystones fast-travel question
- [[CreateBetterFps]] — client-side FPS optimization for Create when shaders are on

## Optimization
- [[Sodium]] — base rendering-optimization engine; now has native NeoForge support (see its note — this
  replaced [[Embeddium]], which was added by mistake first)
- [[Iris Shaders|Iris]] — shader pack loader; replaces "Oculus," which never got a 1.21.1/NeoForge build
- [[Iris and Oculus Flywheel Compat|Iris & Oculus Flywheel Compat]] — keeps Flywheel's optimizations on
  with shaders active, pairs with [[CreateBetterFps]]
- [[ModernFix]] — startup time / memory usage optimization for large packs
- [[FerriteCore]] — memory dedup for block-state/model allocations
- [[Entity Culling]] — skips rendering occluded entities
- [[ImmediatelyFast]] — GUI/immediate-mode rendering optimization
- [[Concurrent Chunk Management Engine]] — multithreaded chunk gen/IO (alpha-status NeoForge port — see
  its note)
- [[Alternate Current]] — redstone update-propagation rewrite; watch for Create-redstone interaction
- [[BadOptimizations]] — misc tick-time micro-optimizations
- [[FastFurnace]] — smelting recipe-match caching
- [[FastWorkbench]] — crafting-table per-slot scan removal
- [[Placebo]] — dependency, required by FastFurnace/FastWorkbench

## Not a separate install
- [[Flywheel]] — ships jar-in-jar inside Create's own file for current versions; see its note for why
  `packwiz modrinth add flywheel` fails and shouldn't be retried.

## Not yet researched / open questions
- ~~Trains ([[Steam 'n' Rails]]?) — do we want rail-based logistics/combat, or is that scope creep?~~
  Resolved 2026-11-20: yes, armored trains (see Trains section).
- Pack is now **PvP and PvE equally** (decided 2026-11-20). Mob scaling is installed ([[Improved Mobs]],
  [[Enhanced AI]], [[Trigger Mobs]]) but untuned — the open question is now *how hard*, not *whether*.
- Mob-side scaling: do vanilla mobs need buffing/reworking to be a real "war" opponent, or is the PvP-style
  gear enough on its own? → open [[Design Doc Template|design doc]] once we decide.
- [[Mob Radar]] vs [[Create Radars|Create: Radars]] vs [[Xaero's Minimap]] entity radar — three overlapping
  detection systems now. See [[Mob Radar]].
- [[Sophisticated Storage]]/[[Sophisticated Backpacks]] vs [[Tom's Simple Storage Mod|Tom's Simple
  Storage]]/[[Create Contraption Terminals]] — two storage paradigms, may both stay for different use
  cases (portable upgrades vs. networked base terminals) — see [[Tom's Simple Storage Mod]].
- "FTB Chunks: Sable Aerospace" addon (protects Aeronautics structures in claimed chunks) was pulled in by
  mistake once and removed — see [[FTB Chunks]]'s note. Worth adding deliberately later.
- Whether to add "FTB Ranks" or other FTB-family mods for finer-grained faction permissions beyond what
  FTB Teams alone provides — not requested yet, flagging as a natural next step for faction design.
- [[Create Teleporters]] adds a *third* fast-travel-adjacent system alongside [[Waystones]] and vehicle
  travel — same balance question, now three-way.
- Three general-purpose "grab bag" Create addons now installed ([[Create Connected]],
  [[Create Bits n Bobs|Create: Bits 'n' Bobs]], [[Create Misc and Things|Create: Misc and Things]]) — worth
  a config pass together once in-game to check for duplicate/overlapping content.

## Distribution gotchas (for future adds)
- **FTB family mods (Teams/Quests/Chunks/Library) are not on Modrinth at all.** `packwiz modrinth add
  ftb-teams` silently falls back to a fuzzy search and grabs the wrong project — always use
  `packwiz curseforge add <slug>-forge` for these (the CurseForge slug keeps a legacy `-forge` suffix even
  for the NeoForge build).
- [[Flywheel]] and the "FTB Chunks x Xaero's Compat" bridge are CurseForge/bundled-only in the same way —
  check a project's actual Modrinth page exists before trusting a guessed slug; a `packwiz modrinth add`
  that returns "Searching Modrinth..." (fuzzy text search) instead of an immediate match is a signal the
  exact slug guess was wrong and the result needs verifying, not just accepting.

## Rejected candidates
- [[Valkyrien Skies (unofficial port)]] — rejected 2026-09-01, superseded by [[Create Aeronautics]]. Kept
  for history; don't re-add without revisiting what Aeronautics can't cover.
- [[Embeddium]] — rejected 2026-09-01, superseded by [[Sodium]] once it became clear Sodium now has native
  NeoForge support and [[Iris Shaders|Iris]] depends on it directly. Don't re-add unless Sodium's NeoForge
  support regresses in a future MC version.

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
- [[Loot Edit]] — **custom** loot-table export/override tool (needs NeoForge >=21.1.267) *(testing)*

## Combat
- [[Better Trims]] — owner's fork of Functional Armor Trim with the dedicated-server crash fixed; trims give stat bonuses *(testing, added 2026-11-22)*
- ~~[[Functional Armor Trim]]~~ — removed 2026-11-22: crashes dedicated servers (loads a client class)
- [[More Enchants]] — 21 extra enchantments (several strong in PvP; flagged) *(testing, added 2026-11-22)*
- [[Create Big Cannons]] — multiblock artillery, autocannons, projectiles/fuzes; explicitly built for PvP
- [[Ritchie's Projectile Library]] — dependency, required by Create Big Cannons
- [[CBC Aeronautics Missiles]] — guided missiles connecting Big Cannons + Aeronautics + Radars
- [[CBC Military Supplement]] — torpedoes, aerial bombs, extra shells (deps: [[Shaolib]],
  [[Shaolib Munitions]]) *(testing, added 2026-11-20)*. Shaolib secretly needs [[Synaxis]]; see
  [[../02-Bugs/Explosions crash - Shaolib missing Synaxis]]
- [[CBC Firepower Components]] — compact cannon mounts for vehicles *(testing)*
- [[CBC Ballistic Computer]] — trajectory calc + redstone-controlled artillery *(testing)*
- [[Create The Air War|Create: The Air War]] — aircraft weapons for Aeronautics *(testing)*
- [[Create Warnautics|Create: Warnautics]] — CBC bombs, MOAB, mines, C4, AIM-9, rocket pods; mod ID
  `cbc_more_content` *(testing, added 2026-11-21)*
- [[CBC Enhanced Shells]] — **only the nukes** (Nuclear Shell Mk.I/II, Mini H-Bomb, H-Bomb); the other ~100
  shells are hidden. Pinned to 1.2.5 for Firepower Components' range. *(testing, added 2026-11-22)*

## Nuclear (added 2026-11-22)
- [[Create Nuclear]] — uranium/thorium, reactors (millions of SU), radiation, meltdowns that leave a
  Wasteland biome. Its uranium rods gate the nukes: [[../03-Design/Nuclear Weapons]] *(testing)*

## Infantry / personal weapons
- [[Create Gunsmithing|Create: Gunsmithing]] — steampunk guns crafted via Create machines *(testing)*
- [[NTGL NukaTeam's Gun Lib|NTGL]] — dependency gun library (dep: [[GeckoLib]]) *(testing)*

## PvE threat
- [[Illager Invasion]] — new illager types + Invoker boss, join raids; Illager Forts, Labyrinths (dep: [[Puzzles Lib]]) *(testing, added 2026-11-22)*
- [[Create Pillager Arise|Create: Pillager Arise]] — 10 Create-built pillager structures (blimp, cathedral, fortress gate, village) *(testing, added 2026-11-22)*
- [[Trigger Mobs]] — mobs spawn with and fire Gunsmithing/NTGL guns *(testing)*
- [[Improved Mobs]] — mob gear/stat scaling, block breaking (dep: [[TenshiLib]]) *(testing)*
- [[Enhanced AI]] — breaching creepers, mining zombies, sniping skeletons (dep: [[InsaneLib]]) *(testing,
  beta)*
- [[Create Aeronautics AMBUSH|Create Aeronautics: AMBUSH]] — ambushes, invasions and enemy airship/vehicle
  fleets using Aeronautics + Big Cannons; natural airship spawns on by default *(testing, added 2026-11-21)*
- Three mods all buff ranged/block-breaking mobs — needs a mob-balance design doc before release. AMBUSH
  adds a fourth PvE threat source (enemy fleets), so it should be part of that doc.

## Vehicles
- [[Synaxis]] — Sable control circuits/Lua/joints/actuators; also a crash fix for [[Shaolib]]
  (deps: [[LDLib2]], [[Sable Photomancy]]) *(testing)*
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
- [[CBC Locometal Armor]] — train armor vs. Big Cannons; `side = both` since 2026-11-22 so it runs in single-player *(testing)*
- [[Create Who Touched My Train|Create: Who Touched My Train]] — train locking/permissions *(testing)*

## Drones
- [[Create Droneworks Simulated]] — drone camera + wireless remote controller, addon to Create Aeronautics
- [[Carbon Config]] — dependency, required by Create: Droneworks Simulated

## Radar
- ~~[[Mob Radar]]~~ — *removed 2026-11-21*; Create: Radars is the radar system
- [[Create Radars|Create: Radars]] — Create-native radar, pulled in by [[CBC Aeronautics Missiles]] for
  missile targeting. The pack's radar system (Mob Radar overlap resolved by removing Mob Radar).
- [[Create Radar Fire Arc Filter|Create Radar: Fire Arc Filter]] — no-fire sectors for radar-slaved
  cannons *(testing)*. Its install tried to bump Radars to 5.1.1; reverted to 0.4.9.4 — see its note.
- Radar integration map (which mods share Create: Radars' network vs. run their own): see
  [[Create Radars]].

## Storage
- [[Sophisticated Storage]] — upgradeable storage barrels/chests, filtering, auto-crafting
- [[Sophisticated Backpacks]] — portable counterpart to Sophisticated Storage
- [[Sophisticated Core]] — dependency, shared by both Sophisticated mods
- [[Tom's Simple Storage Mod|Tom's Simple Storage]] — networked terminal/connector storage system
- [[Create Contraption Terminals]] — lets Tom's Storage terminals work on moving Create contraptions
- [[Sophisticated Storage Create Integration]] — full Sophisticated chests/barrels on moving contraptions
  (vehicle cargo holds) *(testing, added 2026-11-20)*
- [[Create Compatible Storage|Create: Compatible Storage]] — fixes modded chests on contraptions *(testing)*
- [[Create Aeronautics Automated Logistics|Create Aeronautics: Automated Logistics]] — airship cargo routes
  and auto-docking *(testing)*
- **Storage direction decided 2026-11-20:** Sophisticated is the preferred storage family; Tom's stays as
  the networked terminal. Rejected for now: AE2, Refined Storage, Storage Drawers, Create Factory/Meta
  Logistics, Vibrant Vaults.
- **Updated 2026-11-21 (owner):** the plan is for the pack to steer players onto **Tom's Simple Storage** as
  *the* storage network. Sophisticated chests + tier upgrades fill the "chest upgrade" role (no separate
  Iron Chests-style mod). For now this is enforced in the quest book only; Create package logistics and
  the Sophisticated Controller still have recipes. See [[../03-Design/Quest Book|Quest Book]] decisions log.

## World generation (added 2026-11-21)
- [[Create Structures Arise|Create: Structures Arise]] — 28 Create-built structures *(testing, added 2026-11-22)*
- [[Create Let The Adventure Begin|Create: Let The Adventure Begin]] — Create-themed loot structures *(testing, added 2026-11-22)*
- [[Create Aeronautics Structures]] — world-generated hot-air balloons (working/broken) *(testing, added 2026-11-22)*
- [[ChoiceTheorem's Overhauled Village|CTOV]] — biome-styled villages and pillager outposts; `side` fixed to both *(testing, added 2026-11-22)*
- [[Terralith]] + [[Tectonic]] — vanilla-block biomes plus big terrain (dep: [[Lithostitched]]) *(testing)*
- [[Biomes O' Plenty]] — 50+ biomes with new woods (deps: [[TerraBlender]], [[GlitchCore]]) *(testing)*
- [[Incendium]] — Nether biomes and structures *(testing)*
- [[Stellarity]] — full End overhaul; pearls kept, elytras swapped for loot (see note) *(testing)*
- Rejected for now: BetterNether/BetterEnd (no 1.21.1 NeoForge), Nullscape (owner chose Stellarity alone),
  Oh The Biomes We've Gone and Regions Unexplored (overlap with BOP), Amplified Nether, End Remastered.

## Environment / pollution
- [[Pollution of the Realms]] — pollution simulation: smog clouds, acid rain, oil spills, crop and health
  damage (dep: [[ForgeEndertech]]) *(testing, added 2026-11-21)*
- [[Create Smog|Create: Smog]] — Create machines for it: smokestacks, precipitator, air scrubbers, waste
  treatment; runs on top of PoTR *(testing, added 2026-11-21)*
- [[Thick Air]] — no breathable air below Y=0, above Y=128, or in the Nether/End; Create Backtank +
  Diving Helmet works as an air supply (dep: [[Curios]]) *(testing, added 2026-11-21)*. Y=128 acts as an
  aircraft altitude ceiling without oxygen gear.

## Food
- [[Farmer's Delight]] — crops, cutting board, cooking pot, meals and feasts *(testing, added 2026-11-21)*
- [[Create Slice and Dice|Create: Slice & Dice]] — Slicer and Sprinkler that automate Farmer's Delight
  (dep: [[Kotlin for Forge]]) *(testing, added 2026-11-21)*

## Automation / progression
- [[Create Enchantment Industry|Create: Enchantment Industry]] — automated enchanting with liquid XP
  (dep: [[Create Dragons Plus|Create: Dragons Plus]]) *(testing)*

## Death / graves (added 2026-11-21)
- [[GraveStone Mod]] — grave with your items on death; **owner-only**, sneak to recover *(testing)*
- [[Gravestone x Curios API Compat]] (dep: [[BaguetteLib]]) and [[Gravestone and Sable Compatibility Patch]] (graves stay on airships)

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
- [[FTB Ultimine]] — vein mining (hold ` and break); defaults 64 blocks *(testing, added 2026-11-22)*
- [[Lootr]] — per-player structure loot chests; item-frame conversion off to keep elytras out *(testing, added 2026-11-22)*
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
- Client additions 2026-11-22 (owner: "any other client side opti mods"), all `side = "client"`, clean boot:
  **Dynamic FPS** (throttles when unfocused/idle), **More Culling** (leaf/block culling; pulled in **Cloth Config**,
  `both`), **Sodium Extra** (fog/particle/animation toggles), **Reese's Sodium Options** (options menu). Skipped:
  Lithium (server logic; risk with Sable/Aeronautics physics, test separately), Noisium (last update 2024, overlaps C2ME).
- Shader pack: **Complementary Reimagined** r5.10 (`pack/shaderpacks/`, client-only) for [[Iris]] *(added 2026-11-22)*
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
- **`packwiz curseforge add` can rewrite existing dependencies.** Adding [[CBC Enhanced Shells]] (2026-11-22)
  re-wrote `create.pw.toml` and `create-big-cannons.pw.toml` to CurseForge sources. `git diff pack/mods`
  after every CurseForge add, and `git checkout` those files back.
- **Optional dependencies still enforce version ranges.** [[CBC Firepower Components]] only accepts
  CBC Enhanced Shells `[1.2.2,1.3.0)`, and the newest version crashed the game on load. Check
  `neoforge.mods.toml` of the mods already installed, not just the new one.
- **Check `side =` after every `packwiz modrinth add`.** Modrinth marks some libraries server-only (e.g.
  [[Lithostitched]]), so packwiz writes `side = "server"` and the client installer skips the jar. Single-player
  runs an integrated server, so anything the game needs must be `both`. (2026-11-21: Tectonic crashed on
  boot for this reason.) Still server-only on purpose: Alternate Current (doesn't run in single-player). CBC Locometal Armor was
  switched to `both` 2026-11-22 (owner).
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

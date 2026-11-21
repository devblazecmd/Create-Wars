---
tags: [meta]
---

# Changelog

Human-readable history of pack decisions, separate from git log — git tells you *what* changed in files,
this tells you *why*, in prose, per pack version.

## 0.1.0 — 2026-09-01
- Repo scaffolded: Obsidian vault (`vault/`) + packwiz pack skeleton (`pack/`) side by side.
- Target confirmed: Minecraft 1.21.1, NeoForge, packwiz-managed pack.
- Researched initial mod candidate list (all `#mod/status/candidate`, nothing installed yet) — see
  [[../01-Mods/Mod List]].
- Scope decision pending: curated-mods-only vs. also writing custom mods, left open per project owner.
- Rejected [[../01-Mods/Valkyrien Skies (unofficial port)|Valkyrien Skies (unofficial port)]] as a ship
  physics candidate — [[../01-Mods/Create Aeronautics|Create Aeronautics]] covers that role, and avoiding
  an unofficial, unsupported dependency keeps future version bumps simpler.
- Installed dev toolchain: Java 21 (Temurin), Prism Launcher, packwiz CLI (fetched from GitHub Actions
  artifacts via nightly.link since packwiz has no traditional GitHub Releases).
- Ran `packwiz init` for real: `pack/pack.toml` now pins NeoForge `21.1.249` for MC `1.21.1` (was a `TODO`
  placeholder before this).
- Pinned all researched candidate mods into `pack/mods/` via `packwiz modrinth add`/`packwiz curseforge add`:
  Create 6.0.10, Create Aeronautics 1.3.2, Create Big Cannons 5.11.7, Create: Droneworks Simulated 0.1.1,
  Create Crafts & Additions 1.7.0, Mob Radar 1.1.0, KubeJS 2101.7.2-build.374 — plus auto-resolved
  dependencies Sable, Ritchie's Projectile Library, Carbon Config, Rhino, Better Advanced Tooltips.
- Discovered [[../01-Mods/Flywheel|Flywheel]] isn't a separate install for current Create versions — it
  ships jar-in-jar inside Create's own jar. Corrected its vault note (was previously listed as a required
  standalone dependency based on research alone).
- Added storage/logistics: [[../01-Mods/Sophisticated Storage|Sophisticated Storage]] and
  [[../01-Mods/Sophisticated Backpacks|Sophisticated Backpacks]] (sharing the
  [[../01-Mods/Sophisticated Core|Sophisticated Core]] dependency), pinned `1.5.91.2127` and `3.25.78.2107`
  respectively. New `#mod/category/storage` tag added to the taxonomy for these.
- Added seven more requested mods plus their auto-resolved dependencies:
  [[../01-Mods/CBC Aeronautics Missiles]] `0.2.0` (pulled in [[../01-Mods/Create Radars|Create: Radars]] as
  a dependency — a second radar system alongside [[../01-Mods/Mob Radar|Mob Radar]], flagged as an open
  decision), [[../01-Mods/Create Compact Flap]] `1.0.4.1`, [[../01-Mods/Create Ender Transmission]]
  `2.1.1-1.21.1`, [[../01-Mods/Create Extra Copycats]] `1.0.2`, [[../01-Mods/Hot's Aerostuff]] `1.1.7`
  (correcting a naming mix-up — this is not the dead "Create: Hot Stuff" 1.20.1-only addon),
  [[../01-Mods/Aeronautics Simulated Copycats|Aeronautics: Simulated Copycats]] `1.3.2`, and
  [[../01-Mods/Create TFMG Community Edition]] `1.2.4b-community` (source on GitHub, but that repo has no
  published Releases — actual distribution is CurseForge only).
- Added storage: [[../01-Mods/Tom's Simple Storage Mod|Tom's Simple Storage]] `2.4.2` with its Create
  integration addon [[../01-Mods/Create Contraption Terminals]] `1.4.0`, plus
  [[../01-Mods/Just Hammers]] `21.1.4`.
- Added the FTB team/claims/questing stack: [[../01-Mods/FTB Teams]] `2101.1.11`,
  [[../01-Mods/FTB Quests]] `2101.1.34`, [[../01-Mods/FTB Chunks]] `2101.1.21`, plus dependencies
  [[../01-Mods/FTB Library]] and [[../01-Mods/Architectury API]]. **Learned the hard way that none of the
  FTB family is on Modrinth** — `packwiz modrinth add ftb-teams`/`ftb-quests`/`ftb-chunks` each silently
  fuzzy-matched to the wrong unrelated addon (Better Party X FTB Teams, FTB Quests Optimizer, FTB Chunks:
  Sable Aerospace). Removed all three wrong entries and re-added correctly via
  `packwiz curseforge add <slug>-forge`. Documented this gotcha in [[../01-Mods/Mod List]] and
  [[../01-Mods/FTB Teams]] so it isn't repeated on a future version bump.
- Added a map stack that plays well with FTB Chunks: [[../01-Mods/Xaero's Minimap]] `26.4.2`,
  [[../01-Mods/Xaero's World Map]] `1.45.0`, and the bridge
  [[../01-Mods/FTB Chunks x Xaero's Compat]] `1.1.4` (renders FTB claims on Xaero's maps).
- New `#mod/category/teams` tag added to the taxonomy for the FTB stack.
- Added five more Create addons: [[../01-Mods/Create Aeronautics Toolgun|Create Aeronautics: Toolgun]]
  `0.3.6` (gravity gun/towing + blueprint tool), [[../01-Mods/Create Waystones Recipes]] `3.0.1.b` (pulled
  in the base [[../01-Mods/Waystones|Waystones]] mod as a dependency — raises an open fast-travel-vs-
  vehicles balance question), [[../01-Mods/Create Aeroworks|Create: Aeroworks]] `1.5.0` (gyroscope/joystick
  flight controls), [[../01-Mods/Create Bits n Bobs|Create: Bits 'n' Bobs]] `2.2.9` (pulled in
  [[../01-Mods/Strut Your Stuff (Struts)|Strut Your Stuff]] and [[../01-Mods/Azimuth API]] as dependencies),
  and [[../01-Mods/Create Connected]] `1.3.3-mc1.21.1`.
- Added [[../01-Mods/Just Enough Items (JEI)|Just Enough Items (JEI)]] `19.51.0.417` — recipe viewer,
  overdue given the pack is now at 42 mods.
- Added seven more Create addons, all resolved exactly to the requested versions:
  [[../01-Mods/Create Deep Seas]] `2.2.4` (submarines — opens up underwater combat),
  [[../01-Mods/Create Misc and Things|Create: Misc and Things]] `4.1.1`,
  [[../01-Mods/Create New Furnitures|Create : New Furnitures]] `1.1.2` (CurseForge only),
  [[../01-Mods/Create Teleporters]] `2.0.2b` (a third fast-travel system alongside Waystones — same open
  balance question, now three-way), [[../01-Mods/Create Aeronautics Kinetic Grip|Create Aeronautics:
  Kinetic Grip]] `1.0.5` (CurseForge only), [[../01-Mods/Create Aeronautics Throwable Rope Connector|Create
  Aeronautics: Throwable Rope Connector]] `0.4.3`, and [[../01-Mods/CreateBetterFps]] `1.1.4`. Pack is now
  at 49 mods.
- Did a dedicated research pass on optimization mods and added the full stack early, per project owner's
  request, rather than waiting until performance problems show up: [[../01-Mods/Sodium]],
  [[../01-Mods/Iris Shaders|Iris]], [[../01-Mods/Iris and Oculus Flywheel Compat|Iris & Oculus Flywheel
  Compat]], [[../01-Mods/ModernFix]], [[../01-Mods/FerriteCore]], [[../01-Mods/Entity Culling]],
  [[../01-Mods/ImmediatelyFast]], [[../01-Mods/Concurrent Chunk Management Engine|C2ME (NeoForge, alpha)]],
  [[../01-Mods/Alternate Current]], [[../01-Mods/BadOptimizations]], [[../01-Mods/FastFurnace]], and
  [[../01-Mods/FastWorkbench]] (with [[../01-Mods/Placebo]] as a dependency).
  **Correction made mid-batch:** initially added [[../01-Mods/Embeddium|Embeddium]] (the traditional
  "Sodium for Forge/NeoForge" fork) before discovering Sodium itself now ships native NeoForge builds and
  that Iris depends on Sodium directly — running both would mean two forks of the same rendering engine
  active at once. Removed Embeddium, documented the discovery in [[../01-Mods/Sodium]]'s note so it isn't
  repeated on a future update. Also caught that "Oculus" (the old Forge-era Iris fork) never got a 1.21.1
  build, so used Iris itself as the shader loader instead. New `#mod/category/optimization` tag added to
  the taxonomy. Pack is now at 61 mods.

- **First real test of the pack.** No GUI/Microsoft-login client test was possible in this dev environment,
  so instead ran the most rigorous automated check available: installed a NeoForge 1.21.1 server into a
  scratch instance outside the repo, used the real `packwiz-installer` (via `packwiz-installer-bootstrap`,
  fetched from its GitHub Releases) to resolve and download every mod for the server side, then booted a
  headless dedicated server and watched the log for crashes.
  - Hit CurseForge's "third-party download disabled" wall on [[../01-Mods/CBC Aeronautics Missiles]] — no
    automated tool (packwiz, Prism, curl) can fetch it, only a browser. Project owner manually downloaded
    it; since only `0.1.0` was on hand (not the `0.2.0` originally pinned), re-pinned the pack to that exact
    file via `packwiz curseforge add --file-id 8658979`. Discovered `0.1.0` doesn't declare
    [[../01-Mods/Create Radars|Create: Radars]]/[[../01-Mods/Sable|Sable]] as dependencies the way `0.2.0`
    does — the radar-targeting integration may not be present at this version.
  - That re-pin cascaded a second problem: packwiz re-resolved [[../01-Mods/Create Aeronautics]] (a shared
    dependency) through CurseForge metadata instead of its previous working Modrinth source, and *that*
    CurseForge copy is also distribution-disabled. Fixed by re-adding it via
    `packwiz modrinth add create-aeronautics` to force it back to a direct-download source. **Lesson
    recorded in the vault:** any `packwiz curseforge add` can silently flip an existing shared dependency's
    source — worth checking `git diff` on other `.pw.toml` files after any curseforge add, not just the one
    just added.
  - The dedicated server then crashed with `ModLoadingException` for two missing runtime dependencies
    neither Modrinth nor CurseForge had declared: [[../01-Mods/Waystones|Waystones]]/
    [[../01-Mods/Create Waystones Recipes]] need [[../01-Mods/Balm|Balm]], and
    [[../01-Mods/Aeronautics Simulated Copycats|Aeronautics: Simulated Copycats]] needs
    [[../01-Mods/Create Copycats Plus|Create: Copycats+]] (referenced in research long ago but never
    actually installed). Added both via packwiz.
  - **Second boot succeeded: `Done (6.503s)!`** — all 63 server-side mods loaded, world generated across
    overworld/nether/end/the custom teleporter pocket dimension, and the server idled without error for the
    rest of the test. Filed [[../02-Bugs/Cross-mod compat noise on server boot]] for a handful of non-fatal
    recipe/loot-table errors from Create: Connected, Create: Misc and Things, and TFMG Community Edition's
    optional cross-mod compat content — cosmetic, not blocking.
  - Not yet tested: the client side (rendering mods, GUI, actual play) — needs a real Prism Launcher launch
    with Microsoft login, which this environment can't do. Server-side testing is a strong signal but not a
    substitute for an actual playtest.

- **First real client test — success.** Project owner created a Prism Launcher instance matching the pack
  exactly (Minecraft 1.21.1, NeoForge 21.1.249), then the same `packwiz-installer` process used for the
  server smoke test was pointed at that instance's real `minecraft/` folder instead of the scratch
  directory, this time without `--side server` so client-only mods (Sodium, Iris, ImmediatelyFast,
  CreateBetterFps, BadOptimizations, Entity Culling — everything correctly excluded from the server test)
  were included too.
  - Hit the [[../01-Mods/CBC Aeronautics Missiles]] manual-download wall again as expected, but this time
    the project owner had the `0.2.0` file (not `0.1.0`) — re-pinned the pack back to `0.2.0` via
    `packwiz curseforge add --file-id 8746555`, which restores the [[../01-Mods/Create Radars|Create:
    Radars]]/[[../01-Mods/Sable|Sable]] integration that was uncertain at `0.1.0`. The same
    Create-Aeronautics-gets-flipped-to-blocked-CurseForge side effect happened a third time and was fixed
    the same way (`packwiz modrinth add create-aeronautics`) — this is now a confirmed recurring pattern,
    documented directly in [[../01-Mods/CBC Aeronautics Missiles]]'s note as something to redo after any
    future re-pin of that mod.
  - All mods installed cleanly into the real instance. **Project owner launched it and confirmed: "all
    looks good."** This is the first full end-to-end validation of the pack — client rendering stack
    (Sodium/Iris/Flywheel compat), all 61+ gameplay mods, and the manual-download mod all working together
    in an actual running game, not just a headless server.

## Unreleased — 2026-11-20: "more content" pass (warfare + PvE)
- Project owner set direction: **PvP and PvE weighted equally**, and **trains are in scope** as armored rail
  warfare (resolves the long-open Steam 'n' Rails question).
- Researched candidates on Modrinth's API filtered to 1.21.1 + NeoForge, then added (all via
  `packwiz modrinth add`, all `#mod/status/testing`):
  - Infantry: [[../01-Mods/Create Gunsmithing|Create: Gunsmithing]] `1.4.9` (+ [[../01-Mods/NTGL NukaTeam's Gun Lib|NTGL]] `3.2.0`).
  - Vehicle armor: [[../01-Mods/Rolled Homongenous Forked|Rolled Homongenous: Forked]] `1.0.3b`,
    [[../01-Mods/Create Armored Constructs|Create: Armored Constructs]] `1.0.0`,
    [[../01-Mods/Create Bits n Tracks CE|Create: Bits 'n' Tracks CE]] `3.0.3` (tank treads).
  - Munitions: [[../01-Mods/CBC Military Supplement]] `3.0.7-1.21.1` (+ [[../01-Mods/Shaolib]],
    [[../01-Mods/Shaolib Munitions]] `0.1.0`), [[../01-Mods/CBC Firepower Components]] `0.4.4`,
    [[../01-Mods/Create The Air War|Create: The Air War]] `5.00`.
  - Fire control: [[../01-Mods/CBC Ballistic Computer]] `1.3.5.10`,
    [[../01-Mods/Create Radar Fire Arc Filter|Create Radar: Fire Arc Filter]] `1.0.0`.
  - Trains: [[../01-Mods/Steam 'n' Rails]] `0.3.0-beta.2`, [[../01-Mods/CBC Locometal Armor]] `2.0.0`,
    [[../01-Mods/Create Who Touched My Train|Create: Who Touched My Train]] `1.4.0-Create6.0-beta`.
  - PvE: [[../01-Mods/Trigger Mobs]] `1.5.6`, [[../01-Mods/Improved Mobs]] `1.16.1` (+ [[../01-Mods/TenshiLib]]),
    [[../01-Mods/Enhanced AI]] `4.3.2.0-beta` (+ [[../01-Mods/InsaneLib]]).
- **Dependency re-resolution side effects (caught via `git diff`, per the lesson from the first test):**
  - Create: Radars was silently upgraded `0.4.9.4` -> `5.1.1` when adding Fire Arc Filter. Reverted to the
    tested `0.4.9.4` — 5.x is a new major line and Fire Arc / CBC Aeronautics Missiles predate it.
  - Ritchie's Projectile Library got added a second time as `rpl.pw.toml`. Duplicate removed.
  - Create Big Cannons switched CurseForge -> Modrinth source, same version. Kept.
- Pack now at 85 mods. **Not yet boot-tested** — the headless server test was blocked in this session
  (auto-mode permission on running the downloaded installer); needs to be run before any of the above
  flip to `active`.
- **Storage pass (same day):** project owner chose to stay on the Sophisticated family + Tom's rather than
  adding AE2/Refined Storage/Storage Drawers. Added vehicle-cargo storage only:
  [[../01-Mods/Sophisticated Storage Create Integration]] `0.1.23.246`,
  [[../01-Mods/Create Compatible Storage|Create: Compatible Storage]] `2.14.0`, and
  [[../01-Mods/Create Aeronautics Automated Logistics|Create Aeronautics: Automated Logistics]] `0.7.0`.
  No dependency side effects this time (`git diff` clean on existing files). Pack now at 88 mods, still
  awaiting a boot test.
- **Full mod update pass (same day):** `packwiz update --all` found 36 newer versions. Applied 35; reverted
  Create: Radars `5.1.1` back to `0.4.9.4` again (same reason as above). Notable:
  - Major bumps: [[../01-Mods/Create Deep Seas]] `2.2.4` -> `3.4.8` (pressure/hull mechanics rework),
    [[../01-Mods/Create Teleporters]] `2.0.2b` -> `3.0.2` (portals now move trains and Sable ships).
  - [[../01-Mods/Sophisticated Storage]] `1.5.91` -> `1.6.20`, Core `1.4.90` -> `1.5.39`, Backpacks
    `3.25.78` -> `3.26.22` — also brings them in line with the newer Create-integration addon.
  - [[../01-Mods/Create TFMG Community Edition]] `1.2.4b` -> `1.3.3a`, [[../01-Mods/Create Aeronautics]]
    `1.3.2` -> `1.3.3`, [[../01-Mods/Sable]] `2.0.5` -> `2.0.6`, plus FTB family, Xaero's, JEI, KubeJS, and
    optimization-mod patch bumps.
  - **New hidden dependency:** JEI `19.71` requires [[../01-Mods/MezzConfig]], which `packwiz update` did
    not add. Caught by cross-checking every pinned Modrinth version's declared deps against the pack.
    Lesson: `update` never adds new deps — always run that check after a bulk update.
  - No Modrinth/CurseForge source flips. CurseForge-sourced mods (FTB family, TFMG, Radars, RPL, CBC
    Aeronautics Missiles, etc.) can't be dependency-checked the same way without a CurseForge API key —
    the boot test is the only check for those.
  - Pack now at 89 mods. Still awaiting the boot test.
- **Client boot test (2026-11-21):** synced the Prism instance with `packwiz-installer` (client side, all
  files downloaded, including CBC Aeronautics Missiles with no manual-download wall this time) and launched it.
  - First launch failed during mod loading: [[../01-Mods/NTGL NukaTeam's Gun Lib|NTGL]] requires
    [[../01-Mods/GeckoLib]] `>=4.8.2`, which wasn't in the pack. Added via `packwiz modrinth add geckolib`
    (`4.9.3`). Neither packwiz nor the Modrinth dependency cross-check had flagged it.
  - Second launch reached the title screen with no crash. Remaining log errors are non-fatal: MezzConfig
    complaining about old JEI config keys, a missing irisflw access-transformer file, Xaero's version-check
    timeout, and model JSON errors logged in [[../02-Bugs/Client model load errors]].
  - Not yet tested: creating/loading a world with the 26 mods added since the last test. Pack now at 90 mods.
- **Diamond recipe + blaze burner fuel tiers (2026-11-21):** added [[../03-Design/Diamond Recipe]]
  (superheated compacting, 9 coal blocks → 1 diamond) and [[../03-Design/Blaze Burner Fuel Tiers]]
  (Blaze Cake → Biofuel → Napalm, each needing the previous tier's superheat to produce). These are the
  pack's first KubeJS scripts. Found that TFMG's napalm burner fuel was dead data without Create: Liquid Fuel.
  Not yet tested in game.
- **Added [[../01-Mods/Create Enchantment Industry|Create: Enchantment Industry]] `2.5.4b` (2026-11-21)**
  plus its dependency [[../01-Mods/Create Dragons Plus|Create: Dragons Plus]] `1.11.9`. Checked dependencies
  against both the Modrinth metadata and the jar's `neoforge.mods.toml`: all met, nothing hidden. Pack now
  at 92 mods. Not yet boot-tested.
- **Removed Create: The Air War launchers + ammo (2026-11-21):** see the Config decisions in
  [[../01-Mods/Create The Air War]]. KubeJS recipe removal + JEI hiding; the mod itself stays.
- **Explosion crash fix (2026-11-21):** Tomahawk missiles crashed the server on impact. Root cause:
  [[../01-Mods/Shaolib]] 0.1.0 always calls into [[../01-Mods/Synaxis]] from its explosion hook but
  never declares or checks it (see [[../02-Bugs/Explosions crash - Shaolib missing Synaxis]]). Added
  Synaxis `1.6.3` + [[../01-Mods/LDLib2]] `2.2.46.a` + [[../01-Mods/Sable Photomancy]] `1.0.1`. Neither
  Synaxis's Modrinth metadata nor packwiz listed its dependencies; they came from reading the jar's
  `neoforge.mods.toml`. Another `packwiz curseforge add` slip (LDLib) was switched back to Modrinth, and no
  other sources flipped. Client boot + world load with 93 mods (incl. Enchantment Industry): clean.
- **Elytras removed (2026-11-21):** see [[../03-Design/Elytra Removal]]. End ship item frames are emptied,
  gliding is blocked, and the item is hidden from JEI.
- **NeoForge 21.1.249 → 21.1.267 + custom [[../01-Mods/Loot Edit]] mod (2026-11-21):** the project
  owner's Loot Edit jar requires NeoForge >=21.1.267, so the pack was bumped via `packwiz migrate loader
  latest` (21.1.267 was also the newest 21.1 on maven.neoforged.net). Safety steps: world + `mmc-pack.json`
  + `pack.toml` backed up to the Prism instance's `backups/before-neoforge-bump-20261121-0339/`. Scanned
  all 93 mod jars for NeoForge upper bounds; none exclude 267. Prism instance `mmc-pack.json` updated to
  match. Boot + world load: clean; KubeJS 4/4 scripts OK; Loot Edit exported 4,969 tables.
  - The 309 `Couldn't parse element` loot-table errors at load are **not** from the bump; they're
    identical on 249. They come from Steam 'n' Rails track loot tables for mods that aren't installed
    (e.g. `railways:blocks/track_tfc_acacia`).
  - **Rollback:** set `neoforge = "21.1.249"` in `pack/pack.toml`, restore the backed-up `mmc-pack.json`,
    and remove Loot Edit (it won't load on 249).

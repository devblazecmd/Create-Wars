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

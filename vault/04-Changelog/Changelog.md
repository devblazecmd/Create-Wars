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

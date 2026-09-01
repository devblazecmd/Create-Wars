# Create Wars

A Minecraft modpack built on [Create](https://modrinth.com/mod/create): machines, guns, radar, and drones,
for fighting mobs or each other. Targets **Minecraft 1.21.1, NeoForge**.

## Repo layout

- **`vault/`** — Obsidian vault. Design docs, the mod list, and the bug tracker. This is the source of
  truth for *why* things are the way they are — git history explains *what* changed, the vault explains
  *why* and *what to check* when a Minecraft version bump breaks something.
  - `00-Meta/Tag Taxonomy.md` — the tagging scheme everything else follows
  - `01-Mods/Mod List.md` — every mod under consideration or in use, one note each
  - `02-Bugs/Bug Tracker.md` — bug notes, tagged by severity/type/version
  - `03-Design/` — game design docs (weapon balance, factions, progression)
  - `04-Changelog/` — human-readable pack history
  - `Templates/` — note templates; use these when adding new mod/bug/design notes
- **`pack/`** — the actual [packwiz](https://packwiz.infra.link/)-managed pack (`pack.toml`, `index.toml`,
  per-mod `.toml` files, configs, KubeJS scripts). See [pack/README.md](pack/README.md) for setup and the
  add/update workflow.

## Status

Scaffolding only — no mods installed yet. `pack/pack.toml` has a placeholder NeoForge version; see
[pack/README.md](pack/README.md) for the first-time-setup steps (needs Java + the packwiz CLI, neither of
which are in this dev environment).

Mod scope decided so far, from initial research (all candidates, none pinned yet — see
[vault/01-Mods/Mod List.md](vault/01-Mods/Mod%20List.md)):
- **Core:** Create, Flywheel
- **Combat:** Create: Big Cannons
- **Vehicles:** Create Aeronautics (+ Sable), Create Crafts & Additions
- **Drones:** Create: Droneworks Simulated
- **Radar:** Mob Radar
- **Scripting:** KubeJS

Open questions are tracked at the bottom of the mod list note — notably whether to add trains
(Steam 'n' Rails) or ship physics (an *unofficial* Valkyrien Skies NeoForge port) and whether vanilla mobs
need rebalancing to be a credible "war" opponent.

Whether the pack stays curated-mods-only or grows a custom mod (e.g. bespoke radar/drone mechanics no
existing addon covers) is intentionally undecided — revisit once we hit something existing mods can't do.

## Workflow at a glance

1. Research a mod → write a `#mod/status/candidate` note in `vault/01-Mods/` from the template.
2. Decide to include it → `packwiz mr add`/`packwiz cf add` in `pack/` → flip the note to
   `#mod/status/active`, fill in the pinned version.
3. Something breaks (especially after a MC/mod version bump) → file a bug note in `vault/02-Bugs/` from the
   template, tag it, link it to the mod note(s) involved.
4. Notable pack-wide decisions → append to `vault/04-Changelog/Changelog.md`.

# pack/

This folder is a [packwiz](https://packwiz.infra.link/) pack: `pack.toml`, `index.toml`, and one `.toml`
file per mod under `mods/`. Everything here is plain text on purpose — diffs stay readable and mod
add/remove/update shows up as a normal git change instead of a binary blob.

**`pack.toml` currently has a placeholder `neoforge = "TODO"` version.** Nobody has run packwiz against
this repo yet (no Java/packwiz installed in the environment that scaffolded it). First real setup step:

## First-time setup (do this once)

1. Install Java 21 (NeoForge 1.21.1 requires it) and the [packwiz CLI](https://github.com/packwiz/packwiz).
2. From this `pack/` folder, run `packwiz init` — pick Minecraft 1.21.1 and NeoForge, let it fill in the
   real NeoForge loader version and generate `index.toml`. It's fine that `pack.toml` already exists;
   packwiz will ask before overwriting, confirm the version fields match what's above.
3. Add mods with `packwiz mr add <slug>` (Modrinth) or `packwiz cf add <slug>` (CurseForge) — see
   [[../vault/01-Mods/Mod List]] in the Obsidian vault for the researched candidate list and their
   confirmed slugs/versions.
4. After adding a mod, flip its vault note's tag from `#mod/status/candidate` to `#mod/status/active` and
   fill in `pack_version_pinned` / `last_verified` with the actual pinned version.
5. Export a playable instance with `packwiz-installer` or point [Prism Launcher](https://prismlauncher.org/)
   at this pack's `pack.toml` URL/path directly (Prism has native packwiz support).

## Ongoing workflow

- **Adding a mod:** `packwiz mr add`/`packwiz cf add` → create/update its vault note → commit both together.
- **Updating a mod:** `packwiz update <mod>` (or `packwiz update --all`) → update `last_verified` and
  `pack_version_pinned` in its vault note → commit together.
- **Bumping Minecraft version:** this is the moment the vault pays for itself. Before bumping, sweep
  `01-Mods/` for every mod tagged with the *old* `#mc-version/...` tag and check upstream for a matching
  new-version release before touching `pack.toml`. Add the new `#mc-version/...` tag alongside (don't
  replace) the old one on each note as you confirm it.
- **Something breaks after an update:** file it as a [[../vault/02-Bugs/Bug Tracker|bug note]] using the
  template, tag the mod(s) involved, and link back and forth between the bug note and the mod note.

## KubeJS scripts

`kubejs/server_scripts/` and `kubejs/client_scripts/` hold pack-specific balance/behavior scripts (damage
tuning, custom recipes, cross-mod glue). Document non-obvious scripts in a vault note under `03-Design/` —
the *why* behind a balance number belongs there, not just in a code comment.

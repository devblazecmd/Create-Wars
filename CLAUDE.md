# Create Wars — CLAUDE.md

Modpack project: Create-based Minecraft modpack targeting **1.21.1 / NeoForge**, adding combat/vehicle/
drone/radar content on top of Create for PvP and mob-fighting gameplay.

## Repo layout
- `vault/` — Obsidian vault, the project's source of truth for *why* (design decisions, mod research, bug
  history). Read `vault/00-Meta/Tag Taxonomy.md` before adding or editing notes.
- `pack/` — packwiz-managed pack (`pack.toml`, `index.toml`, `mods/*.toml`, `config/`, `kubejs/`). See
  `pack/README.md` for the add/update workflow. **`neoforge` in `pack/pack.toml` is still a `"TODO"`
  placeholder** — no one has run `packwiz init` in this repo yet (needs Java + packwiz CLI, not present in
  the environment this was scaffolded in).

## Working conventions
- Every mod gets a note in `vault/01-Mods/` before or immediately after being added to `pack/` — don't add
  a mod to `pack.toml`/`index.toml` without a corresponding note. Use `vault/Templates/Mod Note Template.md`.
- Mod status tags (`#mod/status/candidate|active|testing|disabled|removed`) must reflect actual pack state.
  If you add a mod via packwiz, flip its note from `candidate` to `active`/`testing` in the same change.
- Never delete an old `#mc-version/x.y.z` tag when bumping Minecraft versions — add the new one alongside
  it. The whole point of the vault is answering "what needs checking when we bump versions," which requires
  keeping the history of what was verified against which version.
- Bugs found during testing go in `vault/02-Bugs/` as their own note (template: `Bug Report Template.md`),
  linked to the mod note(s) involved — don't just fix and forget, since modpacks re-break the same way
  across version bumps.
- Don't hand-guess mod version strings, NeoForge build numbers, or file hashes — these must come from
  actually running packwiz/checking Modrinth/CurseForge, not from memory or pattern-matching an old note.
  Mod notes written before install are explicitly marked "web research only, not yet installed" for this
  reason — verify before trusting a pinned version number in an old note.

## Known open decisions (don't resolve unilaterally — flag to the user)
- Curated-mods-only vs. also authoring custom Java/Kotlin mods: intentionally left open.
- Trains (Steam 'n' Rails) and ship physics (Valkyrien Skies, unofficial 1.21.1 NeoForge port only) are
  candidates, not committed — see the bottom of `vault/01-Mods/Mod List.md`.
- Mob-side balance (do vanilla mobs need reworking to be a credible "war" opponent) is undecided.

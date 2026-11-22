---
tags: [meta]
---

# Bug Tracker (MOC)

Index of open/notable bug notes. Use [[../Templates/Bug Report Template|Bug Report Template]] for each new
one — one note per bug, tagged by severity/type/mc-version, linked to the affected [[../01-Mods/Mod List|mod note(s)]].

First real test happened 2026-09-01: a headless NeoForge server boot with the full mod list (see
[[../04-Changelog/Changelog|changelog]]). Two hard crashes were found and fixed before this note was
written (missing [[../01-Mods/Balm|Balm]] and [[../01-Mods/Create Copycats Plus|Create: Copycats+]]
dependencies) — those aren't logged here since they were resolved immediately by adding the missing mods,
not by a code/config fix. What's below is what's left after that.

## Open
- [[Cross-mod compat noise on server boot]] — cosmetic, non-fatal recipe/loot-table errors from
  Create: Connected, Create: Misc and Things, and TFMG Community Edition's optional cross-mod compat
  content.
- [[Create Nuclear armor dye recipes fail to load]]: 64 recolor recipes have an empty smithing template.
  Cosmetic only.
- [[Client model load errors]] — empty/invalid model JSON in Create: Radars, Create: The Air War
  and Create: Misc and Things. Non-fatal, needs an in-game look.

## Investigating
*(none)*

## Fixed
- [[Quest items with no survival recipe]]: pack recipes for Armored Constructs, Military Supplement, Synaxis
  jet and Air War FPV drone items.
- [[Gunsmithing steel sheet needed hidden steel]]: steel sheets needed hidden Gunsmithing steel after unification.
- [[Explosions crash - Shaolib missing Synaxis]]: Tomahawk (and likely any explosion) crashed the
  server; fixed by adding Synaxis + deps.

## Won't fix
*(none)*

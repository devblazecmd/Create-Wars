---
tags: [mod/status/active, mod/category/vehicles, mc-version/1.21.1, loader/neoforge]
mod_id: copycats
pack_version_pinned: "copycats-3.0.11+mc.1.21.1-neoforge.jar (updated 2026-11-20 from copycats-3.0.8+mc.1.21.1-neoforge.jar)"
last_verified: "2026-11-20 (packwiz update --all; not yet boot-tested)"
---

# Create: Copycats+

**Source:** [Modrinth](https://modrinth.com/mod/copycats) — "all the copycats you've ever wanted," combined
into a single mod.

**Why this is here:** referenced early in this pack's research (see the "not yet researched" section
history in [[Mod List]]) as the base copycat system that [[Create Extra Copycats]] and
[[Aeronautics Simulated Copycats|Aeronautics: Simulated Copycats]] extend, but never actually installed —
it wasn't declared as a hard Modrinth dependency of either addon, so packwiz never auto-added it. Only
surfaced as a hard crash (`Mod sim_copycats requires copycats any`) during a headless server boot test. See
the 2026-09-01 changelog entry for the full writeup.

**Known minor issue found during the same test:** [[Sable]] logs `Failed to apply tag physics properties.
Unknown block: copycats:copycat_catwalk` on every dimension load, even with this mod installed — non-fatal
(Sable just skips that one block's custom physics properties), but worth a closer look; possibly a version
mismatch between this mod's block set and what Sable's tags expect.

## Role in Create Wars
Base copycat-block system for [[Create]]. [[Create Extra Copycats]] adds a couple more block types on top
of it; [[Aeronautics Simulated Copycats|Aeronautics: Simulated Copycats]] requires it directly for
Aeronautics-specific physical-property copycats.

## Dependencies
- Required by: [[Aeronautics Simulated Copycats|Aeronautics: Simulated Copycats]]
- Extended by: [[Create Extra Copycats]] (not a hard dependency per packwiz, but functionally related)

## Version notes
Added via `packwiz modrinth add copycats` on 2026-09-01; resolved to `3.0.8+mc.1.21.1-neoforge`.

## Known issues
See the Sable `copycat_catwalk` tag warning noted above — not yet filed as a formal bug note since it
didn't crash anything, but worth watching.

## Config decisions
None yet.

## Update history
- 2026-11-20: `copycats-3.0.8+mc.1.21.1-neoforge.jar` -> `copycats-3.0.11+mc.1.21.1-neoforge.jar` via `packwiz update --all`.

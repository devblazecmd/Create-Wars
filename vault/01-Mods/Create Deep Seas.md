---
tags: [mod/status/active, mod/category/vehicles, mc-version/1.21.1, loader/neoforge]
mod_id: create-deep-seas
pack_version_pinned: "create_submarine-3.4.8.jar (updated 2026-11-20 from create_submarine-2.2.4.jar)"
last_verified: "2026-11-20 (packwiz update --all; not yet boot-tested)"
---

# Create Deep Seas

**Source:** [Modrinth](https://modrinth.com/mod/create-deep-seas) — "Submarine in Create Aeronautics!"

## Role in Create Wars
Adds submarines to [[Create Aeronautics]]. This is the naval counterpart to Aeronautics' air vehicles —
extends the vehicle-warfare scope from air/land into underwater. Combined with [[CBC Aeronautics Missiles]]
and [[Create Radars|Create: Radars]], this opens up submarine combat as a distinct theater.

**Content note:** Modrinth flags an `epilepsy_triggers` disclosure on this project — worth being aware of
for any streaming/accessibility considerations, not a functional issue.

## Dependencies
- No new dependencies at add time (packwiz found [[Create Aeronautics]] already present).

## Version notes
Added via `packwiz modrinth add create-deep-seas` on 2026-09-01; resolved to `2.2.4`, matching the
requested version exactly.

## Known issues
There's a known third-party bug fix mod, "Create: Deep Seas - Lava Fix" (players inside a sealed submarine
still take fire/lava damage while submerged in lava despite the interior being emptied) — not installed,
but worth adding if that bug is encountered in testing.

## Config decisions
None yet.

## Update history
- 2026-11-20: `create_submarine-2.2.4.jar` -> `create_submarine-3.4.8.jar` via `packwiz update --all`.
- **Major version jump (2.x -> 3.x).** 3.x adds hull pressure models, girder beams, pressure goggles, an
  optional progressive-flooding mode (off by default), and a "Vortex Engine" coloured-light renderer that
  auto-disables under Iris shaders. 3.4.0 was labelled ALPHA in its changelog. Untested in this pack —
  if submarines misbehave, rolling back to `2.2.4` is the first step.

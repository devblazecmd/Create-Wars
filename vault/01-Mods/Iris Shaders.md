---
tags: [mod/status/active, mod/category/optimization, mc-version/1.21.1, loader/neoforge]
mod_id: iris
pack_version_pinned: "1.8.14-beta.1+mc1.21.1 (iris-neoforge-1.8.14-beta.1+mc1.21.1.jar)"
last_verified: "2026-09-01 (added via packwiz modrinth add)"
---

# Iris Shaders

**Source:** [Modrinth](https://modrinth.com/mod/iris) · coderbot — "A modern shader pack loader for
Minecraft intended to be compatible with existing OptiFine shader packs"

**Naming note:** the pack was originally going to use "Oculus" (the historical Forge-ecosystem Iris fork),
but Oculus's own Modrinth listing tops out at Minecraft 1.20.1 — it was never ported to 1.21.1/NeoForge.
Iris itself picked up native NeoForge support instead, making it the correct pick here. Don't reach for
Oculus on a future version bump without re-checking whether it's caught back up.

## Role in Create Wars
Shader pack loader. [[CreateBetterFps]] was added earlier specifically because it improves Create's FPS
"when shaderpack is on" — implying shader support was already an intended part of this pack's visual
target. [[Iris & Oculus Flywheel Compat]] bridges this with Create's [[Flywheel]] rendering so shaders
don't tank contraption performance.

## Dependencies
- Hard requires: [[Sodium]] (confirmed via Iris's own Modrinth dependency list)

## Version notes
Added via `packwiz modrinth add iris` on 2026-09-01; resolved to `1.8.14-beta.1+mc1.21.1` — note this is a
**beta** build, the only kind currently available for 1.21.1. Watch for a stable release on a future update
pass.

## Known issues
None logged yet — untested in-game. Beta-status build is itself worth treating as a known-risk item until
verified stable in this pack specifically.

## Config decisions
None yet.

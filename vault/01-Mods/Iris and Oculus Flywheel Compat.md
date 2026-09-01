---
tags: [mod/status/active, mod/category/optimization, mc-version/1.21.1, loader/neoforge]
mod_id: iris-flw-compat
pack_version_pinned: "NeoForge-2.4.0 (iris-flywheel-compat-NeoForge-2.4.0.jar)"
last_verified: "2026-09-01 (added via packwiz modrinth add)"
---

# Iris & Oculus Flywheel Compat

**Source:** [Modrinth](https://modrinth.com/mod/iris-flw-compat)

## Role in Create Wars
Forces [[Flywheel]] (Create's rendering engine) to keep its optimizations enabled even when a shaderpack is
active via [[Iris Shaders|Iris]] — normally Flywheel disables those optimizations under shaders. Directly
relevant given [[CreateBetterFps]] and [[Iris Shaders|Iris]] are both already in the pack; this is the glue
that makes shaders + heavy Create contraptions coexist without a big FPS cliff. Its own compatibility table
lists Create `6.0.9` pairing with NeoForge/Forge build `2.1.0` — this pack's Create is `6.0.10`, close
enough that packwiz's dependency resolution accepted it without complaint, but worth re-checking if
anything renders oddly under shaders.

## Dependencies
- Hard requires: [[Sodium]] (auto-resolved and added by packwiz)
- Functionally requires [[Iris Shaders|Iris]] and [[Create]]/[[Flywheel]], though not declared as a hard
  Modrinth dependency.

## Version notes
Added via `packwiz modrinth add iris-flw-compat` on 2026-09-01; resolved to `NeoForge-2.4.0`. Modrinth
flagged a version-number/release-date inconsistency for this project (latest number `2.2.0` vs. newest by
date `1.21.1+2.4.0-release`) — same pattern seen before with [[Rhino]] and [[Create Teleporters]]; the
newest-by-date build is what got pinned.

## Known issues
None logged yet — untested in-game.

## Config decisions
None yet.

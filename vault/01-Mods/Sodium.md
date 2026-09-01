---
tags: [mod/status/active, mod/category/optimization, mc-version/1.21.1, loader/neoforge]
mod_id: sodium
pack_version_pinned: "0.8.13+mc1.21.1 (sodium-neoforge-0.8.13+mc1.21.1.jar)"
last_verified: "2026-09-01 (auto-added as a dependency of Iris & Oculus Flywheel Compat via packwiz)"
---

# Sodium

**Source:** [Modrinth](https://modrinth.com/mod/sodium) · CaffeineMC/team 4reLOAKe

**Important, non-obvious fact learned during install:** Sodium historically was Fabric-only, which is why
the community fork [[Embeddium]] existed for Forge/NeoForge users. **As of sometime in 2026, Sodium ships
official native NeoForge builds** (confirmed via its Modrinth loaders list: `fabric`, `neoforge`, `quilt`).
[[Iris Shaders|Iris]] itself now depends directly on Sodium (not Embeddium) for NeoForge. Because of this,
Embeddium was added by mistake alongside Sodium in the same session, then removed — running both would mean
two forks of the same rendering-engine codebase hooking the same internals, a near-certain conflict. If a
future version bump ever needs a rendering-optimization mod again, check whether Sodium's own NeoForge
support has regressed before reaching for Embeddium as a fallback.

## Role in Create Wars
High-performance rendering engine — the actual base optimization layer this pack's whole graphics stack
sits on: [[Iris Shaders|Iris]] (shaders) and [[Iris & Oculus Flywheel Compat]] (keeps
[[Flywheel]]/Create's rendering optimizations on even with shaders active) both build on top of this.

## Dependencies
- Required by: [[Iris Shaders|Iris]], [[Iris & Oculus Flywheel Compat]]

## Version notes
Auto-resolved and added by `packwiz modrinth add iris-flw-compat` on 2026-09-01; pinned at
`0.8.13+mc1.21.1`.

## Known issues
None logged yet — this whole optimization stack (Sodium/Iris/Flywheel-compat/ModernFix/etc.) hasn't been
tested in-game together yet. Given the sheer mod count (61+), a first launch should be watched closely for
mixin conflicts.

## Config decisions
None yet.

---
tags: [mod/status/removed, mod/category/optimization, mc-version/1.21.1, loader/neoforge]
mod_id: embeddium
pack_version_pinned: "n/a — removed"
last_verified: "2026-09-01 (added then removed the same session, via packwiz)"
---

# Embeddium

**Status: rejected 2026-09-01.** Added first (as the historically-correct "Sodium for Forge/NeoForge"
fork), then removed once it became clear [[Sodium]] itself now has official native NeoForge builds and
that [[Iris Shaders|Iris]] depends directly on Sodium, not this. Keeping both installed would run two forks
of the same rendering-engine codebase simultaneously — a near-certain source of mixin conflicts. Kept as a
note for history per the taxonomy's `#mod/status/removed` convention.

**Source:** [Modrinth](https://modrinth.com/mod/embeddium) — "A powerful, mod-friendly, FOSS client
performance mod for NeoForge," forked from the last FOSS-licensed Sodium codebase.

## Role in Create Wars
None — superseded by [[Sodium]] for this pack. Don't re-add unless [[Sodium]]'s NeoForge support is
confirmed broken/regressed in a future Minecraft version and Embeddium is the only working alternative at
that time.

## Dependencies
n/a

## Known issues
n/a — not installed.

## Config decisions
n/a

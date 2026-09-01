---
tags: [mod/status/removed, mod/category/dependency, mc-version/1.21.1, loader/neoforge]
mod_id: flywheel
pack_version_pinned: "n/a — bundled inside Create's jar"
last_verified: "2026-09-01 (confirmed via packwiz + Modrinth API during install)"
---

# Flywheel

**Status: not a separate install.** `packwiz modrinth add flywheel` failed ("no valid versions found") because
the standalone Modrinth listing (slug `flywheel`, now titled "Flywheel (Legacy)") only ships versions for
MC 1.18.2/1.19.2. Its own description confirms why: *"Flywheel is now intended to be bundled within the
mods that need it. You do not need to download Flywheel directly for versions >= 0.6.9."* Confirmed via
`GET /v2/project/LNytGWDc/dependencies` on the Modrinth API — Create's own dependency list still points at
the legacy standalone project, which is stale metadata, not a real runtime requirement for current Create.

**Source:** [Flywheel (Legacy) on Modrinth](https://modrinth.com/mod/flywheel) — historical only

## Role in Create Wars
Rendering engine Create uses internally for contraption/kinetic block rendering. As of the versions we're
targeting, it ships jar-in-jar inside [[Create]]'s own mod file — nothing to add to `pack/mods/` for it.

## Dependencies
n/a — not installed separately.

## Known issues
None — not applicable.

## Config decisions
None.

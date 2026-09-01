---
tags: [mod/status/active, mod/category/optimization, mc-version/1.21.1, loader/neoforge]
mod_id: c2me-neoforge
pack_version_pinned: "mc1.21.1-0.4.0-alpha.0.120 (c2me-neoforge-mc1.21.1-0.4.0-alpha.0.120.jar)"
last_verified: "2026-09-01 (added via packwiz modrinth add)"
---

# Concurrent Chunk Management Engine (NeoForge)

**Source:** [Modrinth](https://modrinth.com/mod/c2me-neoforge)

## Role in Create Wars
Multithreads chunk generation, I/O, and loading, without changing vanilla worldgen behavior by default.
Relevant for a pack with claimed territory ([[FTB Chunks]]) and large-scale vehicle travel
([[Create Aeronautics]], [[Create Deep Seas]]) that will push players/servers to load chunks across a wide
map quickly.

**Alpha-status note:** this is explicitly a devbuild/alpha release (`0.4.0-alpha.0.120`) — the NeoForge port
of C2ME hasn't reached a stable release yet as of this pinning. Treat as higher-risk than the rest of the
optimization stack; watch closely for world-corruption or crash reports in testing before trusting it on a
long-running world.

## Dependencies
- None required by packwiz at add time (standalone).

## Version notes
Added via `packwiz modrinth add c2me-neoforge` on 2026-09-01; resolved to `mc1.21.1-0.4.0-alpha.0.120`.

## Known issues
None logged yet — flagged above as alpha-status and worth extra caution.

## Config decisions
None yet.

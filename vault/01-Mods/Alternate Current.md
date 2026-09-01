---
tags: [mod/status/active, mod/category/optimization, mc-version/1.21.1, loader/neoforge]
mod_id: alternate-current
pack_version_pinned: "mc1.21-1.9.0 (alternate_current-mc1.21-1.9.0.jar)"
last_verified: "2026-09-01 (added via packwiz modrinth add)"
---

# Alternate Current

**Source:** [Modrinth](https://modrinth.com/mod/alternate-current)

## Role in Create Wars
Rewrites vanilla redstone-dust update propagation into a deterministic single-pass queue instead of
cascading block updates — drastically reduces tick-time cost of large redstone builds. [[Create]] itself
uses kinetic power rather than redstone dust for most of its own mechanisms, so direct overlap should be
limited, but Create *does* have redstone-reading/emitting contact blocks and links
([[Create Ender Transmission]] etc.) that interact with vanilla redstone — worth watching for any
unexpected interaction during testing, though no specific incompatibility is known at install time.

## Dependencies
- None required by packwiz at add time (standalone).

## Version notes
Added via `packwiz modrinth add alternate-current` on 2026-09-01; resolved to `mc1.21-1.9.0`.

## Known issues
None logged yet — flagged above for the Create-redstone-interaction angle to watch during testing.

## Config decisions
None yet.

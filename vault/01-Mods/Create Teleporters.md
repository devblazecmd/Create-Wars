---
tags: [mod/status/active, mod/category/utility, mc-version/1.21.1, loader/neoforge]
mod_id: create-teleporters
pack_version_pinned: "createteleporters-3.0.2-1.21.1.jar (updated 2026-11-20 from createteleporters-remastered-2.0.2b-neoforge-1.21.1.jar)"
last_verified: "2026-11-20 (packwiz update --all; not yet boot-tested)"
---

# Create: Teleporters

**Source:** [Modrinth](https://modrinth.com/mod/create-teleporters) · author dcchill — "a complete rebuild
of the original Create Teleporters mod," redesigned to fit Create's aesthetics and fix old bugs.

**Naming note:** Modrinth's own listing shows a version-ordering inconsistency (latest version *number*
`2.4` vs. newest by release *date* `2.0.2b`) — same pattern seen with [[Rhino]] earlier in this pack. The
requested build was `2.0.2b`, which is what got pinned; if a future update grabs `2.4` unexpectedly, check
whether that's actually newer or an out-of-order release.

## Role in Create Wars
Point-to-point teleportation blocks built with Create mechanics. Overlaps functionally with
[[Waystones]]/[[Create Waystones Recipes]] — see the open fast-travel-vs-vehicles balance question already
flagged there; this adds a second teleportation system to weigh into that same decision.

## Dependencies
- None required by packwiz at add time (standalone addon on top of [[Create]]).

## Version notes
Added via `packwiz modrinth add create-teleporters` on 2026-09-01; resolved to `2.0.2b-neoforge-1.21.1`,
matching the requested version exactly.

## Known issues
None logged yet.

## Config decisions
None yet — fold into the fast-travel balance design doc alongside [[Waystones]] once that's written.

## Update history
- 2026-11-20: `createteleporters-remastered-2.0.2b-neoforge-1.21.1.jar` -> `createteleporters-3.0.2-1.21.1.jar` via `packwiz update --all`.
- **Major version jump (2.x -> 3.x).** 3.0 lets custom portals carry **trains** and **Sable ships**
  (Aeronautics vehicles); 3.0.1 requires tracks on both sides of a portal and removed passive portal
  drain. Balance implication for the open fast-travel question: warships/armored trains can now teleport
  into a fight, not just players.

---
tags: [mod/status/testing, mod/category/combat, mc-version/1.21.1, loader/neoforge]
mod_id: cbc-enchanced-shells-create-big-cannons
pack_version_pinned: "1.2.5 (CBCmoreshells-1.2.5.jar, CurseForge file 8838000) - PINNED, see Version notes"
last_verified: "2026-11-22 (client boot into world, clean load; nukes not fired yet)"
---

# CBC Enhanced Shells

**Source:** [CurseForge](https://www.curseforge.com/minecraft/mc-mods/cbc-enchanced-shells-create-big-cannons)
(CurseForge only; the slug really is spelled "enchanced"). Mod ID **`cbc_enhanced_shells`**. The jar is named
`CBCmoreshells-*.jar`, but this is **not** [[CBC Military Supplement]] (mod ID `cbcmoreshells`).

## Role in Create Wars
**Only here for the nukes** (owner 2026-11-22). The mod adds about 100 tiered (Mk.I to Mk.V) shells,
powder charges and (in 1.5.x) missiles. Those overlap [[CBC Military Supplement]] and
[[Create Warnautics]], so `pack/kubejs/server_scripts/nuclear_weapons.js` removes their recipes and hides
them. Four items stay:
- **Nuclear Shell** and **Nuclear Shell Mk.II**: mushroom-cloud detonation. The mod page says the blast is
  240+ blocks. Not measured here yet.
- **Mini H-Bomb Shell** (4 nuke shells) and **H-Bomb Shell** (3 Mk.II): thermonuclear dome and a ringed
  shockwave.

The nuke recipes are replaced with ones that need [[Create Nuclear]] uranium rods. See
[[../03-Design/Nuclear Weapons]].

## Dependencies
- Hard requires: [[Create]], [[Create Big Cannons]] (≥5.11.4), [[Ritchie's Projectile Library]]. All present.
- Optional: FTB Chunks (declared as an optional dependency in `neoforge.mods.toml`; what it does is
  unknown, maybe claim checks), Create Aeronautics, Sable.

## Version notes
- Added 2026-11-22. `packwiz curseforge add` first resolved **1.5.1**, and that **crashed on load**:
  [[CBC Firepower Components]] 0.4.4 declares an optional dependency on `cbc_enhanced_shells`
  **`[1.2.2,1.3.0)`**, and NeoForge enforces the range whenever both are installed.
- Switched to **1.2.5** (the newest file in range; it has all four nukes, checked in the jar) and
  **`packwiz pin`**ned it. Unpin only when Firepower Components widens its range.
- `packwiz curseforge add` also re-wrote `create.pw.toml` and `create-big-cannons.pw.toml` from Modrinth
  to CurseForge sources (same files). Reverted with `git checkout`. Watch for this on every CurseForge add
  that pulls dependencies.
- 1.2.5 has **no config file**, so blast size and terrain damage can't be tuned.

## Known issues
None in the boot log. Not playtested: blast radius, server lag, claim interaction.

## Config decisions
None (no config). Balance is by recipe cost; see the design note.

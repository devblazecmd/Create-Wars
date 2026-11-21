---
tags: [bug/status/open, bug/severity/low, bug/type/visual, mc-version/1.21.1, loader/neoforge]
affected_mods: ["[[Create Radars]]", "[[Create The Air War]]", "[[Create Misc and Things]]"]
date_opened: "2026-11-21"
date_resolved: ""
---

# Client model load errors

## Symptom
Non-fatal `ModelManager` errors during client resource load. The game still reaches the title screen.
- [[Create Radars|Create: Radars]] `0.4.9.4`: blockstates `sonar_panel`, `sonar_bearing`, `smart_mount`,
  `sky_radar`, `siren`, `shield_jammer`, `radome` and models `shield_jammer`, `cannon_mount_radar`,
  `smart_cannon_mount`, `sky_radar_mount` fail with `JSON data was null or empty` / `EOFException`. The
  files inside the mod jar are empty.
- [[Create The Air War|Create: The Air War]] `5.00`: `models/entity/fab_1500.json` uses rotation `-17.5`,
  which vanilla rejects (only -45/-22.5/0/22.5/45 allowed).
- [[Create Misc and Things]]: `blazeblock.json` model fails; texture `vibration_mechanism2 copie.png` has an
  invalid path (space in filename) and is ignored.

## Reproduction
1. Launch the client and read `logs/latest.log`.

## Environment
- Pack version / commit: after `b40e3e3` + GeckoLib 4.9.3
- Affected mod versions: as above

## Root cause
Upstream asset bugs in the mod jars. The Radars errors were already in the 2026-09-01 client log, so
they're not a regression.

## Fix
None yet. Needs an in-game check: if the listed Radars blocks or the FAB-1500 bomb render as
missing-texture cubes, consider a resource-pack override. Otherwise leave it.

## Related
- [[Cross-mod compat noise on server boot]]

---
tags: [bug/status/open, bug/severity/cosmetic, bug/type/config, mc-version/1.21.1, loader/neoforge]
affected_mods: ["[[../01-Mods/Steam 'n' Rails]]", "[[../01-Mods/CBC More Shells]]", "[[../01-Mods/Create Connected]]", "[[../01-Mods/Create Misc and Things]]", "[[../01-Mods/Create TFMG Community Edition]]"]
date_opened: "2026-09-01"
date_resolved: ""
---

# Cross-mod compat noise on server boot

## Symptom
During the first successful headless NeoForge server boot test (2026-09-01, see
[[../04-Changelog/Changelog|changelog]]), the log showed a long run of non-fatal `ERROR`-level lines:

- `[[../01-Mods/Create Connected|Create: Connected]]`: dozens of
  `Couldn't parse element ... loot_table ... create_connected:blocks/dye_depot_*_fan_dyeing_catalyst -
  Unknown registry key` errors.
- `[[../01-Mods/Create Misc and Things|Create: Misc and Things]]`: several
  `Parsing error loading recipe create_things_and_misc:*` errors referencing items from mods that aren't
  installed (`nethers_exoticism`, `wildbackport`, `unusualend`), plus two referencing
  `create_things_and_misc:deleted_mod_element`.
- `[[../01-Mods/Create TFMG Community Edition|TFMG Community Edition]]` (likely): a warning that fluid tags
  `c:biodiesel, c:ethanol, c:high_cetane_diesel, c:high_octane_gasoline, c:hydrogen_fuel` aren't fully
  populated in the data pack.

None of these stopped the server from reaching `Done (6.503s)!` and idling cleanly afterward.

## Reproduction
1. Boot a NeoForge 1.21.1 dedicated server with this pack's current mod list.
2. Watch the log during data pack / recipe / loot table loading, before "Done".

## Environment
- Pack version / commit: as of the 2026-09-01 optimization-stack commit plus the Balm/Copycats+ fix commit
- Tested server-side only (no client/rendering mods loaded) via `packwiz-installer --side server` + manual
  NeoForge 21.1.249 server boot in a scratch instance outside the repo.

## Root cause
These three mods each ship optional cross-compat content (recipes/loot tables) gated on other mods that
aren't part of this pack — a normal, expected pattern for "kitchen sink" Create addons that support dozens
of possible mod combinations. The errors are Minecraft's data pack loader failing closed on the specific
recipes/loot tables that reference missing registry entries, not a sign anything in *our* pack is broken.

## Fix
No fix needed unless the noise becomes a problem (e.g. log spam hiding real errors during later testing).
If so, options: check each mod's config for a way to disable unused compat modules, or just accept the log
noise as normal for a large curated pack.

## Related
See [[../01-Mods/Create Copycats Plus|Create: Copycats+]]'s note for a related but separate finding from
the same boot test: [[../01-Mods/Sable|Sable]] logging `Unknown block: copycats:copycat_catwalk` on every
dimension load, also non-fatal.

## Update 2026-11-21: newer sources (counts from a full client boot)
Still non-fatal, and the same count on every boot (309 loot-table lines, checked across 3 logs), so a
*change* in these numbers is the signal to look closer:
| Source | Count | What it is |
|---|---|---|
| `railways` (Steam 'n' Rails) | 276 loot tables | Compat track variants for wood mods we don't have (`track_byg_*`, `track_tfc_*`, ...). Pure noise. |
| `cbcmoreshells` | 16 loot tables | Some use `minecraft:copy_nbt` (removed in 1.21), others point at items that don't exist (e.g. `landing_indicator`). Those blocks may **drop nothing** when broken. |
| `cbcmoreshells` | 2 recipes | `dual_he_rocket` and `dual_aphe_rocket` use the old `{"item":...}` result format, so those two rockets have **no recipe** in this pack. Real upstream bug. |
| `create_connected` | 16 loot tables | As above (dye depot compat). |
| `arcon` (Armored Constructs) | 1 loot table | Compat/upstream noise. |
| `create_things_and_misc` | ~6 recipes | As above (sail/chair compat). |

**Possible fixes if they matter:** a KubeJS recipe for the two dual rockets, and KubeJS loot tables for the
CBC More Shells blocks that drop nothing. Not done yet; flag to the owner if players notice.

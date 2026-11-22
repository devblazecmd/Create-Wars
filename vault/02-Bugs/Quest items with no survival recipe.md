---
tags: [bug/status/open, bug/severity/major, bug/type/version-incompatibility, mc-version/1.21.1, loader/neoforge]
affected_mods: ["[[../01-Mods/Create Armored Constructs]]", "[[../01-Mods/CBC Military Supplement]]", "[[../01-Mods/Synaxis]]", "[[../01-Mods/Create The Air War]]", "[[../01-Mods/FTB Quests]]"]
date_opened: "2026-11-22"
date_resolved: ""
---

# Quest items with no survival recipe

## Symptom
`tools/audit_quests.py` (live recipe export, 9,671 recipes) found quests that ask for items no loaded
recipe makes. Those quests can't be completed in survival.

## Confirmed: nothing makes them
Not in the live recipe manager, and no recipe file for them in any jar:
- **[[../01-Mods/Create Armored Constructs]] (`arcon` 1.0.0): none of its 116 items has a recipe.** The jar has
  no `recipe` folder at all, even though the mod page says the "Arsenal" section "provides crafting recipes".
  Quests: Armored `arcon`, `arcon_breech`, `arcon_muzzle`, `bops`.
- **[[../01-Mods/CBC Military Supplement]] 3.0.7:** `racked_torpedo`, `he_bouncing_bomb`, `depth_charge`,
  `torpedo_detection_device`, `rocket_bracket` (only block loot tables exist). 275 of its 385 items have no recipe,
  but most of those are cannon parts made by casting. Quests: Aeronautics `aerial_torpedo`, `bouncing_bomb`,
  `rocket_bracket`; Naval `depth_charge`, `torpedo_detector`.
- **Synaxis 1.6.3:** `synaxis:jet` (Aeronautics `jet`).
- **Create: The Air War 5.00:** `fpv_drone`, `drone_controller` (Drones `fpv`, `drone_joystick`).

## Fine: made by a mechanic, not a recipe
Fluid buckets (filled with a spout or by hand), Big Cannons cannon parts (casting / cannon builder),
`create:blaze_burner` (catch a blaze), levitite (Aeronautics blend that sets in the world). **Check in JEI:**
`createbigcannons:autocannon_cartridge`.

## Fix
Owner decision pending. Options: write KubeJS recipes for them, drop the quests, or (for Armored Constructs)
treat the mod as creative-only or replace it.

---
tags: [bug/status/fixed, bug/severity/major, bug/type/config, mc-version/1.21.1, loader/neoforge]
affected_mods: ["[[../01-Mods/FTB Quests]]", "[[../01-Mods/Packwiz]]"]
date_opened: "2026-11-22"
date_resolved: "2026-11-22"
---

# Running game overwrites synced quest book

## Symptom
The owner reported "nothing updated" after quest-layout changes had been generated, committed and synced to the
instance. The game showed the old book: Brass Casing still linked to Brass Hand and Electron Tube.

## Cause
The game was still running while `packwiz-installer` copied the new `config/ftbquests/quests/*.snbt` into the
instance. FTB Quests keeps the book in memory and **saves it back to disk** (here at 04:24:51, a minute after the
sync). That replaced the new files with the old book, reformatted. packwiz-installer then treats those files as
current (its cache says they were installed), so a later sync doesn't restore them.

This is probably also part of why Nuclear Age "wasn't staying" in the Ages tab earlier that day.

## Fix
Close the game, delete `<instance>/config/ftbquests/quests`, copy `pack/config/ftbquests/quests` over it, then
relaunch. After that, all chapter files matched the pack byte for byte, and the game loaded 24 chapters and
549 quests.

## How to avoid it
- **Never sync quest changes while the game is running.** Close it first (or ask the owner to), sync, then launch.
- After syncing, `cmp` a chapter file in the instance against `pack/` to confirm it really landed.
- In-game edits to the book are also lost on the next sync. Make changes in `tools/quests/build_quests.py`.

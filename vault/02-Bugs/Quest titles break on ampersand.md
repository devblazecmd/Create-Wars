---
tags: [bug/status/fixed, bug/severity/minor, bug/type/visual, mc-version/1.21.1, loader/neoforge]
affected_mods: ["[[../01-Mods/FTB Quests|FTB Quests]]"]
date_opened: "2026-11-21"
date_resolved: "2026-11-21"
---

# Quest titles break on ampersand

## Symptom
The Radar chapter's name showed an error in the quest book (owner report, 2026-11-21).

## Cause
FTB Quests reads `&` as the start of a colour/format code (`&a`, `&7`, `&r`, ...). A plain `&` followed
by a space ("Radar & Missiles") is an invalid code, so the text doesn't render properly. The same problem
was in "Mechanical Press & Depot", "Auto Yaw & Pitch Controllers" and a "Requires: Press & Depot" line.

## Fix
Changed `&` to "and" in `tools/quests/build_quests.py`, then regenerated the book.

## Rule going forward
In quest text, only use `&` for real format codes. Write "and" everywhere else. Check for strays with:
`grep -nE '[^&]& ' pack/config/ftbquests/quests/lang/en_us.snbt` (it should find nothing).

Related: [[../03-Design/Quest Book|Quest Book]]

---
tags: [design/progression, mc-version/1.21.1, loader/neoforge]
status: approved
---

# Quest Book v4: Plan (challenges-tab, automation-breakout, automation-agriculture)

Specs (approved 2026-11-23; owner: "i can make edits after you give the initial outline"):
[[Quest Book v4 - challenges-tab]], [[Quest Book v4 - automation-breakout]],
[[Quest Book v4 - automation-agriculture]]. Map: [[Quest Book v4 - Capability Map]].
`task-types`, `exploration` and `bounties` get their own plan once these ship.

The task list lives in this note (same as [[Quest Book - Plan]]), not in `tasks/todo.md`.

## Architecture decisions
- **ID snapshot tool first.** Every restructure is checked by machine: a script dumps every quest / task /
  reward ID *and* each reward's amount from the generated SNBT, then diffs it against a saved snapshot.
  Moving quests must be a no-op in that diff, apart from intended changes.
- **`id_chapter` + ID-aware references.** Today `"chapter/quest"` refs, chapter `unlock`s and the writer
  all compute `qid(chapter, quest)` from the chapter a quest *sits in*. After the override, a quest's ID
  comes from its `id_chapter`. So the generator builds one `slug → effective ID` table and resolves every
  ref through it. That lands with zero output change before anything moves.
- **Tier chapters use `connected=False`.** With one hub per chapter, `levels_for` would treat the hub as
  a chapter finale (+5 instead of +2). Marking the chapters as separate bubbles keeps every reward amount
  identical. The snapshot diff catches any slip.
- **Agriculture grows out of the old Food bubble.** The breakout creates `agriculture` holding the 4
  existing food quests (same IDs), and the agriculture tasks fill it in. That way no task leaves the food
  quests homeless.
- **Food data as a table, not 131 hand-written `Q()` calls.** A `FARM` table of
  `(group, item_id, count, title, desc)` is expanded into quests. Capstones and sub-hubs are generated from
  the groups.
- **Capstones** use `hidden_deps` (deps + hidden lines). A new layout key **`place: {slug: (x, y)}`**
  gives them (and any other hand-placed quest) explicit positions, since a chapter supports only one
  `gate`.
- **Milk/egg rule is computed once, then frozen.** A helper reads the recipe export and prints which food
  items need milk or eggs on *every* recipe. The result is pasted into the generator as a constant with a
  dated comment, so the generator never depends on an instance export to run. `audit_quests.py` re-checks
  it on each audit.
- **Stack sizes from the game, not from memory.** `export_registry_ids.js` gains each item's max stack
  size. Amounts are 64 / 16 / 8 / 4 per the spec, picked from that data.

## Task list

### Phase 1: Foundation + Challenges tab
- [x] **T1: ID snapshot tool**
  - Acceptance: `python -I tools/quest_ids.py snapshot <file>` writes `{quest/task/reward id → chapter file,
    type, amount}`. `python -I tools/quest_ids.py diff <file>` lists added / removed / moved / amount-changed
    entries. Running both on an untouched build gives an empty diff.
  - Verify: generate → snapshot → regenerate → diff = empty.
  - Files: `tools/quest_ids.py` (new). Size: S.
- [x] **T2: Challenges tab**
  - Acceptance: `GROUPS` gains `("challenges", "Challenges")` last. Defend Your Home `group="challenges"`.
  - Verify: generator clean; `check_quest_refs.py` 0 unknown; snapshot diff = **no ID or amount changes**;
    `git diff` touches only `chapter_groups.snbt`, lang, `defense.snbt`.
  - Files: `build_quests.py`, generated output. Size: XS. Deps: T1.

### Phase 2: Automation breakout
- [x] **T3: `id_chapter` override + ID-aware references (no content change)**
  - Acceptance: `Q(..., id_chapter=None)` and a chapter-level `id_chapter`. One effective-ID table drives
    quest/task/reward IDs, dependency refs, `unlock`s and `extra_deps`. Cross-chapter ref validation uses
    the table.
  - Verify: generated output **byte-identical** to before (`git diff --stat` empty after regenerating).
  - Files: `build_quests.py`. Size: S. Deps: T1.
- [x] **T4: Split Automation into tier chapters + Agriculture shell**
  - Acceptance: 6 tier chapters (Andesite, Brass, Heat, Industrial, Quantum, Enchanting) + `agriculture`
    (the 4 food quests), all in group `automation`, all `id_chapter="automation"`, each `connected=False`,
    chapter unlocks = the old bubbles' extra deps. Old `automation` chapter removed.
    `rockcutting_wheel` → `automation/crushing` ref updated. `audit_quests.py` filter on `"automation"`
    updated.
  - Verify: generator clean (layout checks pass); snapshot diff shows **only moved-file entries, 0 added /
    removed / amount-changed**; refs 0 unknown; audit 0 order gaps.
  - Files: `build_quests.py`, `tools/audit_quests.py`, generated output. Size: M. Deps: T3.
- [x] **T5: Export max stack sizes**
  - Acceptance: `pack/kubejs/server_scripts/export_registry_ids.js` also writes each item's max stack size.
    Readers ignore it if missing.
  - Verify: boot at Checkpoint A, then the export contains e.g. `minecraft:egg → 16`,
    `minecraft:milk_bucket → 1`.
  - Files: `export_registry_ids.js`. Size: XS.

### Checkpoint A: restructure done
Boot 2026-11-23: `Loaded 8 chapter groups, 30 chapters, 562 quests, 4 reward tables`, 0 FTB Quests errors; instance
quest files byte-identical to `pack/` after load; export has `max_stack` (egg 16, milk bucket 1, cake 1, soup 16).
- [x] Sync to the instance with the **game closed**, `cmp` the synced quest files, boot. 0 FTB Quests
      errors. Export refreshed (T5).
- [ ] Owner: Challenges tab shows Defend Your Home. Automation tab shows 6 tier chapters + Agriculture
      (4 quests). Existing progress is intact.
- [ ] Decisions log entry (done); commit (with owner OK).

### Phase 3: Agriculture
- [x] **T6: Agriculture layout spike (high risk, first)**
  - Acceptance: `FARM` table with all 131 items (IDs + amounts from the T5 export), 3 circle hubs, 9 sub-hub
    entries, 13 capstones (`hidden_deps`), `place` layout key. Chapter passes `check_layout` (no overlaps,
    no lines through quests). Descriptions may be one-line stubs.
  - Verify: generator clean; refs 0 unknown; snapshot diff = 4 existing quests unchanged + only additions.
  - Files: `build_quests.py`, generated output. Size: M. Deps: Checkpoint A.
- [x] **T7: Rewards + milk/egg rule**
  - Acceptance: item quests `levels=1`; sub-hub entries/hubs +2; capstone levels per the spec table
    (Crops 9, Meats 5, Fan 8, Slicer 5, Mixing 14, Spout 5, Bakery 7, Assembly 11, Feasts 5; Farmer/Rancher
    15, Chef 25, Feed the Army 30) and rolls (Spoils II ×1, ×2 for 20+; War Trophy ×1 for circle capstones,
    ×2 for the finale). Milk/egg list computed, frozen into the generator, applied as hidden deps on
    `auto_milk` / `auto_eggs`.
  - Verify: `audit_quests.py` XP section shows Agriculture ≈ 310 levels; audit re-check of the milk/egg list
    matches; 0 order gaps.
  - Files: `build_quests.py`, `tools/audit_quests.py`. Size: S. Deps: T6.
- [x] **T8: Descriptions: Crop circle + Animal Products (31 items, 5 hubs/sub-hubs/capstones)**
  - Acceptance: each description names the machine and recipe from the recipe export/JEI. Hub text explains
    the harvester / mob-farm / deployer approach.
  - Verify: spot-check each stated recipe against the export; deployer milking and shearing confirmed in
    game before being stated (otherwise worded neutrally).
  - Files: `build_quests.py`. Size: S. Deps: T6.
- [x] **T9: Descriptions: Fan Cooking, Slicer, Spout, Feasts (39 items + sub-hubs)**
  - Same acceptance/verify as T8. Size: S. Deps: T6.
- [x] **T10: Descriptions: Mixing, Bakery, Assembly (61 items + sub-hubs + Master Chef / finale)**
  - Same acceptance/verify as T8. Size: M. Deps: T6.

### Checkpoint B: Agriculture done
- [x] Generator clean; refs 0 unknown; audit 0 hidden / 0 order gaps; snapshot: 4 old quests keep IDs.
- [ ] Game closed → sync → `cmp` → boot, 0 FTB Quests errors.
- [ ] Owner reviews the chapter in game (layout, names, rewards) and edits.
- [ ] T11 below, then commit (with owner OK).

- [ ] **T11: Docs**
  - Acceptance: [[Quest Book]] decisions log + book-structure table updated (tabs, chapter counts, quest
    total); the three specs flipped to `status: approved` and their success criteria ticked; changelog entry;
    capability map marks the three modules shipped.
  - Files: vault notes only. Size: S.

## Parallelization
Sequential through T4 (shared generator internals). T5 can be done any time before Checkpoint A. After T6,
T7 to T10 all touch `build_quests.py` but different data rows, so they're safe to do in any order. One
session doing them in sequence is simplest.

## Risks and mitigations
| Risk | Impact | Mitigation |
|---|---|---|
| A moved quest gets a new ID → teams lose progress | High | T3 must be byte-identical; T1 snapshot diff on every restructure; amount diffs catch level-role changes |
| 27-item fans / 156-quest chapter can't lay out cleanly | Med | T6 spike first; `place` for hand positions; sub-hubs as their own bubbles if fans collide |
| Running game overwrites synced quest files | Med | Close the game before sync, then `cmp` (memory note) |
| Stale `automation.snbt` lingers in the instance | Low | Generator deletes stale chapter files in `pack/`; check the instance's chapter folder after sync |
| Wrong recipe stated in a description | Med | Descriptions only from the recipe export/JEI; in-game check for deployer milking/shearing |
| ~310 levels feels like too much | Low | Owner reviews at Checkpoint B; capstone levels are constants, easy to tune |

## Open questions
None blocking.

---
tags: [design/progression, mc-version/1.21.1, loader/neoforge]
status: approved
---

# Spec: challenges-tab

Module of [[Quest Book v4 - Capability Map]]. Parent spec: [[Quest Book]].

## Objective
Owner (2026-11-23), first: bounties go in a renamed "Challenges" tab with all challenges in it. Then
revised: "bring back the automation tab then break automation tab out". Owner picked **Automation +
Challenges**: the Automation tab stays (and gets broken into chapters, see
[[Quest Book v4 - automation-breakout]]), and a **new Challenges tab** holds the combat challenge tiers:
**Defend Your Home** now, **Bounties** later.

## Assumptions
1. Know Your Enemy stays in Warfare (it's a one-kill-per-mob guide and unlocks Defend Your Home).
2. Challenges is the **last** tab in the sidebar, after Automation.

## Changes (`tools/quests/build_quests.py`)
- `GROUPS`: append `("challenges", "Challenges")`. The `automation` group is unchanged.
- Defend Your Home: `group="warfare"` → `group="challenges"`. Chapter slug, quest slugs and unlock
  (`enemy/ambush`) unchanged, so progress is kept (quest IDs don't depend on the group).

## Commands
```
python -I tools/quests/build_quests.py
python -I tools/check_quest_refs.py
python tools/audit_quests.py --instance "C:/Users/blake/AppData/Roaming/PrismLauncher/instances/Create Wars - Testing/minecraft"
cd pack && packwiz refresh
```
Close the game before syncing to the instance, then `cmp` the synced files.

## Testing
- Generator runs clean. Ref check: 0 unknown.
- `git diff`: new group in `chapter_groups.snbt` + lang, and the `defense` chapter's `group` field. No quest
  IDs change.
- In game: Challenges tab shows Defend Your Home. Warfare no longer does. Existing progress is intact.

## Boundaries
- Always: keep slugs; log in [[Quest Book]]'s decisions log.
- Ask first: moving any other chapter into Challenges.
- Never: rename chapter or quest slugs.

## Success criteria
- [ ] New last tab "Challenges" holds Defend Your Home.
- [ ] Automation tab still exists.
- [ ] No quest ID changed; clean boot, 0 FTB Quests errors.

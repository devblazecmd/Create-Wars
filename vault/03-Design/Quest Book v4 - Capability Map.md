---
tags: [design/progression, mc-version/1.21.1, loader/neoforge]
status: approved
---

# Quest Book v4: Capability Map

Owner request (2026-11-23): "more depth and some more things added" to the quests. Owner picked:
- **Deeper Automation challenges**, starting with farming: every crop and meat, every food item, and the
  animal products, in separate circles. The Automation tab is broken into one chapter per tier so each
  can go deeper later.
- **Exploration chapter.**
- **Repeatable / bounty quests.**
- **Phased delivery:** each module gets its own spec and ships separately.

Parent spec: [[Quest Book]]. Generator: `tools/quests/build_quests.py` (source of truth, see its header).

| Module id | Responsibility | Depends on |
|---|---|---|
| `challenges-tab` | New **Challenges** tab (last in sidebar) for the combat challenge tiers: Defend Your Home moves in from Warfare, and Bounties is added later. Spec: [[Quest Book v4 - challenges-tab]]. | — |
| `automation-breakout` | Split the single Automation chapter into **one chapter per tier** (Andesite, Brass, Heat, Industrial, Quantum, Enchanting) inside the Automation tab. Restructure only. Generator gains an `id_chapter` override so every moved quest keeps its ID and progress. Spec: [[Quest Book v4 - automation-breakout]]. | — |
| `automation-agriculture` | New **Agriculture** chapter in the Automation tab: Crop (18 crops + 8 meats), Food (100 items across 7 method sub-hubs), Animal Products (5). Item quests +1 level. Big **completion capstones** per sub-hub and circle, and a "Feed the Army" finale. Milk ships as buckets; `task-types` may upgrade it to a "tank holding milk" observation later. Spec: [[Quest Book v4 - automation-agriculture]]. | `automation-breakout` |
| `task-types` | Generator support for the FTB Quests task types the book doesn't write yet: **dimension**, **biome**, **structure**, **advancement**, optionally **fluid** and **observation**. The format comes from FTB Quests 2101.1.39 bytecode and an in-game save. `check_quest_refs.py` learns to validate the new IDs. | — |
| `exploration` | New **Exploration** tab + chapter: Nether, End, Stellarity's dragon, Incendium, CTOV / Pillager Arise / Illager Invasion structures, Biomes O' Plenty biomes. | `task-types` |
| `bounties` | New **Bounties** chapter in the Challenges tab. **Repeatable** (FTB `can_repeat` + `repeat_cooldown`, **12 h**): kill bounties (existing mobs only) and delivery bounties (farm or factory output). Pays Spoils of War rolls + XP. Defend Your Home stays one-time. | `challenges-tab`, `automation-agriculture`; `task-types` only if bounties use structure or biome tasks |

**Build order:** `challenges-tab` → `automation-breakout` → `automation-agriculture` → `task-types` →
`exploration` → `bounties`.
Follow-ups after that: deepen each tier chapter from `automation-breakout`, each with its own small spec.
- 2026-11-23: Andesite done ([[Quest Book v4 - automation-andesite]]), using the shared grouped-chapter builder.

## Owner answers (2026-11-23)
1. Tabs: keep the **Automation** tab and break it into chapters. A new **Challenges** tab holds Defend
   Your Home and Bounties. (This replaces the earlier "rename Automation to Challenges".)
2. Automation breakout: **one chapter per tier**. Ore/basics can stay light.
3. Bounty cooldown: **every 12 hours**.
4. Exploration gets **its own tab**.
5. Milk: **fill a tank if it can be tracked, otherwise buckets.** FTB Quests 2101.1.39: `FluidTask` only
   reads the player's inventory. `ObservationTask` has `BLOCK_ENTITY` + NBT filter, so a tank check *may*
   work after `task-types`. Buckets first.
6. Agriculture: all crops (vanilla + Farmer's Delight), every food item including all of FD ("it is a
   challenge tier after all"), honey included.
7. Rewards: "the hubs need to feel worth the work getting to them" → completion capstones.

## Why this order
- `challenges-tab` and `automation-breakout` are pure restructures (no new content), easy to verify by
  ID equality, and they set up the tabs everything else goes into.
- `automation-agriculture` needs the breakout's `id_chapter` override and Automation tab layout.
- `task-types` is the risky one (undocumented SNBT format). Isolating it keeps exploration's content
  from being blocked on format debugging.
- `bounties` last: it points at content the other modules create.

## Constraints carried from the parent spec / CLAUDE.md
- Rewards stay XP + materials + existing reward tables. Nothing that skips a tier.
- No PvP tasks.
- Mob-side balance is an **open decision** (CLAUDE.md). Bounties target existing mobs and don't
  rebalance them.
- Every item/entity/biome/structure ID is checked against the live registry export, never guessed.
- Quest edits go in the generator; close the game before syncing.

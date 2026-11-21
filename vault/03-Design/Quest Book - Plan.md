---
tags: [design/progression, mc-version/1.21.1, loader/neoforge]
status: in-progress
---

# Quest Book: v1 Plan (chapters 1–4)

Implementation plan for [[Quest Book]] v1. **Status: T1–T7 built and loading in game (2026-11-21); owner review in progress.**
Kept in the vault (not `tasks/`) because the vault is this repo's source of truth for design work.

## Approach
Claude writes the quest SNBT directly; the owner reviews in game (spec decision 4). Quests guide only,
reward XP + materials, and have no PvP tasks.

### Components and order
```
T1 format spike ──→ T2 reference checker ──→ T3 book skeleton ──→ T4 Ch1 ──→ T5 Ch2 ──→ T6 Ch3 ──→ T7 Ch4 ──→ T8 sign-off
```
Sequential: every chapter depends on the format (T1), the checker (T2) and the skeleton (T3). Chapters
5–16 are out of scope.

### Content correction found while planning
Brass needs a **heated** Mixer, so a Blaze Burner comes *before* brass. Chapter 3 therefore opens with
capturing a Blaze (Empty Blaze Burner), and Chapter 4 ("Heat") focuses on superheating and the
[[Blaze Burner Fuel Tiers]]. This fits the spec's chapter goals; only the boundary between 3 and 4
moves.

## Risks
| Risk | Mitigation |
|---|---|
| FTB Quests 2101 SNBT/lang layout differs from older guides (text moved into `lang/*.snbt` via `TranslationManager`) | T1: get an authoritative sample before writing anything at scale |
| Hand-written IDs (16-hex) collide or are malformed | Generate IDs with a script (random 64-bit, uppercase hex, checked unique) |
| Quest points at a wrong or removed item | T2 checker must report 0 unknown IDs before shipping |
| Quest text drifts from the KubeJS scripts | Recipe-stating quests cite the script; T8 re-checks each against JEI |
| Layout (x/y) looks messy in the book | Owner reviews visually; positions are easy to tweak in the editor afterwards |

## Tasks

- [x] **T1: Format spike**
  - Acceptance: an authoritative sample of FTB Quests 2101's on-disk format (data file, one chapter, one
    quest with an item task + XP + item reward, lang entries) is recorded in this note.
  - How: owner opens the editor (`/ftbquests editing_mode`), makes **one** throwaway chapter + quest,
    and closes the game; Claude reads the generated `config/ftbquests/quests/` files. Fallback if the
    owner prefers zero editor time: derive the format from the jar's bytecode (slower, less certain).
  - Verify: files exist and parse; format documented below.
  - Files: this note only (throwaway files are deleted afterwards).

- [x] **T2: Reference checker**
  - Acceptance: a script lists every item/block ID referenced in the quest SNBT and reports any not
    registered in the pack. Known IDs come from: every mod jar in the instance (item/block model and
    lang keys), the vanilla 1.21.1 client jar, and `createwars:*` items in `kubejs/startup_scripts/`.
  - Verify: run on a test SNBT containing one real ID, one fake ID (`create:not_a_thing`), and one
    removed item (`mob_radar:mob_radar`). It must flag exactly the last two.
  - Files: `tools/check_quest_refs.py` (**new top-level `tools/` folder, needs owner OK**; alternative is
    keeping it outside the repo, which loses it for future chapters).

- [x] **T3: Book skeleton**
  - Acceptance: `pack/config/ftbquests/quests/` has the book file, 4 chapter files (welcome, kinetics,
    brass_and_precision, heat) with one placeholder entry quest each, lang file; ships via
    `packwiz refresh`; instance sync.
  - Verify: checker = 0 unknown; boot into world, 0 FTB Quests errors in `latest.log`; owner sees 4
    chapters.
  - Files: ~6 new SNBT files, `pack/index.toml`.
  - **Checkpoint: owner glance at the 4 empty chapters before content goes in.**

- [x] **T4: Chapter 1, Welcome to the War** (~6 quests, checkmark tasks)
  - Content: open the book; make or join a team (FTB Teams); claim chunks (FTB Chunks); pack rules:
    no elytras (gliding blocked), waystones don't generate and must be crafted (Telejuice), Air War
    launchers removed; "where to go next" pointer to Chapter 2.
  - Rewards: small XP; starter materials (bread, torches, logs). No tools above stone.
  - Verify: checker; boot; owner completes the chapter.

- [x] **T5: Chapter 2, Kinetics** (~10 quests, mostly item tasks)
  - Content: Andesite Alloy → Shaft/Cogwheel → Water Wheel (power) → Millstone → Mechanical Press →
    Basin + Mechanical Mixer → Encased Fan (bulk washing/smelting) → Belt/Depot → Mechanical Saw/Drill →
    Goggles (stress readout).
  - Rewards: XP + andesite alloy / iron / zinc in modest amounts.
  - Verify: checker; boot; owner completes first + last quest.
  - **Checkpoint: owner reviews tone/length/reward size before T6–T7 copy the pattern.**

- [x] **T6: Chapter 3, Brass & Precision** (~9 quests)
  - Content: Empty Blaze Burner → capture a Blaze → heated Mixer → Brass Ingot → Brass Casing →
    Electron Tube → Mechanical Crafter (big recipes, incl. waystones later) → Precision Mechanism
    (sequenced assembly) → Deployer.
  - Rewards: XP + copper/zinc/gold nuggets.
  - Verify: checker; boot; owner completes first + last quest.

- [x] **T7: Chapter 4, Heat** (~8 quests)
  - Content: Cinder Flour → Blaze Cake Base → Blaze Cake (Tier 1 superheat) → **Diamond** (9 Coal Blocks,
    superheated compacting) → Straw + Biofuel (Tier 2, brewing needs superheat) → Napalm (Tier 3, TFMG,
    late; marked optional) → Telejuice teaser pointing toward the future Teleportation chapter.
  - Every recipe stated must match `diamond_compacting.js` / `blaze_burner_tiers.js`.
  - Rewards: XP + coal/sugar/eggs. **No diamonds or blaze cakes as rewards** (would skip the tier).
  - Verify: checker; boot; owner completes first + last quest.

- [ ] **T8: v1 sign-off**
  - Acceptance: all spec success criteria for chapters 1–4 pass; changelog entry; FTB Quests note
    flipped to describe the book; spec decisions log updated.
  - Verify: checker 0 unknown; clean boot; owner playthrough of chapters 1–4.
  - Files: changelog, `01-Mods/FTB Quests.md`, `Quest Book.md`.

## Owner decisions on the plan (2026-11-21)
1. T1 method: "do what you think is best". Format derived from FTB Quests 2101.1.39 bytecode, then
   proven by booting a generated book (no editor time needed).
2. Top-level `tools/` folder: approved.

## Build notes (2026-11-21)
- Owner said "do what you think is best", so T3–T7 ran straight through. The owner's in-game review
  replaces the T3/T5 checkpoints.
- Source of truth is the generator `tools/quests/build_quests.py` (content + stable slug-derived IDs),
  not hand-edited SNBT. In-game editor changes are overwritten on regeneration, so port them back.
- Boot result: `Loaded 1 chapter groups, 4 chapters, 40 quests`; translation table synced to client.
  0 FTB Quests warnings. Checker: 0 unknown, 0 banned.
- The game re-saves files it considers non-canonical. The generator was adjusted until 3 of 4 chapter
  files and `data.snbt` matched the game's own re-save exactly (Welcome changed afterwards).
- Owner review: **"Know What's Removed" (Welcome) removed** at the owner's request; "Start Building"
  now depends on "Waystones Are Built, Not Found". Book now 39 quests.
- Reload without restart: `/ftbquests reload`.

## v2 restructure (2026-11-21): sections, ages, expansions
- [x] **V2-1: Sections + renames + unlocks + automate quests**: 3 chapter groups (Getting Started, Ages,
  Expansions); Kinetics → Andesite Age, Brass & Precision → Brass Age, Heat → Heat Expansion (slugs
  kept, so progress is kept); explicit chapter unlocks; `progression_mode: linear`; one-stack automate
  quests (Andesite: cobblestone, andesite alloy, iron nuggets, wheat [optional]; Brass: brass, zinc via
  crushing, electron tubes, precision mechanisms; Heat: blaze cakes, diamonds, biofuel ×16);
  "Andesite Age Complete" gates Brass; "Brass Age Complete" gates Industrial + expansions.
  Verified: checker 0/0; boot `Loaded 4 chapter groups, 4 chapters, 51 quests`; all files match the
  game's re-save.
- [ ] **V2-2: Industrial Age** (TFMG steel + oil → gasoline → napalm; move napalm out of Heat).
- [ ] **V2-3: Quantum Expansion** (chorus → Telejuice → Quantum Pearl/Paper/Casing → waystones,
  scrolls; move the Telejuice teaser out of Heat).
- [ ] **V2-4: Enchanting Expansion** (Create: Enchantment Industry).
- [ ] **V2-5: owner playthrough** of the unlock chain (Welcome → Andesite Complete → Brass Complete →
  each expansion opens).

## Format reference (filled in by T1)
Derived from FTB Quests 2101.1.39 bytecode and confirmed by a clean load + the game's own re-save.
```
config/ftbquests/quests/
  data.snbt            { version: 13, progression_mode, default_*, presets, ... }  (keys sorted)
  chapter_groups.snbt  { chapter_groups: [ { id: "<ID>" }, ... ] }   (sidebar order; title in lang
                       as "chapter_group.<ID>.title"; chapters point at it with group: "<ID>")
  chapters/<slug>.snbt { id, filename, group, order_index, icon: {id}, images: [], quest_links: [],
                         default_quest_shape, default_hide_dependency_lines, quests: [...] }
  lang/en_us.snbt      { "chapter.<ID>.title": "...", "chapter.<ID>.chapter_subtitle": ["..."],
                         "quest.<ID>.title": "...", "quest.<ID>.quest_subtitle": "...",
                         "quest.<ID>.quest_desc": ["line", ...] }
quest  { id, x: 0.0d, y: 0.0d, shape?, size?, optional?, dependencies: ["<ID>"], tasks: [...], rewards: [...] }
task   { id, type: "item", item: {count: 1, id}, count: 4L (omitted when 1) } | { id, type: "checkmark" }
reward { id, type: "xp", xp: 10 } | { id, type: "item", item: {count: 1, id}, count: 8 }
IDs: 16 uppercase hex digits (%016X of a long). Text keys: "<type>.<ID>.<key>"; quest_desc and
chapter_subtitle are lists, title and quest_subtitle are strings.
```

---
tags: [design/progression, mc-version/1.21.1, loader/neoforge]
status: approved
---

# Quest Book (Spec)

Spec for the pack's FTB Quests book. **Status: approved 2026-11-21 (v1 = chapters 1–4).** No quest files exist
yet (`config/ftbquests/quests/` is absent in both the pack and the Prism instance as of 2026-11-21).

## Goal
Give players a guided path from first cogwheel to fielding an armed faction: aircraft, artillery,
radar-guided missiles, armored trains, submarines. The book teaches the pack's *custom* systems,
which nobody can learn from outside wikis: Blaze Burner fuel tiers, Telejuice → Quantum items →
Waystones, the diamond recipe, no elytras. It also gives teams shared goals that tie progression to the
"war" theme.

**Who:** a team of players (FTB Teams) on a PvP/PvE server, new to some or all of the Create addons.

**Success looks like:** a new team can open the book and, following it alone, reach every major
system without alt-tabbing to a wiki, and nothing in the book references an item that doesn't exist.

## Mechanics

### Platform
- [[../01-Mods/FTB Quests|FTB Quests]] `2101.1.39`, [[../01-Mods/FTB Teams|FTB Teams]] (progress is per team
  by default), [[../01-Mods/FTB Library|FTB Library]].
- Quest data lives in `config/ftbquests/quests/` as SNBT (`data.snbt`, `chapters/*.snbt`,
  `reward_tables/*.snbt`, `lang/en_us.snbt`). Shipped by copying into `pack/config/ftbquests/quests/`
  and running `packwiz refresh`, the same way `waystones-common.toml` ships.

### Book structure v3: guidance chapters + a separate Automation chapter (2026-11-21)
Owner: "the quest is more for guidance". Automation goals moved out of the Ages into their own
section, and the remaining chapters were built in the hub-and-spoke style.

| Section (chapter group) | Chapter | Unlocked by | Quests |
|---|---|---|---|
| **Getting Started** | Welcome to the War | none | 6 |
| **Ages** | Andesite Age | Welcome | 25 |
| | Brass Age | Andesite Age Complete (casing, press & depot, basin & mixer, belts, iron sheets) | 17 |
| | Industrial Age (TFMG) | Brass Age Complete (brass casing, electron tube, deployer, precision mech, crafter) | 20 |
| **Expansions** | Heat Expansion | Brass Age Complete | 9 |
| | Quantum Expansion (Teleporters + Quantum items + waystones) | Brass Age Complete | 23 |
| | Enchanting Expansion (Create: Enchantment Industry) | Brass Age Complete | 11 |
| **Infrastructure** | Food (Farmer's Delight, Create: Slice & Dice) | Welcome | 28 |
| | Storage (Sophisticated Backpacks, Sophisticated chests + tier upgrades, Create Item Vault, Tom's Simple Storage network) | Welcome | 25 |
| | Pollution and Air (Create: Smog machines + Thick Air oxygen gear) | Welcome (Smog machines also need Andesite Alloy / Casing / Brass / Brass Casing / Precision) | 28 |
| **Warfare** | Artillery (CBC + Firepower Components + Ballistic Computer) | Andesite Age Complete | 36 |
| | Infantry (Create: Gunsmithing) | Andesite Age Complete | 28 |
| | Radar and Missiles (Create: Radars + Fire Arc Filter + CBC Aeronautics Missiles) | Brass Age Complete + Artillery's Cannon Mount | 25 |
| | Aeronautics (Create Aeronautics, Sable/Simulated, Air War, CBC bombs, Synaxis) | Brass Age Complete | 35 |
| | Naval (Create: High Seas, Deep Seas, CBC torpedoes) | Brass Age Complete | 27 |
| | Rail Warfare (Create trains, Steam 'n' Rails, Who Touched My Train, Locometal) | Brass Age Complete | 17 |
| | Armored Vehicles (Offroad, Bits 'n' Tracks, RHA, Armored Constructs) | Brass Age Complete | 17 |
| | Drones (Droneworks, Air War FPV) | Brass Age Complete | 12 |
| | Know Your Enemy (Improved Mobs, Enhanced AI, Trigger Mobs, AMBUSH; kill tasks on vanilla mobs) | Welcome | 24 |
| | Demolitions (Create: Warnautics bombs, mines, C4, missiles) | Artillery's High Explosive Shell (medium bomb also needs Impact Fuze + Mechanical Crafter; AIM-9 needs Proximity Fuze) | 23 |
| **Automation** | Automation: one hub per tier (Andesite, Brass, Heat, Industrial, Quantum, Enchanting) | Andesite Casing; each later hub also needs its chapter's key quest | 25 |

- Ages and expansions are **guidance**: each quest is "make this machine/material", following real
  recipe order (read from the jars). Andesite Age Complete / Brass Age Complete gate on key machines.
- **Automation** holds the "make X by machine" goals (mostly one stack; tubes/precision 5; iron 7
  blocks). Its hubs use cross-chapter dependencies (`extra_deps`, e.g. Industrial Automation needs
  `industrial/steel`). These aren't drawn, since FTB only draws lines inside a chapter.
- Napalm moved Heat → Industrial (needs `heat/biofuel` too). Telejuice moved Heat → Quantum.
- Moved automate quests got new IDs (chapter is part of the ID), so progress on them resets.

### Flat chapter map (v1 draft, superseded by v2 above if approved)
Ordered roughly by progression. Each chapter is a node graph of quests with dependencies.

| # | Chapter | Covers | Gate into it |
|---|---|---|---|
| 1 | Welcome to the War | Pack rules: no elytras, no wild waystones, teams and claims (FTB Teams/Chunks), the quest book itself | none |
| 2 | Kinetics | Create basics: water wheel → andesite alloy → shafts, press, mixer, basin | 1 |
| 3 | Brass & Precision | Brass, mechanical crafting, sequenced assembly, deployers | 2 |
| 4 | Heat | Blaze Burner → [[Blaze Burner Fuel Tiers]]: cake (T1) → biofuel (T2) → napalm (T3); [[Diamond Recipe]] | 3 |
| 5 | Logistics & Storage | Sophisticated Storage/Backpacks, Tom's Storage, contraption storage | 2 |
| 6 | Teleportation | Telejuice → [[Quantum Pearl]] / Quantum Paper / Quantum Casing → Waystones and scrolls; Create: Teleporters | 4 |
| 7 | Enchanting Industry | Create: Enchantment Industry (liquid XP, automated enchanting) | 4 |
| 8 | Artillery | Create Big Cannons → CBC More Shells, Firepower Components, Ballistic Computer | 3 |
| 9 | Aeronautics | Sable/Create Aeronautics: balloons, planes, Synaxis controls, Air War weapons | 3 |
| 10 | Radar & Missiles | Create: Radars network → CBC Aeronautics Missiles, Fire Arc Filter | 8, 9 |
| 11 | Naval | Create Deep Seas submarines, torpedoes (CBC Military Supplement) | 8 |
| 12 | Rail Warfare | Steam 'n' Rails, CBC Locometal Armor, train locking | 8 |
| 13 | Armored Vehicles | Armored Constructs, Bits 'n' Tracks treads, RHA armor | 8, 9 |
| 14 | Infantry | Create: Gunsmithing guns and ammo | 3 |
| 15 | Drones | Create: Droneworks Simulated, Air War FPV drone | 9 |
| 16 | Know Your Enemy | PvE threats: Trigger Mobs (armed mobs), Improved Mobs, Enhanced AI | 1 |

### Quest content rules
- **Layout: hub-and-spoke** (owner's reference screenshot, 2026-11-21; replaced the earlier grid). Each
  chapter has a main line of big **hub** quests (left → right). The side quests fan out around their
  hub on arcs above and below, each depending only on its hub. An "Age Complete" **gate** quest at the
  end requires a hand-picked list (e.g. the key automate quests) with **hidden dependency lines** so they
  don't cross the fans. Defined in the generator's `LAYOUTS` table, which places satellites
  automatically; the generator refuses to write files if quests overlap or a line passes through a quest.
  - Andesite Age: Find Andesite → **Andesite Alloy** hub (chain Shafts → Water Wheel → Large Water
    Wheel straight up; chain Cogwheels → Gearbox → Vertical Gearbox straight down) → **Andesite Casing** hub (basin/mixer, millstone; chain Kelp → Dried Kelp →
    Belts on the bottom spoke, with Andesite Tunnel branching off Dried Kelp; chain Press → Depot → **Iron Sheets**, which fans out to Gold Sheets, Mechanical Saw, Mechanical
    Harvester, Mechanical Drill, Encased Fan; Gold Sheets fans out to Wrench and Engineer's Goggles) → **Automation** hub →
    Andesite Age Complete. Side quests follow real recipe order (sheets before saw/drill/fan/tools).
  - Brass Age (rebuilt 2026-11-21 from Create 6.0.10's actual recipes): Empty Blaze Burner → Catch a
    Blaze → **Brass Ingot** hub (up: Rose Quartz → Polished Rose Quartz → Electron Tube, fanning to Brass
    Funnel + Brass Tunnel; down: Brass Sheets → Brass Hand) → **Brass Casing** hub (up: Deployer →
    Precision Mechanism, fanning to Mechanical Arm + Rotation Speed Controller; down: Mechanical Crafter)
    → **Automation** hub (Brass, Electron Tubes, Precision Mechanisms; Crushing Wheels → Ore Processing)
    → Brass Age Complete.
  - Heat Expansion: **Fuel Tiers** → **Blaze Cake** → **Biofuel** → **Automation** hubs.
- **Task types:** prefer `item` (obtain) and `checkmark` (read/acknowledge) tasks; `observation` for
  "look at this placed block" where obtaining an item doesn't prove understanding (e.g. a working
  superheated burner).
- **Descriptions** explain *why* and point out pack-specific changes. Every custom recipe gets a
  quest whose description states the recipe.
- **Rewards:** XP plus materials only. No gear, vehicles or anything that skips a tier. No currency, no
  loot crates.
- **XP (owner, 2026-11-21: "even higher and feel better overall"):** XP points ×4 on every quest
  (`XP_SCALE`), plus whole **levels** on milestones: main-line hub +2, automate quest +3, chapter finale +5,
  Age Complete +10 (`levels_for` in the generator). Whole book: 35,200 XP points + 301 levels.
- **Bonus rewards (owner, 2026-11-21):** every quest with item tasks also rewards a little of what it
  asked for: about ⅛ of the task amount, min 1, max 8 (generator `bonus_count`, per task; `bonus=False`
  on a quest turns it off). Exception to the v1 "no blaze cakes/diamonds as rewards" rule: the bonus
  only arrives after the player already made the item, so it can't skip a tier. Notable: Catch a Blaze
  gives back a filled Blaze Burner; Automate: Diamonds gives 8 diamonds.
- **Teams:** default FTB Quests team progress (one team completes it for everyone in the team).
- **Guide only:** quests never lock recipes or items. No gating mod. (Book progression *does* lock
  quests behind their dependencies since v2: `progression_mode: linear`.)
- **No PvP tasks:** no quest requires fighting or killing other players/teams.

## Commands
```
# Ship quest files (after authoring in-game or editing SNBT)
cp -r "<instance>/minecraft/config/ftbquests/quests" "pack/config/ftbquests/"
cd pack && packwiz refresh

# Sync pack -> Prism instance (client)
cd "<instance>/minecraft" && java -cp packwiz-installer.jar link.infra.packwiz.installer.Main -g -s client "file:///C:/Users/blake/OneDrive/Documents/GitHub/Create%20Wars/pack/pack.toml"

# Launch into world for testing
"C:/Users/blake/AppData/Local/Programs/PrismLauncher/prismlauncher.exe" --launch "Create Wars" --world "New World"

# Check logs after load
grep -iE "ftbquests|FTB Quests" "<instance>/minecraft/logs/latest.log" | grep -iE "error|warn|unknown|invalid"

# In game: toggle editor
/ftbquests editing_mode
```
`<instance>` = `C:/Users/blake/AppData/Roaming/PrismLauncher/instances/Create Wars`.

## Project structure
```
pack/config/ftbquests/quests/        → shipped quest book (source of truth once committed)
  data.snbt                          → book settings
  chapters/<chapter>.snbt            → one file per chapter (16 per the map above)
  reward_tables/*.snbt               → loot-crate style rewards, if used
  lang/en_us.snbt                    → text, if FTB Quests stores it separately in this version
vault/03-Design/Quest Book.md        → this spec + decisions log
vault/04-Changelog/Changelog.md      → one entry per shipped chapter batch
```

## Code style
FTB Quests SNBT, one quest per compound, readable titles, 16-hex-digit IDs as FTB Quests generates them:
```snbt
{
	id: "4A1C2E6F0B3D5A71"
	title: "Liquid Teleportation"
	description: ["Mix &dChorus Fruit&r with water over a &6heated&r burner to make &dTelejuice&r."]
	dependencies: ["2B7F0C1E9D4A6385"]
	tasks: [{ id: "6E2D4B1A8C3F5097", type: "item", item: "createteleporters:quantum_fluid_bucket" }]
	rewards: [{ id: "1F8A3C5E7B2D4069", type: "xp", xp: 50 }]
	x: 2.0d
	y: 0.0d
}
```
Conventions: chapter file names in snake_case; item IDs always namespaced; `&` formatting codes for
emphasis only (one color per concept: `&d` teleport/quantum, `&6` heat, `&c` combat).

## Testing strategy
No unit tests exist for a quest book. Verification is layered:
1. **Reference check (automated, before shipping):** a small script extracts every `item:` /
   `observation` ID from the SNBT and checks each exists among the pack's registered items (from mod
   jars' lang/registry data and `kubejs/startup_scripts`). Zero unknown IDs required. This catches the
   most common modpack quest bug: a quest pointing at an item that was renamed or removed (e.g. the
   removed Air War launchers, elytras, Mob Radar).
2. **Load check:** boot the instance into a world. `latest.log` has no FTB Quests errors and the book
   shows every chapter.
3. **Playthrough check (manual, owner):** per chapter, complete the first and last quests in a test world
   to confirm dependencies and rewards fire.
4. Every recipe a quest description states is checked against the actual JEI recipe (custom ones live
   in `pack/kubejs/server_scripts/`).

## Boundaries
- **Always:** use real item IDs verified against the installed jars; record each design choice in the
  decisions log; ship via `pack/config/ftbquests/` + `packwiz refresh`; boot-test before calling a
  chapter done.
- **Ask first:** adding a mod (e.g. a game-stages/recipe-locking mod for hard gating, or a currency mod
  for rewards); rewards that hand out combat gear, vehicles or anything that skips a progression tier;
  changing recipes to fit the book (the book should describe the pack, not reshape it); any quest that
  requires PvP actions (killing players).
- **Never:** reference items from removed or disabled mods; give rewards that bypass the
  [[Elytra Removal]] or the Telejuice-gated waystones; ship hand-edited SNBT without the reference
  check; hand-guess IDs.

## Success criteria
- [ ] All approved chapters exist in `pack/config/ftbquests/quests/` and ship through packwiz.
- [ ] Reference check reports **0** unknown item/block IDs.
- [ ] Instance boots into a world with **0** FTB Quests errors in `latest.log`.
- [ ] Every pack-specific mechanic (fuel tiers, diamond recipe, Quantum items, waystone recipe, no
      elytras, no wild waystones, Air War launcher removal) has a quest whose description is accurate
      to the current scripts.
- [ ] Each chapter's entry quest is reachable from chapter 1 through dependencies (no orphan chapters).
- [ ] The owner has completed the first and last quest of every chapter in a test world.

## Open questions
1. **Three steel ingots:** `createbigcannons:steel_ingot`, `tfmg:steel_ingot` and `cgs:steel_ingot` all
   exist. Recipes using the `c:ingots/steel` tag accept any of them, but CBC casting, TFMG's blast
   furnace and Gunsmithing's mixing each make their own. Unify with KubeJS (e.g. hide two and add
   conversions), or leave them?
1. **Warfare chapters:** still the flat draft list; settle before authoring them.

## Decisions log
- 2026-11-21: Spec drafted (owner ran `/spec-driven-development quests`). FTB Quests chosen as the
  platform because it's already in the pack and per-team progress fits FTB Teams factions.
- 2026-11-21: Owner answers: (1) **guide only**, no recipe gating; (2) rewards **XP + materials**;
  (3) chapter map **undecided** beyond v1; (4) **Claude authors the SNBT, owner reviews in game**;
  (5) **no PvP quests**; (6) **v1 = chapters 1–4** (Welcome, Kinetics, Brass & Precision, Heat).
- 2026-11-21: v1 built (chapters 1–4) via `tools/quests/build_quests.py` (generator = source of truth;
  IDs derived from slugs so regeneration keeps progress), validated by `tools/check_quest_refs.py`
  (unknown + pack-banned items). `progression_mode: flexible` so tasks count before dependencies
  (guide, not gate). Chapters chain: each chapter's first quest depends on the previous chapter's last.
- 2026-11-21: Owner review: removed "Know What's Removed" from Welcome.
- 2026-11-21: **Book structure v2 approved.** Owner: sections; Andesite → Brass → Industrial are *ages*
  (sequential, key Andesite quests unlock Brass); Heat, Quantum and Enchanting are *expansions* unlocked
  by Brass; automate quests want **one stack** made. Progression switched flexible → linear so unlocks
  are real in the book.
- 2026-11-21: Owner found the book "very clunky"; the cause was the layout only. Re-gridded all chapters
  (0 diagonal/crossing lines). Added the Andesite iron chain: Automate Iron Nuggets → **Iron Ingots** →
  **Iron Blocks** (press + basin compacting), hanging below the nugget quest; not required for Andesite
  Age Complete.
- 2026-11-21: Automate Iron Blocks lowered from a stack to **2** (owner: a stack = 5,184 nuggets, too
  grindy for the Andesite Age). Exception to the one-stack rule.
- 2026-11-21: Andesite Age now starts with **Find Andesite** (16 andesite) → Andesite Alloy (owner).
  Find Andesite is the chapter's entry quest (receives the Welcome unlock).
- 2026-11-21: Andesite Age main path reworked (owner): Find Andesite → Andesite Alloy → Shafts →
  Cogwheels → Water Wheel → Large Water Wheel → Press → … Cogwheels branches up into circle quests
  Gearbox → Vertical Gearbox. ("Shafts and Cogwheels" split; Shafts keeps the old slug/ID.)
- 2026-11-21: Owner: main progression after Alloy is **Casing**; shafts/cogs/water wheels are side objectives.
  Then owner shared a hub-and-spoke reference: whole book re-laid out that way (new "Automation" hub
  quest in each chapter). 61 quests.
- 2026-11-21: Water wheels moved onto a chain: Shafts → Water Wheel → Large Water Wheel (owner). Layout
  engine gained `chains` (quests extending a satellite outward along its spoke).
- 2026-11-21: Press chain (owner): Casing → Mechanical Press → Depot → Iron Sheets → Gold Sheets. Depot split
  out of "Belts and Depots" (now "Belts"; same slug). 64 quests.
- 2026-11-21: Owner: iron sheets unlock saw, drill and fan; gold sheets unlock wrench and goggles.
  "Saw and Drill" split (saw keeps the old slug), "Tools of the Trade" split into Wrench (old slug) and
  Engineer's Goggles. Layout engine gained `fans` (sub-branches off a spoke quest) and top/bottom
  satellite lists; spacing rule raised to 0.6 between quest edges. 66 quests.
- 2026-11-21: Iron automate quests merged (owner): **Automate: Iron** = stack of nuggets + stack of ingots +
  2 iron blocks, one quest (slug auto_iron). Iron Ingots / Iron Blocks quests removed. 64 quests.
- 2026-11-21: Removed "Automate: Crops" (wheat) from the Andesite Age (owner). 63 quests.
- 2026-11-21: Added Mechanical Harvester to the Iron Sheets fan (owner). Fans now grow their radius with
  quest count. 64 quests.
- 2026-11-21: Belts now come via a chain (owner): Casing → Kelp → Dried Kelp → Belts. 66 quests.
- 2026-11-21: Gearboxes chained off Cogwheels (owner): Cogwheels → Gearbox → Vertical Gearbox, on Alloy's
  bottom spoke.
- 2026-11-21: Bonus rewards added to all 54 item quests (owner): a little of what the quest asked for.
- 2026-11-21: Owner: gold sheets branch from the Press (not from Iron Sheets); Press and Depot merged into
  one quest ("Mechanical Press & Depot", slug press). Layout engine: fans accept (quests, offset, spread).
  Offsets chosen by searching for the first layout that passes the overlap/line check. 65 quests.
- 2026-11-21: Added Andesite Tunnel, branching off Dried Kelp (owner). 66 quests.
- 2026-11-21: Brass Age rebuilt in the Andesite style (owner). Dependencies follow the real recipes,
  read from the Create jar: electron tube = polished rose quartz + iron sheet; brass hand = brass sheet
  + alloy; deployer = andesite casing + brass hand + tube; precision mechanism via deployers; arm and
  speed controller need precision + brass casing; funnel/tunnel = brass + tube + dried kelp; crushing
  wheel is andesite-tier, so it now leads into Automate: Ore Processing. New quests: Rose Quartz, Brass
  Funnel, Brass Tunnel, Brass Sheets, Brass Hand, Mechanical Arm, Rotation Speed Controller. 73 quests.
- 2026-11-21: Automate: Iron now asks for **7** iron blocks (was 2; owner).
- 2026-11-21: Brass automate quests for Electron Tubes and Precision Mechanisms lowered to **5** each (owner).
  Exceptions to the one-stack rule, like Iron Blocks.
- 2026-11-21: **v3** (owner: "continue with this style"; "make an automation chapter... since the quest is
  more for guidance"). Automation chapter added; Industrial Age (TFMG), Quantum Expansion and
  Enchanting Expansion built; Heat slimmed. 8 chapters, 137 quests. Generator gained cross-chapter deps.
- 2026-11-21: v3 confirmed in game (`Loaded 5 chapter groups, 8 chapters, 137 quests`, no errors).
- 2026-11-21: Owner: diamonds only in Automation (Heat's "Diamonds from Coal" removed; Automate: Diamonds
  now states the coal-block recipe). Added **Automate: Netherite** (4 ingots, not a stack, because debris is
  non-renewable) to Heat Automation. Netherite recipe checked: vanilla 4 scrap + 4 gold (shapeless)
  plus debris smelting/blasting are present and untouched by any mod or script. Automatable with fan
  bulk blasting (lava) + Mechanical Crafters.
- 2026-11-21: Automation chapter tiers are now **separate bubbles** (owner): no line or dependency between
  tier hubs, laid out 2×3 (top: Andesite, Brass, Industrial; bottom: Heat, Quantum, Enchanting). Each tier
  hub is unlocked only by its own chapter's key quest (kinetics/casing, brass_and_precision/brass_casing,
  industrial/steel, heat/blaze_cake, quantum/telejuice, enchanting/liquid_xp). Layout engine: `connected=False`
  plus optional y on main entries; duplicate dependencies are dropped.
- 2026-11-21: **Warfare section** (owner: "expand into the other mods ... like weapons and radar"):
  Artillery, Infantry, Radar & Missiles in the hub-and-spoke style, from the jars' recipes. Cast CBC
  parts (barrels, breeches) have no crafting recipe (CBC casts them), so those quests point to the
  Ponder. 11 chapters, 226 quests. Still to do in Warfare: Aeronautics, Naval, Rail, Armored, Drones.
- 2026-11-21: Warfare finished: Aeronautics, Naval, Rail Warfare, Armored Vehicles, Drones. Item IDs all
  verified; for parts whose recipes weren't read, quest text describes function and points to JEI and
  the Ponder rather than guessing ingredients. XP raised (×4 points + level rewards). Boot-tested:
  `Loaded 6 chapter groups, 16 chapters, 334 quests`, 706 translations, no warnings, no file rewrites.
- 2026-11-21: **Infrastructure section** (owner: "add a food mod then do an infrastructure tab with
  food and storage"): added Farmer's Delight + Create: Slice & Dice; new Food and Storage chapters,
  unlocked from Welcome, recipe order read from the jars. Slicer/Packager also need Andesite Casing,
  Item Vault needs Iron Sheets (cross-chapter deps). Chapter renamed "Radar and Missiles" (a bare `&`
  breaks FTB text; see [[../02-Bugs/Quest titles break on ampersand]]). 18 chapters, 393 quests.
- 2026-11-21: Removed **Automate: Quantum Pearls** (owner: "dont really need quantum pearls automated"). Quantum
  Automation keeps Automate: Telejuice only. 392 quests.
- 2026-11-21: **Storage chapter v2** (owner): Tom's Simple Storage is *the* storage network. Dropped
  Create package logistics (Packager, Stock Ticker, Frogport and the rest), Fluid Tank and PSI, and the
  Sophisticated Controller/Link/I/O from the quests. **Quests only**: their recipes still work (owner
  chose not to disable them). Chest upgrade mod = Sophisticated Storage's chests + tier upgrades (copper ->
  netherite); no new mod added. Main line: Backpack -> Sophisticated Chest -> Chest Tier Upgrades -> Item
  Vault -> Inventory Connector -> Storage Terminal -> Crafting Terminal. 25 quests; book 386.
- 2026-11-21: **Demolitions chapter** (owner: "add those to the quests", meaning Warnautics). One chapter
  instead of splitting it across Aeronautics and Naval. Main line: Packed Guncotton -> Small Bomb -> Medium Bomb
  -> Large Bomb -> C4 -> Cruise Missile -> MOAB. Recipe order from the jar. Owner kept AIM-9, rocket pods
  and the cruise missile (they're quested), so they're not removed like the Air War launchers. 409 quests.
- 2026-11-21: **Pollution and Air** (Infrastructure) and **Know Your Enemy** (Warfare) chapters (owner: "then we
  need pollution and mobs quests"). Generator gained **kill tasks** (`kill(entity, n)`; format from
  `KillTask.writeData`: `entity` string + `value` long). `check_quest_refs.py` now also validates entity IDs
  (`entity.*` lang keys). Mob mods add no new mob types, so the kill tasks use vanilla mobs. Both
  respirators are quested with distinct titles (Air Respirator = Thick Air, Smog Respirator = Smog). PoTR's
  tools are not quested (disabled). 21 chapters, 460 quests.
- Possible later: AMBUSH's FTB Quests hook (quest tag `ambush:trigger:<id>` starts an ambush when the quest
  starts; tagged tasks can be auto-completed). Not used yet; needs specific ambush IDs and testing.
- 2026-11-21: **Portable Storage Interface** back in the book, in Rail Warfare (Train Controls hub) (owner
  approved the recommendation). Thick Air quest text updated to Y=192. Infantry steel quest now asks for
  TFMG steel ([[Steel Unification]]). Armored Hatch quest replaced with **Sandbags**
  ([[../02-Bugs/RHA hatch is not a registered item]]). `check_quest_refs.py` now uses the live registry export.
  Kill tasks confirmed: all 23 survived an in-game save of the book. 461 quests.
- 2026-11-21: **Raiding Party** quest (Know Your Enemy): first AMBUSH-triggered quest. Generator gained `tags=` on
  `Q()` (written as the `tags` string list). **Food Automation** hub in Automation (bread, cabbage leaves via
  Slicer, vegetable soup), needs `food/slicer`. 466 quests.

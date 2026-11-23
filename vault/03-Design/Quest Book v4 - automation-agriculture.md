---
tags: [design/progression, mc-version/1.21.1, loader/neoforge]
status: approved
---

# Spec: automation-agriculture

Module of [[Quest Book v4 - Capability Map]]. Parent spec: [[Quest Book]]. Depends on
[[Quest Book v4 - automation-breakout]] (Automation tab chapters + `id_chapter` override).

## Objective
Owner (2026-11-23):
- "more depth to the automation challenge like all the crops and meats then all the crafted foods bread
  sweet rolls also milk then maybe wool, leather, eggs and feathers, not all clumped together, like a Crop
  Automation circle then Food Automation and then Animal Product Automation"
- "crops should be all crops including the ones added via farmers delight, same thing with the crafted
  food including things like honey"
- On every Farmer's Delight food: "all of them, it is a challenge tier after all"

Today the Automation chapter has one **Food Automation** bubble with 3 quests. This module replaces it
with a full farming challenge: **every crop, every meat, every food item in the pack (vanilla, Create,
Crafts & Additions, Farmer's Delight), and the animal products**. Each one asks for a stack made by
machines.

## Structure: new **Agriculture** chapter in the Automation tab
Farming gets its own chapter in the **Automation** tab, alongside the tier chapters from
[[Quest Book v4 - automation-breakout]] (owner picked one chapter per tier). Inside it, the owner's three
circles, separate and in the owner's order:

```
 Crop Automation            Food Automation                          Animal Product Automation
 ├─ Crops fan (18)  ★       ├─ Fan Cooking (16) ★  ├─ Spout (8)    ★  └─ fan (5)
 └─ Meats fan (8)   ★       ├─ Slicer (9)       ★  ├─ Bakery (13)  ★
        ↓                   ├─ Mixing (27)      ★  ├─ Assembly (21)★       ↓
   ★★ Master Farmer         └─ Feasts (6)       ★                     ★★ Master Rancher
                                      ↓
                               ★★ Master Chef
                                      ↓ (all three ★★)
                            ★★★ Feed the Army
 ★ = sub-hub capstone   ★★ = circle capstone   ★★★ = chapter finale
```

### Rewards: hubs that feel worth the work
Owner (2026-11-23): "the hubs need to feel worth the work getting to them". Owner picked **completion
capstones**: the individual item quests stay small, and the big payout comes at the end of each group.
| Quest kind | Count | Needs | Reward |
|---|---|---|---|
| Item quest | 131 | its sub-hub | XP + **+1 level** (overrides the automate +3) + the usual ⅛ bonus |
| Hub / sub-hub entry (checkmark) | 3 + 9 | unlock / its circle hub | XP + 2 levels (normal hub) |
| **Sub-hub capstone** ★ | 9 | every item quest in that sub-hub | **levels = half the sub-hub's quest count (min 5)** + **1 Spoils of War II roll** (2 rolls if the sub-hub has 20+ quests) |
| **Circle capstone** ★★ | 3 | Master Farmer: Crops ★ + Meats ★; Master Chef: all 7 food ★; Master Rancher: all 5 animal products | **+15 levels** (Farmer, Rancher) / **+25 levels** (Chef), + **1 War Trophy roll** |
| **Chapter finale** ★★★ "Feed the Army" | 1 | all three ★★ | **+30 levels + 2 War Trophy rolls** |

Sub-hub capstone levels: Crops 9, Meats 5, Fan Cooking 8, Slicer 5, Mixing 14, Spout 5, Bakery 7,
Assembly 11, Feasts 5 = 69. **Chapter total ≈ 131 + 24 + 69 + 55 + 30 ≈ 310 levels.** That's big on
purpose: it's the largest challenge in the book (the Automation chapter today has 80; Defend Your Home
has 100). Capstone dependency lines are **hidden**, since they would cross every fan (same trick as the
Age Complete gates). Capstones sit at the outer edge of their fan. Capstone titles/icons are picked
during the build (e.g. "Mixing Mastered", icon = a signature dish).
- Food Automation's 100 quests are split into **7 method sub-hubs**, one per machine/recipe type, so the
  page reads as "learn this machine, then make everything it makes". Sub-hubs are checkmark quests that
  explain the machine, the same as the existing tier hubs.
- Chapter slug `agriculture`, title **Agriculture**. Chapter unlock = `kinetics/casing` (same as
  Automation).
- Hub unlocks (cross-chapter, not drawn):
  - Crop Automation ← `kinetics/harvester`
  - Food Automation ← `food/slicer` (unchanged)
  - Animal Product Automation ← `brass_and_precision/deployer` (Deployers milk cows and shear sheep;
    confirmed in game before a description says so)
- **Milk/egg rule:** a food quest whose *every* recipe needs milk or eggs (computed from the recipe
  export) also requires `auto_milk` / `auto_eggs`, with a hidden line. Today that's 15 items (e.g.
  sweet roll, chocolate, pie crust, fried rice, fried egg, wheat dough, shepherd's pie).

### Keeping progress on the 3 existing quests
`food_auto`, `auto_bread`, `auto_cabbage_leaf` and `auto_soup` move here and keep their IDs through the
`id_chapter="automation"` override added by [[Quest Book v4 - automation-breakout]]. Their rewards change
to the new scheme (+1 level instead of +3). Reward IDs don't depend on the amount, so already-claimed
rewards stay claimed and nothing can be claimed twice.

## Quest list
All 131 item IDs verified in the live registry export, and every food has at least one loaded recipe
(2026-11-23). One quest per item, slug `auto_<item path>`, title `Automate: <Name>`.

**Amounts:** owner rule (2026-11-23): "the automate tasks should require at min a full stack of the item".
Amount = at least the item's max stack size from the registry export (`max_stack`): 64 for stackables, 16 for
16-stackers (bowls, bottles, eggs), 16 for buckets, 8 for cakes and pies, 4 for feast blocks (all three stack to 1).
`audit_quests.py` STACK check enforces the minimum.

**Excluded on purpose:** pie, cake and roll *slices* (they come from cutting the whole item, which is
quested); feast *servings* (gleaming salad, roast chicken, etc. are served from the feast block, which
is quested); rotten tomato; non-food plants (cactus, bamboo, torchflower, pitcher plant).

| Group | Items |
|---|---|
| **Crops (18)** | wheat, carrot, potato, beetroot, sugar cane, melon slice, pumpkin, apple, cocoa beans, sweet berries, glow berries, nether wart; FD cabbage, tomato, onion, rice; brown and red mushroom (FD colonies) |
| **Meats (8)** | beef, porkchop, chicken, mutton, rabbit, cod, salmon; FD ham |
| **Fan Cooking (16)** | cooked beef / porkchop / chicken / mutton / rabbit / cod / salmon, baked potato; FD beef patty, cooked bacon, cooked chicken cuts, cooked mutton chops, cooked cod slice, cooked salmon slice, fried egg, smoked ham |
| **Slicer (9)** | FD cabbage leaf *(kept)*, minced beef, bacon, chicken cuts, mutton chops, cod slice, salmon slice, pumpkin slice, raw pasta |
| **Mixing (27)** | FD vegetable soup *(kept)*, tomato sauce, cooked rice, beef stew, chicken soup, fish stew, baked cod stew, bone broth, onion soup, pumpkin soup, noodle soup, vegetable noodles, fried rice, mushroom rice, cabbage rolls, dumplings, ratatouille, pasta with meatballs, pasta with mutton chop, squid ink pasta, glow berry custard, hot cocoa, apple cider, dog food; vanilla mushroom stew, beetroot soup, rabbit stew |
| **Spout (8)** | honey bottle, FD milk bottle, Create sweet roll, honeyed apple, chocolate glazed berries, builder's tea; C&A honey cake, chocolate cake |
| **Bakery (13)** | bread *(kept)*, FD wheat dough, Create bar of chocolate, FD pie crust, cookie, FD honey cookie, FD sweet berry cookie, pumpkin pie, cake, FD apple pie, FD chocolate pie, FD sweet berry cheesecake, FD melon popsicle |
| **Assembly (21)** | FD hamburger, bacon sandwich, chicken sandwich, egg sandwich, mutton wrap, bacon and eggs, steak and potatoes, roasted mutton chops, grilled salmon, stuffed potato, barbecue stick, mixed salad, fruit salad, nether salad, kelp roll, cod roll, salmon roll, melon juice, horse feed; golden carrot, golden apple |
| **Feasts (6)** | FD roast chicken, shepherd's pie, honey glazed ham, stuffed pumpkin, gleaming salad, rice roll medley (block items) |
| **Animal Products (5)** | milk bucket, white wool, leather, egg, feather |

The full ID list lives in the generator once built. The tasks are the namespaced IDs of the names above.

Each description says **how** to automate the item in this pack (machine + recipe), taken from the recipe
export or JEI, never from memory. Group sub-hub descriptions explain the machine once, so item
descriptions can stay one or two lines.

## Commands
```
python -I tools/quests/build_quests.py
python -I tools/check_quest_refs.py
python tools/audit_quests.py --instance "C:/Users/blake/AppData/Roaming/PrismLauncher/instances/Create Wars - Testing/minecraft"
cd pack && packwiz refresh
```
Close the game before syncing quest files to the instance, then verify with `cmp`.

## Project structure
- `tools/quests/build_quests.py`: new `agriculture` chapter in `CHAPTERS` (group `automation`);
  `LAYOUTS["agriculture"]`; capstones; the milk/egg rule. (`id_chapter` comes from automation-breakout.) Food quests are probably generated
  from a data table rather than written out as 131 hand-written `Q(...)` calls.
- `pack/config/ftbquests/quests/chapters/agriculture.snbt` (new), `automation.snbt` (food bubble
  removed), `lang/en_us.snbt`.
- `vault/03-Design/Quest Book.md`: decisions log entry.

## Code style
Match the existing automate quests:
```python
Q("auto_sweet_roll", "Automate: Sweet Rolls", 0, 0, [
    "Run bread under a &aSpout&r filled with milk. Make a &astack&r.",
], [item("create:sweet_roll", STACK)], xp=50),
```

## Testing strategy
1. Generator: no overlap or line-crossing errors (it refuses to write otherwise).
2. `check_quest_refs.py`: 0 unknown IDs.
3. `audit_quests.py`: 0 HIDDEN, 0 ORDER gaps. Any new NO RECIPE entry is a crop or mob drop.
4. ID check: `food_auto`, `auto_bread`, `auto_cabbage_leaf`, `auto_soup` have the same IDs (quest, task,
   reward) as in the current `automation.snbt`.
5. Boot: 0 FTB Quests errors. Owner looks at the chapter in game.

## Boundaries
- Always: verify IDs and recipes against the live export; keep the 4 existing IDs; log in the decisions log.
- Ask first: adding mods or recipes to make something automatable; changing XP constants.
- Never: hand-guess IDs; edit generated SNBT by hand.

## Success criteria
- [ ] Automation tab holds an **Agriculture** chapter with three separate circles, in this order: Crop,
      Food (7 method sub-hubs), Animal Products.
- [ ] 26 crop/meat, 100 food, 5 animal product quests with the tasks above.
- [ ] 9 sub-hub capstones, 3 circle capstones and the Feed the Army finale, with the rewards in the
      table. Each capstone can only be completed once everything it covers is done.
- [ ] Existing progress on the 4 moved quests is kept.
- [ ] The milk/egg rule is applied from the recipe export (as a description note; see Decisions 2026-11-23 in-game review).
- [ ] Ref check 0 unknown; audit 0 hidden / 0 order gaps; clean boot.
- [ ] Every description's recipe matches JEI.

## Decisions
- 2026-11-23: all crops (vanilla + FD); every food item, including all of Farmer's Delight (owner: "all
  of them, it is a challenge tier after all").
- 2026-11-23 (default, owner didn't object): food that needs milk or eggs requires the matching animal
  product quest, with a hidden line.
- 2026-11-23: farming is its own **Agriculture** chapter in the **Automation** tab (owner: bring back
  the Automation tab and break it into one chapter per tier).
- 2026-11-23: rewards = small item quests (+1 level) and big **completion capstones** (owner: "the hubs
  need to feel worth the work getting to them").

- 2026-11-23 (owner in-game review: "some of the mixing ones are missing connection lines"): the milk/egg
  requirement is **no longer a hard dependency**. FTB hides all of a quest's lines or none, so the 25 quests lost their
  line to their group. They now only say "Needs milk/eggs from Animal Product Automation" in the description.

## Open questions
None blocking. Capstone names and icons are chosen during the build, and the owner can rename them in review.

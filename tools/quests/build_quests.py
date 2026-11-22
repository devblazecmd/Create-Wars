"""Generate the Create Wars FTB Quests book (FTB Quests 2101.x, file version 13).

Usage:
    python -I tools/quests/build_quests.py            # writes pack/config/ftbquests/quests/
    python -I tools/check_quest_refs.py               # then validate item references

This file is the SOURCE OF TRUTH for the quest book. Edits made in the in-game editor are overwritten
the next time this runs, so port any in-game tweaks (positions, wording) back here.

IDs are derived from stable slugs (sha1 -> 63-bit), so regenerating keeps team progress. Never rename a
chapter/quest slug of a shipped quest unless you intend to reset its progress.

Format notes (from FTB Quests 2101.1.39 bytecode, 2026-11-21):
  * text lives in lang/en_us.snbt as "<type>.<ID>.<key>" (keys: title, quest_subtitle, quest_desc,
    chapter_subtitle), not inline in chapter files
  * items/icons are ItemStack compounds {id, count}; ItemTask.count is a long
  * task/reward "type" is the bare path for ftbquests' own types ("item", "checkmark", "xp")
  * ItemReward amount is a separate "count" (int); ItemTask amount is "count" (long, e.g. 4L)
  * the game sorts keys and re-saves files it considers non-canonical; output here matches its format
Spec: vault/03-Design/Quest Book.md   Plan: vault/03-Design/Quest Book - Plan.md
"""
import hashlib
import math
import os


REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "pack", "config", "ftbquests", "quests")
FILE_VERSION = 13


def qid(*parts):
    h = int.from_bytes(hashlib.sha1("/".join(parts).encode()).digest()[:8], "big") & 0x7FFFFFFFFFFFFFFF
    return f"{max(h, 2):016X}"


# --------------------------------------------------------------------------------------------------
# Content helpers
# --------------------------------------------------------------------------------------------------
def Q(slug, title, x, y, desc, tasks, deps=(), xp=10, items=(), subtitle=None, icon=None, shape=None,
      size=None, optional=False, bonus=True, tags=(), levels=None, rolls=()):
    # tags: FTB Quests object tags (QuestObjectBase writes "tags" as a string list when non-empty).
    # Used by AMBUSH: "ambush:trigger:<id>" starts that ambush when the quest is started.
    return dict(slug=slug, title=title, x=x, y=y, desc=desc, tasks=tasks, deps=list(deps), xp=xp,
                items=list(items), subtitle=subtitle, icon=icon, shape=shape, size=size, optional=optional,
                bonus=bonus, tags=list(tags), levels=levels, rolls=list(rolls))
    # levels: override the role-based whole-level bonus (levels_for).
    # rolls: [(reward_table_slug, times)] -> that many FTB "random" rewards rolling REWARD_TABLES[slug].


def bonus_count(task_count):
    """Owner (2026-11-21): every quest also rewards a little of what it asked you to make.
    About 1/8 of the task amount, at least 1, at most 8."""
    return max(1, min(8, task_count // 8))


def item(i, count=1):
    return ("item", i, count)


CHECK = ("checkmark", None, 0)


def kill(entity, count=1):
    """FTB Quests kill task: kill `count` of entity type `entity`."""
    return ("kill", entity, count)

# Formatting: &d teleport/quantum, &6 heat, &c combat/rules, &a tips, &r reset

# Sections (FTB Quests chapter groups), in sidebar order. Spec: "Book structure v2".
GROUPS = [
    ("getting_started", "Getting Started"),
    ("ages", "Ages"),
    ("expansions", "Expansions"),
    ("infrastructure", "Infrastructure"),   # owner 2026-11-21: food + storage
    ("warfare", "Warfare"),
    ("automation", "Automation"),
]

# A "stack" for automate quests (spec v2: automate = make one stack). 16-stackers get 16.
STACK = 64
STACK16 = 16

# XP (owner 2026-11-21: "even higher and feel better overall"). Every quest's XP points are scaled, and
# milestones also grant whole levels, which feel much better than raw points.
XP_SCALE = 4
LEVELS_HUB = 2        # main-line hub quests
LEVELS_AUTOMATE = 3   # automate quests (the grind)
LEVELS_FINALE = 5     # last main-line quest of a chapter
LEVELS_GATE = 10      # Age Complete gates

# Reward tables for random rolls (owner 2026-11-21: Defend Your Home waves should have "good xp gains and
# random rewards to feel worth it"). (item, count, weight). Every ID checked against the live registry.
REWARD_TABLES = {
    "war_spoils_1": dict(title="Spoils of War I", entries=[
        ("minecraft:iron_ingot", 16, 10), ("minecraft:gold_ingot", 8, 8), ("create:andesite_alloy", 32, 8),
        ("minecraft:cooked_beef", 16, 8), ("minecraft:arrow", 32, 6), ("minecraft:emerald", 6, 5),
        ("minecraft:experience_bottle", 8, 4), ("minecraft:golden_apple", 2, 3), ("thick_air:air_bladder", 1, 3),
        ("minecraft:totem_of_undying", 1, 1)]),
    "war_spoils_2": dict(title="Spoils of War II", entries=[
        ("minecraft:iron_block", 4, 10), ("create:brass_ingot", 16, 8), ("tfmg:steel_ingot", 8, 8),
        ("createbigcannons:powder_charge", 8, 7), ("createbigcannons:he_shell", 4, 6),
        ("farmersdelight:hamburger", 8, 6), ("createbigcannons:impact_fuze", 4, 5),
        ("create:precision_mechanism", 2, 5), ("minecraft:experience_bottle", 16, 5),
        ("minecraft:golden_apple", 4, 3), ("minecraft:diamond", 2, 2), ("minecraft:totem_of_undying", 1, 2)]),
    "war_spoils_3": dict(title="Spoils of War III", entries=[
        ("tfmg:steel_ingot", 24, 8), ("createbigcannons:he_shell", 8, 8), ("createbigcannons:ap_shell", 6, 6),
        ("createbigcannons:ap_autocannon_round", 16, 6), ("createbigcannons:packed_guncotton", 8, 6),
        ("createbigcannons:proximity_fuze", 4, 5), ("cbc_more_content:small_bomb", 4, 5),
        ("create:precision_mechanism", 6, 5), ("minecraft:experience_bottle", 32, 5), ("minecraft:diamond", 4, 4),
        ("cbc_more_content:c4", 2, 3), ("minecraft:netherite_scrap", 2, 3), ("minecraft:totem_of_undying", 1, 3),
        ("minecraft:enchanted_golden_apple", 1, 1)]),
    "war_trophy": dict(title="War Trophy", entries=[
        ("minecraft:netherite_ingot", 1, 3), ("minecraft:enchanted_golden_apple", 2, 3),
        ("minecraft:totem_of_undying", 2, 3), ("minecraft:diamond", 16, 3), ("minecraft:netherite_scrap", 8, 2),
        ("createwars:quantum_pearl", 8, 2)]),
}

CHAPTERS = [
    # ----------------------------------------------------------------------------------------------
    dict(slug="welcome", group="getting_started", title="Welcome to the War",
         subtitle="Start here: the rules of this pack", icon="ftbquests:book", unlock=[], quests=[
        Q("welcome", "Welcome to Create Wars", 0, 0, [
            "Create Wars is a &6Create&r pack about building a faction that can &cfight&r: aircraft, artillery,",
            "radar-guided missiles, armored trains and submarines.",
            "",
            "This book is a &aguide&r: it never locks recipes or items. Chapters open up as you finish",
            "earlier ones: the &6Ages&r in order, then the &6Expansions&r once you reach the Brass Age.",
        ], [CHECK], xp=10, shape="gear", size=1.5, subtitle="Open the book. You did it."),
        Q("team", "Form a Team", 2, 0, [
            "Factions are &aFTB Teams&r. Quest progress is shared by everyone on your team.",
            "",
            "Create a party from the FTB Teams button in your inventory, or with",
            "&a/ftbteams party create <name>&r, then invite your teammates.",
        ], [CHECK], deps=["welcome"], xp=10, items=[("minecraft:bread", 8)]),
        Q("claims", "Claim Your Base", 4, 0, [
            "Protect your base with &aFTB Chunks&r. Open the claim map from the FTB buttons in your",
            "inventory and drag across chunks to claim them for your team.",
            "",
            "Claimed chunks stop other teams breaking or using your blocks.",
        ], [CHECK], deps=["team"], xp=10, items=[("minecraft:torch", 16)]),
        Q("no_elytra", "No Elytras", 6, 0, [
            "&cElytras are disabled.&r End ships no longer carry one, and gliding is blocked even if",
            "you find one.",
            "",
            "If you want to fly, build an aircraft with &6Create Aeronautics&r.",
        ], [CHECK], deps=["claims"], xp=10),
        Q("waystones", "Waystones Are Built, Not Found", 8, 0, [
            "&cWaystones don't generate&r in the world or in villages. You have to craft them, and every",
            "waystone recipe runs on &dTelejuice&r: Quantum Pearls, Quantum Casings and Quantum Paper.",
            "",
            "You'll learn to make it in the &dQuantum Expansion&r.",
        ], [CHECK], deps=["no_elytra"], xp=10),
        Q("ultimine", "Vein Mining", 0, 0, [
            "&6FTB Ultimine&r: hold the &aUltimine key&r (default &a`&r, the grave key; change it in",
            "Controls) and break a block to mine up to &a64&r connected blocks of the same kind: a whole",
            "ore vein or tree. Costs hunger per block. Hold it and right-click to harvest crops, strip",
            "logs or till soil in bulk.",
        ], [CHECK], xp=10),
        Q("lootr", "Loot Is Per Player", 0, 0, [
            "&6Lootr&r: structure chests (villages, outposts, forts, ruins) give &aevery player their own",
            "loot&r. A chest someone else opened still has a roll for you. Opened chests change look.",
        ], [CHECK], xp=10),
        Q("next", "Start Building", 10, 0, [
            "Everything starts with rotation. Head to the &6Andesite Age&r.",
        ], [CHECK], deps=["waystones"], xp=20, items=[("minecraft:oak_log", 16)], shape="hexagon"),
    ]),
    # ----------------------------------------------------------------------------------------------
    dict(slug="kinetics", group="ages", title="Andesite Age",
         subtitle="Rotation, your first machines, your first automation", icon="create:andesite_alloy",
         unlock=[("welcome", "next")], quests=[
        # first in list = receives the chapter unlock (welcome/next)
        Q("find_andesite", "Find Andesite", -2, 0, [
            "Everything in Create starts with &aandesite&r: the gray stone found in big patches",
            "underground and in hillsides. Mine some.",
        ], [item("minecraft:andesite", 16)], xp=10, shape="gear", size=1.25),
        Q("andesite_alloy", "Andesite Alloy", 0, 0, [
            "The first Create material. Combine &aandesite&r with &airon nuggets&r (or zinc nuggets).",
            "Check &aJEI&r for the recipe: press &aU&r on an item to see how it's made.",
        ], [item("create:andesite_alloy", 4)], deps=["find_andesite"], xp=10,
            items=[("minecraft:iron_ingot", 2)]),
        Q("wrench_goggles", "Wrench", 0, 0, [
            "Made with a gold sheet. The &aWrench&r rotates Create blocks, and sneak-using it picks",
            "them up instantly.",
        ], [item("create:wrench")], deps=["gold_sheets"], xp=10),
        Q("goggles", "Engineer's Goggles", 0, 0, [
            "Made with a gold sheet. Wear &aEngineer's Goggles&r to see stress, speed and contents",
            "when you look at machines.",
        ], [item("create:goggles")], deps=["gold_sheets"], xp=10),
        Q("shafts_cogs", "Shafts", 0, -2, [
            "Andesite Alloy makes &aShafts&r: they carry rotation in a straight line from one machine",
            "to the next.",
        ], [item("create:shaft", 8)], deps=["andesite_alloy"], xp=10),
        Q("cogwheels", "Cogwheels", 0, -4, [
            "&aCogwheels&r pass rotation sideways to other cogs. Pairing a &alarge&r and a &asmall&r",
            "cogwheel doubles or halves the speed.",
        ], [item("create:cogwheel", 4), item("create:large_cogwheel", 2)], deps=["shafts_cogs"], xp=10),
        # gearbox branch: circles straight above Cogwheels (owner request)
        Q("gearbox", "Gearbox", -2, -4, [
            "A &aGearbox&r turns rotation 90 degrees in any horizontal direction, and is more compact",
            "than a cog pair.",
        ], [item("create:gearbox", 2)], deps=["cogwheels"], xp=10, shape="circle"),
        Q("vertical_gearbox", "Vertical Gearbox", -4, -4, [
            "Same idea, turned on its side: a &aVertical Gearbox&r sends rotation up or down.",
        ], [item("create:vertical_gearbox", 2)], deps=["gearbox"], xp=10, shape="circle"),
        Q("water_wheel", "Water Wheel", 2, -4, [
            "A &aWater Wheel&r turns when water flows past it. It's your first source of",
            "&6stress capacity&r (SU). Every machine uses some; the goggles show how much is left.",
        ], [item("create:water_wheel", 2)], deps=["cogwheels"], xp=15, items=[("create:andesite_alloy", 8)]),
        Q("large_water_wheel", "Large Water Wheel", 4, -4, [
            "Bigger wheel, more power: a &aLarge Water Wheel&r gives far more stress capacity, at a",
            "slower speed. Gear it up with a large-to-small cogwheel pair.",
        ], [item("create:large_water_wheel")], deps=["water_wheel"], xp=20),
        Q("millstone", "Millstone", 4, -2, [
            "Grinds items: gravel to flint, flowers to dye, and more. Look up any item in JEI under",
            "&aMilling&r.",
        ], [item("create:millstone")], deps=["press"], xp=10),
        Q("press", "Mechanical Press and Depot", 4, 0, [
            "The &aMechanical Press&r flattens ingots into sheets and compacts items in a &aBasin&r.",
            "Put a &aDepot&r under it to hold what it's pressing.",
        ], [item("create:mechanical_press"), item("create:depot")], deps=["casing"], xp=15, items=[("minecraft:iron_ingot", 4)]),
        Q("basin_mixer", "Basin and Mixer", 6, 0, [
            "A &aBasin&r holds ingredients; a &aMechanical Mixer&r above it mixes them, and a Press",
            "above it compacts them. Many recipes need &6heat&r from a burner under the basin; you'll",
            "get there in the next two chapters.",
        ], [item("create:basin"), item("create:mechanical_mixer")], deps=["press"], xp=15),
        Q("fan", "Encased Fan", 6, -2, [
            "Blowing through &alava&r smelts items, &awater&r washes them, &afire&r smokes them. A fan",
            "is the cheapest way to process in bulk.",
        ], [item("create:encased_fan")], deps=["iron_sheets"], xp=15),
        # chain off Casing's bottom spoke (owner): kelp -> dried kelp -> belts
        Q("kelp", "Kelp", 0, 0, [
            "Belts are made from &adried kelp&r. Gather &akelp&r from any ocean.",
        ], [item("minecraft:kelp", 32)], deps=["casing"], xp=10),
        Q("dried_kelp", "Dried Kelp", 0, 0, [
            "Cook kelp in a furnace, smoker or on a campfire. Later, an &aEncased Fan&r blowing",
            "through fire does it in bulk.",
        ], [item("minecraft:dried_kelp", 32)], deps=["kelp"], xp=10),
        Q("tunnel", "Andesite Tunnel", 0, 0, [
            "Andesite alloy and dried kelp make an &aAndesite Tunnel&r: put it over a belt to cover it",
            "and split items off to the sides.",
        ], [item("create:andesite_tunnel", 2)], deps=["dried_kelp"], xp=10),
        Q("belts", "Belts", 8, 0, [
            "Dried kelp makes &aBelts&r, which move items between machines. Place a belt by using",
            "it on two shafts.",
        ], [item("create:belt_connector", 4)], deps=["basin_mixer"], xp=15),
        # chain off Press (owner): press -> depot -> iron sheets -> gold sheets
        Q("iron_sheets", "Iron Sheets", 0, 0, [
            "Put &airon ingots&r on the Depot and let the Press flatten them into &aIron Sheets&r.",
        ], [item("create:iron_sheet", 8)], deps=["press"], xp=15, items=[("minecraft:iron_ingot", 8)]),
        Q("gold_sheets", "Gold Sheets", 0, 0, [
            "Press &agold ingots&r into &aGolden Sheets&r: they make the Wrench and Goggles, and go into",
            "precision parts later.",
        ], [item("create:golden_sheet", 4)], deps=["press"], xp=15),
        Q("casing", "Andesite Casing", 2, 0, [
            "Casings make machines tidy and are an ingredient in many recipes, including &dwaystones&r.",
        ], [item("create:andesite_casing", 4)], deps=["andesite_alloy"], xp=15),
        Q("saw_drill", "Mechanical Saw", 0, 0, [
            "Made with iron sheets. A &aMechanical Saw&r cuts trees and processes wood; put it on a",
            "moving contraption to build a tree farm.",
        ], [item("create:mechanical_saw")], deps=["iron_sheets"], xp=15),
        Q("harvester", "Mechanical Harvester", 0, 0, [
            "Made with an iron sheet. A &aMechanical Harvester&r on a moving contraption harvests",
            "fully grown crops and replants them: the basis of any farm.",
        ], [item("create:mechanical_harvester")], deps=["iron_sheets"], xp=15),
        Q("drill", "Mechanical Drill", 0, 0, [
            "Made with iron sheets. A &aMechanical Drill&r mines whatever is in front of it: the heart",
            "of cobblestone generators and tunnel borers.",
        ], [item("create:mechanical_drill")], deps=["iron_sheets"], xp=15),
        # --- automate (one stack each) ---
        # owner: one iron quest with all three steps (nuggets -> ingots -> blocks)
        Q("next", "Andesite Age Complete", 10, 2, [
            "You've built the core Andesite machines. This &aunlocks the Brass Age&r, and the",
            "&6Automation&r chapter has goals for putting these machines to work.",
            "",
            "&7Requires: Press and Depot, Basin and Mixer, Belts and Iron Sheets.&r",
            "",
            "Next up: you'll need a captured &cBlaze&r to make brass.",
        ], [CHECK], deps=["auto_cobble"], xp=50,
            items=[("create:zinc_ingot", 16)], shape="hexagon", size=1.5),
    ]),
    # ----------------------------------------------------------------------------------------------
    dict(slug="brass_and_precision", group="ages", title="Brass Age",
         subtitle="Heated mixing, brass, precision parts and ore processing", icon="create:brass_ingot",
         unlock=[("kinetics", "next")], quests=[
        # --- main line ---
        Q("empty_burner", "Empty Blaze Burner", 0, 0, [
            "Brass needs &6heat&r, and heat comes from a &aBlaze Burner&r. Craft an",
            "&aEmpty Blaze Burner&r from &airon sheets&r and &anetherrack&r.",
        ], [item("create:empty_blaze_burner")], xp=15),
        Q("blaze", "Catch a Blaze", 0, 0, [
            "Find a &cBlaze&r (a Nether fortress blaze spawner is ideal) and use the Empty Blaze Burner",
            "on it to capture it.",
            "",
            "Feed it fuel (coal, logs) and it heats a Basin above it: &6Heated&r.",
        ], [item("create:blaze_burner")], xp=30, items=[("minecraft:coal", 16)]),
        Q("brass", "Brass Ingot", 0, 0, [
            "Mix &acopper&r and &azinc&r in a Basin over a lit Blaze Burner.",
        ], [item("create:brass_ingot", 4)], xp=20, items=[("minecraft:copper_ingot", 8)]),
        Q("brass_casing", "Brass Casing", 0, 0, [
            "Use a &abrass ingot&r on a &astripped log&r (or stripped wood). The casing for Create's",
            "advanced machines.",
        ], [item("create:brass_casing", 2)], xp=15),
        # --- off Brass Ingot, up: rose quartz -> polished -> electron tube -> funnel / tunnel ---
        Q("rose_quartz_raw", "Rose Quartz", 0, 0, [
            "Craft &aQuartz&r with &aredstone dust&r to make &aRose Quartz&r.",
        ], [item("create:rose_quartz", 4)], xp=10),
        Q("rose_quartz", "Polished Rose Quartz", 0, 0, [
            "Polish rose quartz with &aSandpaper&r (hold use), or let a Deployer holding sandpaper do it.",
        ], [item("create:polished_rose_quartz", 2)], xp=15),
        Q("electron_tube", "Electron Tube", 0, 0, [
            "&aPolished Rose Quartz&r on an &aIron Sheet&r: the 'circuit' of Create machines.",
        ], [item("create:electron_tube", 2)], xp=15),
        Q("brass_funnel", "Brass Funnel", 0, 0, [
            "Brass ingot, electron tube and dried kelp. Like an andesite funnel, but it can &afilter&r",
            "and move whole stacks.",
        ], [item("create:brass_funnel", 2)], xp=10),
        Q("brass_tunnel", "Brass Tunnel", 0, 0, [
            "Same ingredients as the funnel. Put it over a belt to &asplit, filter and balance&r items",
            "across belts.",
        ], [item("create:brass_tunnel", 2)], xp=10),
        # --- off Brass Ingot, down: brass sheets -> brass hand ---
        Q("brass_sheets", "Brass Sheets", 0, 0, [
            "Press brass ingots into &aBrass Sheets&r on a Depot, like iron and gold.",
        ], [item("create:brass_sheet", 4)], xp=10),
        Q("brass_hand", "Brass Hand", 0, 0, [
            "A &abrass sheet&r and &aandesite alloy&r. The business end of a Deployer.",
        ], [item("create:brass_hand")], xp=15),
        # --- off Brass Casing, up: deployer -> precision mechanism -> arm / speed controller ---
        Q("deployer", "Deployer", 0, 0, [
            "&aAndesite Casing&r, a &aBrass Hand&r and an &aElectron Tube&r. A Deployer uses items like",
            "a player (placing, clicking, applying), and it's the key machine for sequenced assembly.",
        ], [item("create:deployer")], xp=20),
        Q("precision", "Precision Mechanism", 0, 0, [
            "Made by &aSequenced Assembly&r: a &agolden sheet&r passes Deployers adding cogwheels, large",
            "cogwheels and iron nuggets, in a loop. JEI shows each step.",
        ], [item("create:precision_mechanism")], xp=30, items=[("minecraft:gold_nugget", 16)]),
        Q("mech_arm", "Mechanical Arm", 0, 0, [
            "Brass casing, a precision mechanism, brass sheets and andesite alloy. An Arm picks items",
            "up and drops them into machines, depots and chests in range.",
        ], [item("create:mechanical_arm")], xp=25),
        Q("speed_controller", "Rotation Speed Controller", 0, 0, [
            "Brass casing and a precision mechanism. Sets the exact &aRPM&r of whatever it feeds.",
        ], [item("create:rotation_speed_controller")], xp=20),
        # --- off Brass Casing, down ---
        Q("crafter", "Mechanical Crafter", 0, 0, [
            "&aBrass Casing&r, an &aElectron Tube&r and a crafting table. Place several in a grid, connect",
            "them with the wrench, and power them to craft recipes bigger than 3x3. The &dwaystone&r",
            "recipes in this pack use them.",
        ], [item("create:mechanical_crafter", 4)], xp=25),
        # --- automation ---
        Q("next", "Brass Age Complete", 0, 0, [
            "You've mastered brass. This &aunlocks the Industrial Age&r and all three &6Expansions&r:",
            "Heat, Quantum and Enchanting.",
            "",
            "&7Requires: Electron Tube, Deployer, Precision Mechanism and Mechanical Crafter.&r",
        ], [CHECK], xp=75, items=[("create:zinc_ingot", 16), ("minecraft:copper_ingot", 16)], shape="hexagon"),
    ]),
    # ----------------------------------------------------------------------------------------------
    # Copper Expansion (owner 2026-11-22: "we need copper expansion"). Create's copper tier (fluids and steam)
    # plus Create Crafts and Additions' copper wiring (electricity). Recipes read from the live recipe export.
    dict(slug="copper", group="expansions", title="Copper Expansion",
         subtitle="Fluids, steam power and electricity", icon="create:fluid_tank",
         unlock=[("kinetics", "next")], quests=[
        Q("copper_sheet", "Copper Sheets", 0, 0, [
            "Copper is Create's &6fluid&r metal. Press copper ingots on a Depot, like iron sheets.",
        ], [item("create:copper_sheet", 16)], xp=15),
        Q("copper_casing", "Copper Casing", 0, 0, [
            "Right-click a stripped log or wood with a copper ingot. The shell of every fluid machine.",
        ], [item("create:copper_casing", 8)], xp=25),
        Q("item_drain", "Item Drain", 0, 0, [
            "Copper casing and iron bars. Empties buckets, bottles and potions dropped on it into the",
            "pipes below.",
        ], [item("create:item_drain")], xp=20),
        Q("fluid_hatch", "Fluid Hatch", 0, 0, [
            "&6Create: Dragons Plus&r: an item drain and a copper ingot. A drain that works on",
            "contraptions.",
        ], [item("create_dragons_plus:fluid_hatch")], xp=15),
        Q("hose_pulley", "Hose Pulley", 0, 0, [
            "Copper casing, a copper sheet and a dried kelp block. Lowers a hose to drain a lake or",
            "lava pool, or to fill one. Large bodies of water never run dry.",
        ], [item("create:hose_pulley")], xp=25),
        Q("portable_fluid_interface", "Portable Fluid Interface", 0, 0, [
            "Copper casing and a chute. Pumps fluids in and out of tanks on a moving contraption.",
        ], [item("create:portable_fluid_interface", 2)], xp=20),
        Q("fluid_pipe", "Fluid Pipe", 0, 0, [
            "A copper sheet and copper ingots. Pipes connect tanks and machines. They carry nothing on",
            "their own: they need a pump.",
        ], [item("create:fluid_pipe", 16)], xp=20),
        Q("mechanical_pump", "Mechanical Pump", 0, 0, [
            "A fluid pipe and a cogwheel. Give it rotation and it pushes fluid along the pipe. Faster",
            "rotation pumps more.",
        ], [item("create:mechanical_pump", 2)], xp=25),
        Q("fluid_valve", "Fluid Valve", 0, 0, [
            "A fluid pipe and an iron sheet. Opens and closes a pipe when you turn it.",
        ], [item("create:fluid_valve")], xp=15),
        Q("copper_valve_handle", "Valve Handle", 0, 0, [
            "A copper sheet and andesite alloy. Turns a valve, or anything else, a set amount.",
        ], [item("create:copper_valve_handle")], xp=10),
        Q("smart_fluid_pipe", "Smart Fluid Pipe", 0, 0, [
            "A fluid pipe, brass sheet and electron tube: a pipe with a filter that only lets one",
            "fluid through. &eNeeds the Brass Age.&r",
        ], [item("create:smart_fluid_pipe")], xp=25),
        Q("fluid_tank", "Fluid Tank", 0, 0, [
            "Copper sheets and a barrel. Tanks join into bigger tanks when placed next to each other.",
            "A tall tank is also the body of a &6steam boiler&r.",
        ], [item("create:fluid_tank", 4)], xp=30),
        Q("fluid_vessel", "Fluid Vessel", 0, 0, [
            "&6Create: Connected&r: copper sheets and a barrel. A sideways tank. Converts to and from a",
            "Fluid Tank in the crafting grid.",
        ], [item("create_connected:fluid_vessel", 2)], xp=15),
        Q("fragile_fluid_tank", "Fragile Fluid Tank", 0, 0, [
            "&6Dragons Plus&r: copper sheets, gold and a barrel. A tank that keeps its fluid when you",
            "break it.",
        ], [item("create_dragons_plus:fragile_fluid_tank")], xp=20),
        Q("steam_engine", "Steam Engine", 0, 0, [
            "A copper block, a gold sheet and andesite alloy. Build a &6boiler&r: a Fluid Tank with lit",
            "&aBlaze Burners&r underneath and water pumped in, then put Steam Engines on its sides and",
            "a shaft on each. A bigger tank and more heat run more engines. Look at the tank with",
            "goggles to see its level.",
        ], [item("create:steam_engine", 2)], xp=60),
        Q("steam_whistle", "Steam Whistle", 0, 0, [
            "Copper and a gold sheet. Put it on a boiler; redstone blows it. Taller stacks play lower.",
        ], [item("create:steam_whistle")], xp=10),
        Q("rolling_mill", "Rolling Mill", 0, 0, [
            "&6Create Crafts and Additions&r electricity starts here. Andesite casing, andesite alloy, iron",
            "sheets and a shaft. Rolls ingots into rods and sheets into wire.",
        ], [item("createaddition:rolling_mill")], xp=30),
        Q("copper_rod", "Copper Rod", 0, 0, [
            "Roll a copper ingot.",
        ], [item("createaddition:copper_rod", 4)], xp=10),
        Q("connector", "Connector", 0, 0, [
            "A copper rod, andesite alloy and slime. Wire runs between connectors: put them on",
            "generators, motors and batteries.",
        ], [item("createaddition:connector", 4)], xp=15),
        Q("capacitor", "Capacitor", 0, 0, [
            "Copper and zinc sheets with a redstone torch. A part of every electric machine.",
        ], [item("createaddition:capacitor", 2)], xp=15),
        Q("spool", "Spool", 0, 0, [
            "Iron sheets and iron rods (roll iron ingots). An empty spool to wind wire onto.",
        ], [item("createaddition:spool", 2)], xp=10),
        Q("copper_wire", "Copper Wire", 0, 0, [
            "Roll copper sheets into wire.",
        ], [item("createaddition:copper_wire", 8)], xp=10),
        Q("copper_spool", "Copper Spool", 0, 0, [
            "Copper wire wound on a spool. Use it on two connectors to wire them together.",
            "TFMG has its own &aCopper Spool (TFMG Cable)&r for its cable insulators; the two don't mix.",
        ], [item("createaddition:copper_spool", 2)], xp=15),
        Q("electric_motor", "Electric Motor", 0, 0, [
            "&aMechanical Crafting&r: copper spool, capacitor, iron rods, brass sheets and andesite",
            "alloy. Turns electricity back into rotation, with a speed you set. &eNeeds the Brass Age.&r",
        ], [item("createaddition:electric_motor")], xp=60),
        Q("alternator", "Alternator", 0, 0, [
            "&aMechanical Crafting&r: copper spool, iron rods and sheets, andesite alloy. Turns rotation",
            "into electricity: put one on your steam engines' shaft.",
        ], [item("createaddition:alternator")], xp=50),
        Q("electric_pump", "Electric Pump", 0, 0, [
            "A mechanical pump, copper spool, capacitor and dried kelp (mechanical crafting). Pumps",
            "fluid on electricity instead of rotation.",
        ], [item("createaddition:electric_pump")], xp=25),
        Q("modular_accumulator", "Modular Accumulator", 0, 0, [
            "Brass casing, a capacitor, copper rods and electrum wire (roll electrum). Stores electricity. Blocks placed",
            "together act as one battery.",
        ], [item("createaddition:modular_accumulator", 2)], xp=40),
        Q("portable_energy_interface", "Portable Energy Interface", 0, 0, [
            "Brass casing, a chute and a copper spool. Charges batteries on a moving contraption.",
        ], [item("createaddition:portable_energy_interface")], xp=25),
        Q("electrum", "Electrum", 0, 0, [
            "Charge gold ingots with a Tesla Coil. Electrum wire is what the accumulator needs.",
        ], [item("createaddition:electrum_ingot", 4)], xp=20),
        Q("tesla_coil", "Tesla Coil", 0, 0, [
            "&aMechanical Crafting&r: copper spool, capacitor, brass casing and sheets, an electron tube",
            "and andesite alloy. Charges items on a depot below it (gold into Electrum) and zaps",
            "anything that wanders under it.",
        ], [item("createaddition:tesla_coil")], xp=80, shape="hexagon"),
    ]),
    # ----------------------------------------------------------------------------------------------
    dict(slug="heat", group="expansions", title="Heat Expansion",
         subtitle="Superheating and this pack's fuel tiers", icon="create:blaze_cake",
         unlock=[("brass_and_precision", "next")], quests=[
        Q("tiers", "Fuel Tiers", 0, 0, [
            "Some recipes need a &6Superheated&r burner. This pack has three fuel tiers, and each one",
            "needs superheat to produce, so you climb them in order:",
            "",
            "&61. Blaze Cake&r: 2 min 40 s per cake",
            "&62. Biofuel&r: 20 min per bucket",
            "&63. Napalm&r: 1 hour per bucket (made in the &6Industrial Age&r)",
        ], [CHECK], xp=10, shape="gear", size=1.25),
        Q("cinder_flour", "Cinder Flour", 2, 0, [
            "Crush or mill &anetherrack&r.",
        ], [item("create:cinder_flour", 4)], deps=["tiers"], xp=10, items=[("minecraft:sugar", 8), ("minecraft:egg", 4)]),
        Q("spout", "Spout", 6, 0, [
            "A Spout fills items on a Depot or belt with fluid. You'll use it for Blaze Cakes and,",
            "later, for &dQuantum Paper&r.",
        ], [item("create:spout")], deps=["cake_base"], xp=15),
        Q("cake_base", "Blaze Cake Base", 4, 0, [
            "Compact &aEgg + Sugar + Cinder Flour&r in a Basin (no heat needed).",
        ], [item("create:blaze_cake_base", 2)], deps=["cinder_flour"], xp=15),
        Q("blaze_cake", "Tier 1: Blaze Cake", 8, 0, [
            "Fill a Blaze Cake Base with &a250 mB of lava&r using a Spout.",
            "",
            "Feed it to a Blaze Burner: &6Superheated for 2 min 40 s&r. Automate the feeding with a",
            "Mechanical Arm, Deployer or Funnel.",
        ], [item("create:blaze_cake", 2)], deps=["spout"], xp=30, items=[("minecraft:egg", 8)]),
        Q("biomass", "Biomass", 10, 0, [
            "Compact &aseeds&r into Seed Oil, then mix plants (crops, leaves, saplings, flowers) with",
            "&a100 mB of Seed Oil&r over a &6heated&r burner to make &aBiomass&r.",
        ], [item("createaddition:biomass", 4)], deps=["blaze_cake"], xp=20, items=[("minecraft:wheat_seeds", 16)]),
        Q("biofuel", "Tier 2: Biofuel", 12, 0, [
            "&eChanged in this pack:&r brewing Biofuel now needs a &6Superheated&r burner. Mix",
            "&aSugar + Cinder Flour + 2 Biomass&r to make &a125 mB&r.",
            "",
            "Bootstrap it with Blaze Cakes. Once it's running, Biofuel can keep its own mixer hot.",
        ], [item("createaddition:bioethanol_bucket")], deps=["biomass"], xp=40),
        Q("straw", "Blaze Burner with Straw", 14, 0, [
            "Use a &aStraw&r on a Blaze Burner so it accepts &aliquid fuel&r (see its Ponder).",
            "&a1 bucket of Biofuel = 20 minutes of superheat.&r",
        ], [item("createaddition:straw")], deps=["biofuel"], xp=25),
        # --- automate (one stack each) ---
    ]),
    # ----------------------------------------------------------------------------------------------
    dict(slug="industrial", group="ages", title="Industrial Age",
         subtitle="TFMG: cast iron, coke, steel and oil", icon="tfmg:steel_ingot",
         unlock=[("brass_and_precision", "next")], quests=[
        Q("cast_iron", "Cast Iron", 0, 0, [
            "&6TFMG&r industry starts with &aCast Iron&r: compact &airon ingots&r with &acoal&r in a Basin",
            "under a Press.",
        ], [item("tfmg:cast_iron_ingot", 8)], xp=20),
        Q("coke_oven", "Coke Oven", 0, 0, [
            "&aIndustrial Iron Blocks&r and &acast iron&r. Build the oven multiblock (see its Ponder).",
        ], [item("tfmg:coke_oven")], xp=25),
        Q("coal_coke", "Coal Coke", 0, 0, [
            "The Coke Oven bakes &acoal&r into &aCoal Coke&r, the fuel for the blast furnace.",
        ], [item("tfmg:coal_coke", 16)], xp=20),
        Q("blast_furnace", "Blast Furnace", 0, 0, [
            "Built from &afireproof bricks&r with a &aBlast Furnace Output&r (cast iron block, pipe) and",
            "a hatch. Check the Ponder for the full multiblock.",
        ], [item("tfmg:blast_furnace_output")], xp=40),
        Q("blast_stove", "Blast Stove", 0, 0, [
            "Cast iron tank, pipe and fireproof bricks: heats air for the furnace.",
        ], [item("tfmg:blast_stove")], xp=20),
        Q("blast_hatch", "Blast Furnace Hatch", 0, 0, [
            "Cast iron tank, pipe, sheet and fireproof bricks: where materials go in.",
        ], [item("tfmg:blast_furnace_hatch")], xp=20),
        Q("steel", "Steel", 0, 0, [
            "The furnace makes &amolten steel&r; cast it into &aSteel Ingots&r.",
        ], [item("tfmg:steel_ingot", 8)], xp=40),
        Q("steel_casing", "Steel Casing", 0, 0, [
            "Use a &asteel ingot&r on &ahardened planks&r.",
        ], [item("tfmg:steel_casing", 2)], xp=20),
        Q("steel_mechanism", "Steel Mechanism", 0, 0, [
            "Sequenced assembly with heavy plates, lead and nickel sheets, steel cogwheels and screws.",
            "JEI shows every step.",
        ], [item("tfmg:steel_mechanism")], xp=40),
        Q("heavy_casing", "Heavy Machinery Casing", 0, 0, [
            "A &asteel sheet&r on &aSteel Casing&r. The shell for oil and engine machinery.",
        ], [item("tfmg:heavy_machinery_casing", 2)], xp=30),
        Q("surface_scanner", "Surface Scanner", 0, 0, [
            "Heavy casing, steel mechanism and electron tube. Finds &aoil deposits&r underground.",
        ], [item("tfmg:surface_scanner")], xp=25),
        Q("engine", "Engine", 0, 0, [
            "Heavy casing, heavy plate and steel: a fuel-burning engine for serious rotational power.",
        ], [item("tfmg:regular_engine")], xp=30),
        Q("pumpjack", "Pumpjack", 0, 0, [
            "Base, crank and hammer, built over an oil deposit, pump &acrude oil&r.",
        ], [item("tfmg:pumpjack_base"), item("tfmg:pumpjack_crank"), item("tfmg:pumpjack_hammer")], xp=50),
        Q("crude_oil", "Crude Oil", 0, 0, [
            "Build the Pumpjack over an oil deposit (find one with the Surface Scanner) and pump",
            "&aCrude Oil&r into a tank. Fill a bucket from the tank.",
        ], [item("tfmg:crude_oil_bucket")], xp=30),
        Q("distillation", "Distillation Tower", 0, 0, [
            "A &aDistillation Controller&r and outputs on steel tanks refine crude oil into fuels.",
        ], [item("tfmg:steel_distillation_controller"), item("tfmg:steel_distillation_output", 2)], xp=50),
        Q("gasoline", "Gasoline", 0, 0, [
            "The Distillation Tower splits crude oil into fuels. &aGasoline&r is one of its outputs,",
            "and Napalm needs it.",
        ], [item("tfmg:gasoline_bucket")], xp=25),
        Q("diesel", "Diesel", 0, 0, [
            "Another Distillation Tower output. Diesel runs TFMG's diesel engines.",
        ], [item("tfmg:diesel_bucket")], xp=20),
        Q("kerosene", "Kerosene", 0, 0, [
            "Another Distillation Tower output: aviation fuel for jet and turbine engines.",
        ], [item("tfmg:kerosene_bucket")], xp=20),
        Q("aluminum", "Aluminum", 0, 0, [
            "Process &abauxite&r in a chemical vat for &aAluminum Ingots&r. Napalm needs them.",
        ], [item("tfmg:aluminum_ingot", 4)], xp=25),
        Q("napalm", "Tier 3 Fuel: Napalm", 0, 0, [
            "&eChanged in this pack:&r Napalm is mixed from &aAluminum Ingot + 1000 mB Gasoline +",
            "250 mB Biofuel&r over a &6Superheated&r burner (makes 250 mB).",
            "",
            "In a Straw burner: &a1 bucket = 1 hour of superheat&r. Napalm is also a weapon, so handle",
            "with care.",
        ], [item("tfmg:napalm_bucket")], xp=75),
    ]),
    # ----------------------------------------------------------------------------------------------
    dict(slug="quantum", group="expansions", title="Quantum Expansion",
         subtitle="Telejuice, quantum items, waystones and teleporters", icon="createwars:quantum_pearl",
         unlock=[("brass_and_precision", "next")], quests=[
        Q("chorus", "Chorus Fruit", 0, 0, [
            "Everything quantum starts in &dthe End&r: bring back &achorus fruit&r (and plant some).",
        ], [item("minecraft:chorus_fruit", 16)], xp=20),
        Q("telejuice", "Telejuice", 0, 0, [
            "Mix &aChorus Fruit + 250 mB water&r over a &6heated&r burner to make &dTelejuice&r",
            "(Quantum Fluid).",
        ], [item("createteleporters:quantum_fluid_bucket")], xp=40),
        Q("quantum_casing", "Quantum Casing", 0, 0, [
            "Fill a &aRailway Casing&r with &a1000 mB of Telejuice&r using a Spout.",
        ], [item("createteleporters:quantum_casing", 2)], xp=25),
        Q("quantum_paper", "Quantum Paper", 0, 0, [
            "&eThis pack's own item:&r Spout &a100 mB of Telejuice&r onto &aPaper&r. Used for every",
            "waystone scroll.",
        ], [item("createwars:quantum_paper", 8)], xp=20),
        Q("quantum_pearl", "Quantum Pearl", 0, 0, [
            "&eThis pack's own item:&r mix an &aEnder Pearl + 250 mB Telejuice&r in a Basin.",
            "Replaces ender pearls in waystone recipes.",
        ], [item("createwars:quantum_pearl", 4)], xp=30),
        Q("warp_dust", "Warp Dust", 0, 0, [
            "&eChanged in this pack:&r a &aQuantum Pearl&r and an &aamethyst shard&r make 4 Warp Dust.",
        ], [item("waystones:warp_dust", 4)], xp=20),
        Q("warp_stone", "Warp Stone", 0, 0, [
            "&eChanged in this pack:&r mechanical crafting with &a7 Quantum Pearls&r, amethyst and",
            "emeralds.",
        ], [item("waystones:warp_stone")], xp=40),
        Q("redstone_pearl", "Redstone Pearl", 0, 0, [
            "Mix an &aender pearl&r with &arose quartz&r. A core part of teleporter tech.",
        ], [item("createteleporters:redstone_pearl", 2)], xp=20),
        Q("waystone", "Waystone", 0, 0, [
            "&eChanged in this pack:&r waystones don't generate. Mechanical crafting: Warp Stone,",
            "&d3 Quantum Pearls&r, &d2 Quantum Casings&r, casings and bricks.",
        ], [item("waystones:waystone")], xp=60),
        Q("sharestone", "Sharestone", 0, 0, [
            "A waystone shared by everyone who uses the same color. Uses Quantum Casings too.",
        ], [item("waystones:purple_sharestone")], xp=25),
        Q("portstone", "Portstone", 0, 0, [
            "Mechanical crafting: a Quantum Casing, a Warp Stone, andesite casing, stone bricks and",
            "dye. A one-way teleport point: it only sends you, it can't be a destination.",
        ], [item("waystones:white_portstone")], xp=25),
        Q("warp_plate", "Warp Plate", 0, 0, [
            "Mechanical crafting: Warp Dust, andesite casing, stone bricks and flint (makes 2).",
            "Step on one to warp to the plate it is linked to.",
        ], [item("waystones:warp_plate", 2)], xp=25),
        Q("blank_scroll", "Blank Scroll", 0, 0, [
            "&eChanged in this pack:&r every scroll is made from &dQuantum Paper&r.",
        ], [item("waystones:blank_scroll", 3)], xp=20),
        Q("warp_scroll", "Warp Scroll", 0, 0, [
            "One-time teleport to a waystone. Uses a &dQuantum Pearl&r in this pack.",
        ], [item("waystones:warp_scroll")], xp=20),
        Q("return_scroll", "Return Scroll", 0, 0, [
            "Quantum Paper, a gold nugget and purple dye. One use: teleports you to your spawn",
            "point.",
        ], [item("waystones:return_scroll")], xp=20),
        Q("advanced_part", "Advanced Component", 0, 0, [
            "Sequenced assembly on a &asturdy sheet&r with a &adiamond&r and a &aRedstone Pearl&r.",
        ], [item("createteleporters:advanced_part", 2)], xp=40),
        Q("quantum_mechanism", "Quantum Mechanism", 0, 0, [
            "Sequenced assembly: Advanced Component, sturdy sheet and &dTelejuice&r. The heart of every",
            "teleporter.",
        ], [item("createteleporters:quantum_mechanism", 2)], xp=50),
        Q("tp_link", "TP Link", 0, 0, [
            "Links teleporters together. Advanced component, brass sheet, redstone pearl, transmitter.",
        ], [item("createteleporters:tp_link")], xp=25),
        Q("teleporter", "Entity Teleporter", 0, 0, [
            "Brass casing, electron tube, Quantum Mechanism and Redstone Pearl. Fill it with",
            "&dTelejuice&r to teleport to a paired destination.",
        ], [item("createteleporters:teleporter")], xp=60),
        Q("item_tp", "Item Teleporter", 0, 0, [
            "Sends items to a paired destination. Brass casing, chute, barrel, Quantum Mechanism.",
        ], [item("createteleporters:item_tp")], xp=40),
        Q("block_teleporter", "Block Teleporter", 0, 0, [
            "Moves a block to a paired destination. Needs an Item Teleporter and a Deployer.",
        ], [item("createteleporters:block_teleporter")], xp=40),
        Q("adv_tplink", "Advanced TP Link", 0, 0, [
            "Quantum casing, Quantum Mechanism, Redstone Pearl and a transmitter. Links portals.",
        ], [item("createteleporters:adv_tplink")], xp=40),
        Q("custom_portal", "Custom Portal Controller", 0, 0, [
            "Mechanical crafting with an Entity Teleporter, Quantum Mechanism and more: build portals",
            "of your own shape. Each base needs at least 256 mB of Telejuice.",
        ], [item("createteleporters:custom_portal_base")], xp=75),
        # Create: Ender Transmission (owner 2026-11-22: "should be a quantum thing", recipes made harder with
        # quantum items: pack/kubejs/server_scripts/ender_transmission_quantum.js)
        Q("item_transmitter", "Item Transmitter", 0, 0, [
            "&6Create: Ender Transmission&r: quantum-linked logistics. Every Item Transmitter on the",
            "same &aNetwork&r (1-10) shares items, across any distance and any dimension.",
            "&dPack recipe&r (mechanical crafting): obsidian, a chute, Quantum Casings, Quantum Pearls,",
            "Advanced Components and a Quantum Mechanism.",
        ], [item("createendertransmission:item_transmitter", 2)], xp=100),
        Q("fluid_transmitter", "Fluid Transmitter", 0, 0, [
            "The same recipe with a &aMechanical Pump&r in place of the chute. Moves fluids",
            "between Fluid Transmitters on the same Network.",
        ], [item("createendertransmission:fluid_transmitter", 2)], xp=60),
        Q("energy_transmitter", "Energy Transmitter", 0, 0, [
            "The same recipe with a &aShaft&r in place of the chute. Sends rotation to every",
            "Energy Transmitter on the Network: power a front-line base from home.",
        ], [item("createendertransmission:energy_transmitter", 2)], xp=60),
        Q("chunk_loader", "Chunk Loader", 0, 0, [
            "Keeps the chunks around it loaded, so remote machines keep running. A beacon wrapped in",
            "Quantum Casings and Quantum Pearls, with a Quantum Mechanism (pack recipe).",
        ], [item("createendertransmission:chunk_loader")], xp=80),
    ]),
    # ----------------------------------------------------------------------------------------------
    dict(slug="enchanting", group="expansions", title="Enchanting Expansion",
         subtitle="Create: Enchantment Industry: liquid experience and machine enchanting",
         icon="create_enchantment_industry:blaze_enchanter", unlock=[("brass_and_precision", "next")], quests=[
        Q("grindstone", "Mechanical Grindstone", 0, 0, [
            "Andesite alloy and a shaft. The entry point to Enchantment Industry; its Ponder shows how",
            "it turns items and enchantments into &aliquid experience&r.",
        ], [item("create_enchantment_industry:mechanical_grindstone")], xp=20),
        Q("liquid_xp", "Liquid Experience", 0, 0, [
            "Collect your first bucket of liquid experience (&aBucket o' Enchanting&r).",
        ], [item("create_enchantment_industry:experience_bucket")], xp=30),
        Q("xp_cake_base", "Cake Base o' Enchanting", 0, 0, [
            "Compact &aeggs, sugar and lapis&r in a Basin.",
        ], [item("create_enchantment_industry:experience_cake_base")], xp=15),
        Q("xp_cake", "Cake o' Enchanting", 0, 0, [
            "Fill the cake base with liquid experience using a Spout.",
        ], [item("create_enchantment_industry:experience_cake")], xp=20),
        Q("xp_block", "Block of Experience", 0, 0, [
            "Compact &aliquid experience&r into a solid &aBlock of Experience&r.",
        ], [item("create:experience_block", 2)], xp=30),
        Q("enchanting_template", "Enchanting Template", 0, 0, [
            "Press a &aBlock of Experience&r into an &aEnchanting Template&r.",
        ], [item("create_enchantment_industry:enchanting_template")], xp=25),
        Q("xp_hatch", "Experience Hatch", 0, 0, [
            "Apply a Block of Experience to a fluid hatch. Right-click to store your own levels as",
            "liquid experience; sneak-right-click to take them back.",
        ], [item("create_enchantment_industry:experience_hatch")], xp=25),
        Q("xp_lantern", "Experience Lantern", 0, 0, [
            "Copper casing, Block of Experience and a sponge.",
        ], [item("create_enchantment_industry:experience_lantern")], xp=20),
        Q("blaze_enchanter", "Blaze Enchanter", 0, 0, [
            "Smithing: a &aBlaze Burner&r, an &aenchanting table&r and a &aBlaze Upgrade Smithing",
            "Template&r. Enchants items automatically with liquid experience.",
        ], [item("create_enchantment_industry:blaze_enchanter")], xp=60),
        Q("blaze_forger", "Blaze Forger", 0, 0, [
            "Smithing table: a Blaze Upgrade template, a Blaze Burner and an anvil. Repairs and",
            "combines enchanted gear with liquid experience.",
        ], [item("create_enchantment_industry:blaze_forger")], xp=40),
        Q("printer", "Printer", 0, 0, [
            "Brass sheet, a Spout and a block of iron. Copies books and enchanted books.",
        ], [item("create_enchantment_industry:printer")], xp=40),
    ]),
    # ----------------------------------------------------------------------------------------------
    dict(slug="artillery", group="warfare", title="Artillery",
         subtitle="Create Big Cannons: from log cannons to built-up steel and autocannons",
         icon="createbigcannons:cast_iron_cannon_barrel", unlock=[("kinetics", "next")], quests=[
        Q("log_cannon", "Log Cannon", 0, 0, [
            "The simplest big cannon: &alogs&r and &agunpowder&r make a &aLog Cannon Chamber&r and an end.",
            "Short range and fragile, but it fires. &cBig Cannons are multiblocks&r: check each part's Ponder.",
        ], [item("createbigcannons:log_cannon_chamber"), item("createbigcannons:log_cannon_end")], xp=20),
        Q("cannon_mount", "Cannon Mount", 0, 0, [
            "Andesite casing, iron sheet, shaft and gunpowder. A mount turns and aims a cannon with",
            "rotational power; assemble the cannon on it.",
        ], [item("createbigcannons:cannon_mount")], xp=30),
        Q("wrought_iron", "Wrought Iron Cannon", 0, 0, [
            "&aIron sheets&r and gunpowder: a sturdier chamber than logs.",
        ], [item("createbigcannons:wrought_iron_cannon_chamber"), item("createbigcannons:wrought_iron_cannon_end")], xp=20),
        Q("cannon_carriage", "Cannon Carriage", 0, 0, [
            "Wheels, planks and a shaft: a field carriage to drag a light cannon around.",
        ], [item("createbigcannons:cannon_carriage")], xp=15),
        Q("cannon_loader", "Cannon Loader", 0, 0, [
            "Andesite casing, piston pole and gunpowder. Pushes charges and shells into the breech.",
        ], [item("createbigcannons:cannon_loader")], xp=20),
        Q("powder", "Powder Charge", 0, 0, [
            "Compact gunpowder into &aPacked Gunpowder&r and put it in an &aEmpty Powder Charge&r",
            "(wool and string). More charges = more range, and more strain on the barrel.",
        ], [item("createbigcannons:powder_charge", 4)], xp=25),
        Q("solid_shot", "Solid Shot", 0, 0, [
            "Iron ingots, iron nuggets and wooden slabs: the basic cannonball.",
        ], [item("createbigcannons:solid_shot", 4)], xp=15),
        Q("congealed_nitro", "Congealed Nitro", 0, 0, [
            "Mix &ablaze powder, gunpowder and magma cream&r. The start of stronger propellant.",
        ], [item("createbigcannons:congealed_nitro")], xp=15),
        Q("hardened_nitro", "Hardened Nitro", 0, 0, [
            "Smelt congealed nitro. Crush or mill it into Nitropowder, the stronger propellant.",
        ], [item("createbigcannons:hardened_nitro")], xp=15),
        Q("nitropowder", "Nitropowder", 0, 0, [
            "Mill hardened nitro into &aNitropowder&r: a stronger charge filling than gunpowder.",
        ], [item("createbigcannons:nitropowder", 4)], xp=25),
        Q("shells", "High Explosive Shell", 0, 0, [
            "Mechanical crafting: explosive filling, iron and wooden slabs. Shells need a &afuze&r to",
            "go off.",
        ], [item("createbigcannons:he_shell", 2)], xp=30),
        Q("ap_shell", "Armor Piercing Shell", 0, 0, [
            "Adds &acast iron&r: punches through armor before exploding.",
        ], [item("createbigcannons:ap_shell")], xp=20),
        Q("shrapnel_shell", "Shrapnel Shell", 0, 0, [
            "Shot balls and gunpowder: bursts into fragments.",
        ], [item("createbigcannons:shrapnel_shell")], xp=20),
        Q("smoke_shell", "Smoke Shell", 0, 0, [
            "A hay bale in an iron shell: bursts into a smoke screen to hide an advance.",
        ], [item("createbigcannons:smoke_shell")], xp=15),
        Q("impact_fuze", "Impact Fuze", 0, 0, [
            "An impact fuze head and redstone (makes 2). Goes off on contact. Put a fuze on a shell",
            "before you load it.",
        ], [item("createbigcannons:impact_fuze", 2)], xp=15),
        Q("timed_fuze", "Timed Fuze", 0, 0, [
            "Clock, iron and redstone: bursts after a set time, for airbursts.",
        ], [item("createbigcannons:timed_fuze")], xp=15),
        Q("proximity_fuze", "Proximity Fuze", 0, 0, [
            "Iron bars, quartz and redstone: bursts near a target.",
        ], [item("createbigcannons:proximity_fuze")], xp=20),
        Q("casting", "Cast Iron Cannon", 0, 0, [
            "Better cannons are &acast&r: pour molten cast iron into a &amould&r. Check the Ponder",
            "for casting setups.",
        ], [item("createbigcannons:cast_iron_cannon_chamber"), item("createbigcannons:cast_iron_cannon_barrel")], xp=40),
        Q("casting_sand", "Casting Sand", 0, 0, [
            "Clay, dirt and sand: lines the moulds.",
        ], [item("createbigcannons:casting_sand", 4)], xp=10),
        Q("foundry_lid", "Basin Foundry Lid", 0, 0, [
            "Andesite alloy. Turns a Basin into a foundry for melting metal.",
        ], [item("createbigcannons:basin_foundry_lid")], xp=15),
        Q("cast_mould", "Cast Mould", 0, 0, [
            "Cut logs into a mould. Bigger cannon parts need bigger moulds.",
        ], [item("createbigcannons:small_cast_mould")], xp=10),
        Q("bronze", "Bronze Cannon", 0, 0, [
            "Cast a barrel from molten &abronze&r: lighter and tougher than cast iron.",
        ], [item("createbigcannons:bronze_cannon_barrel")], xp=30),
        Q("built_up", "Built-Up Steel Cannon", 0, 0, [
            "The strongest barrels are &abuilt up&r from steel layers with a Cannon Builder, then",
            "bored with a Cannon Drill. Check the Ponder.",
        ], [item("createbigcannons:built_up_steel_cannon_barrel")], xp=60),
        Q("cannon_builder", "Cannon Builder", 0, 0, [
            "Andesite casing, iron sheet, iron nuggets and a piston pole.",
        ], [item("createbigcannons:cannon_builder")], xp=20),
        Q("cannon_drill", "Cannon Drill", 0, 0, [
            "Andesite casing, fluid pipe, iron and a piston pole. Bores out cast and built-up barrels.",
        ], [item("createbigcannons:cannon_drill")], xp=20),
        Q("cannon_welder", "Cannon Welder", 0, 0, [
            "A &aBlaze Burner&r (Brass Age), brass and iron sheets. Welds built-up cannon parts",
            "together.",
        ], [item("createbigcannons:cannon_welder")], xp=25),
        Q("autocannon", "Autocannon", 0, 0, [
            "A rapid-fire cannon from a cast &abreech&r and &abarrel&r. Feeds on cartridges.",
        ], [item("createbigcannons:cast_iron_autocannon_breech"), item("createbigcannons:cast_iron_autocannon_barrel")], xp=50),
        Q("autocannon_cartridge", "Autocannon Cartridge", 0, 0, [
            "Sequenced assembly: press an &aAutocannon Cartridge Sheet&r into a case. Fill it with powder",
            "and add a round to make ammunition.",
        ], [item("createbigcannons:empty_autocannon_cartridge", 4)], xp=15),
        Q("ap_autocannon_round", "AP Autocannon Round", 0, 0, [
            "Cast iron and iron (makes 8). Armor-piercing ammo for the autocannon.",
        ], [item("createbigcannons:ap_autocannon_round", 8)], xp=20),
        Q("ammo_container", "Autocannon Ammo Container", 0, 0, [
            "Brass and iron sheets. Holds a belt of autocannon rounds for continuous fire.",
        ], [item("createbigcannons:autocannon_ammo_container")], xp=20),
        Q("firepower", "Compact Cannon Mount", 0, 0, [
            "&6CBC: Firepower Components&r: a compact mount for cannons on vehicles and ships. Brass",
            "casing, shaft, cogwheel, iron plate and gunpowder.",
            "&eNeeds the Brass Age.&r Automate brass (Automation chapter) to keep these guns fed.",
        ], [item("cbc_firepower_components:compact_cannon_mount")], xp=40),
        Q("compact_autocannon_mount", "Compact Autocannon Mount", 0, 0, [
            "A small autocannon mount for vehicles: andesite casing, brass sheet, shaft, cogwheel, iron",
            "plate and gunpowder.",
        ], [item("cbc_firepower_components:compact_autocannon_mount")], xp=25),
        Q("auto_cannon_controller", "Automatic Cannon Controller", 0, 0, [
            "Industrial iron, a brass sheet, redstone and a comparator. Lets a mounted cannon aim and",
            "fire on its own.",
        ], [item("cbc_firepower_components:automatic_cannon_controller")], xp=30),
        Q("magazine_loader", "Cannon Magazine Loader", 0, 0, [
            "Brass casing and sheet, industrial iron, a &aCannon Loader&r and redstone. Reloads a big",
            "cannon from a magazine, so it keeps firing without a loader crew.",
        ], [item("cbc_firepower_components:cannon_magazine_loader")], xp=30),
        Q("ballistic_computer", "Ballistic Computer", 0, 0, [
            "&6CBC Ballistic Computer&r: brass casing, electron tube, precision mechanism, shaft and a",
            "display board. Calculates the trajectory so you hit what you aim at.",
            "&eNeeds the Brass Age.&r Automate brass (Automation chapter) to keep these guns fed.",
        ], [item("cbcballistic:ballistic_computer")], xp=40),
        Q("nethersteel", "Nethersteel", 0, 0, [
            "The top cannon material. Cast a barrel from molten &anethersteel&r.",
        ], [item("createbigcannons:nethersteel_cannon_barrel")], xp=75),
    ]),
    # ----------------------------------------------------------------------------------------------
    dict(slug="infantry", group="warfare", title="Infantry",
         subtitle="Create: Gunsmithing: guns built with Create machines", icon="cgs:revolver",
         unlock=[("kinetics", "next")], quests=[
        Q("lead", "Lead", 0, 0, [
            "Bullets are made of &alead&r. Mine and smelt lead ore.",
        ], [item("tfmg:lead_ingot", 8)], xp=15),
        Q("flintlock", "Flintlock", 0, 0, [
            "Andesite alloy, iron sheet, flint and steel and a stripped log: your first gun.",
        ], [item("cgs:flintlock")], xp=30),
        Q("paper_cartridge", "Paper Cartridge", 0, 0, [
            "Gunpowder, a lead nugget and paper: flintlock ammo.",
        ], [item("cgs:paper_cartridge", 8)], xp=15),
        Q("musket_barrel", "Musket Barrel", 0, 0, [
            "Iron sheets and a stripped log. A longer flintlock barrel: more range.",
        ], [item("cgs:flintlock_long_barrel")], xp=15),
        Q("stock", "Stock", 0, 0, [
            "Brass sheet and a stripped log: steadies your aim.",
        ], [item("cgs:stock")], xp=15),
        Q("bayonet", "Bayonet", 0, 0, [
            "Iron and brass sheets. Fixes to the flintlock for when they get too close.",
        ], [item("cgs:bayonet")], xp=10),
        Q("steel", "Steel", 0, 0, [
            "Mix &acharcoal dust&r with &airon&r to make steel. Better guns need it.",
            "&aOne steel:&r every mod's steel is the same item here, so steel from the Industrial",
            "Age blast furnace works too.",
        ], [item("tfmg:steel_ingot", 4)], xp=25),
        Q("charcoal_dust", "Charcoal Dust", 0, 0, [
            "Crush or mill charcoal.",
        ], [item("cgs:charcoal_dust", 4)], xp=10),
        Q("steel_sheet", "Steel Sheet", 0, 0, [
            "Press gun steel into sheets.",
        ], [item("cgs:steel_sheet", 4)], xp=15),
        Q("revolver", "Revolver", 0, 0, [
            "Mechanical crafting: steel, brass and steel sheets, andesite alloy, a cogwheel and a log.",
        ], [item("cgs:revolver")], xp=40),
        Q("press_form_revolver", "Revolver Shell Press Form", 0, 0, [
            "Stonecut an iron ingot. A Press with this form stamps shells.",
        ], [item("cgs:press_form_revolver")], xp=10),
        Q("shell_revolver", "Revolver Shell", 0, 0, [
            "Sequenced assembly: brass sheet and gunpowder, pressed with the form.",
        ], [item("cgs:shell_revolver", 8)], xp=15),
        Q("round_revolver", "Revolver Round", 0, 0, [
            "Add a lead nugget to a blank round.",
        ], [item("cgs:round_revolver", 16)], xp=20),
        Q("scope", "Scope", 0, 0, [
            "Spyglass, brass sheet and black dye.",
        ], [item("cgs:scope")], xp=15),
        Q("long_barrel", "Revolver: Long Barrel", 0, 0, [
            "A longer barrel for the revolver.",
        ], [item("cgs:long_barrel")], xp=15),
        Q("shotgun", "Shotgun", 0, 0, [
            "Mechanical crafting: brass and steel sheets, andesite alloy and a stripped log.",
        ], [item("cgs:shotgun")], xp=40),
        Q("press_form_shotgun", "Shotgun Shell Press Form", 0, 0, [
            "Stonecut an iron ingot. A Press with this form stamps shotgun shells.",
        ], [item("cgs:press_form_shotgun")], xp=10),
        Q("shell_shotgun", "Shotgun Shell", 0, 0, [
            "Sequenced assembly on a blank shotgun round, with nails or blaze powder (makes 8).",
        ], [item("cgs:shell_shotgun", 8)], xp=15),
        Q("round_shotgun", "Shotgun Round", 0, 0, [
            "Lead balls into a blank shotgun round.",
        ], [item("cgs:round_shotgun", 16)], xp=20),
        Q("gatling", "Gatling", 0, 0, [
            "Adds a &aprecision mechanism&r and a cogwheel to the steel-and-brass build.",
        ], [item("cgs:gatling")], xp=60),
        Q("round_gatling", "Gatling Round", 0, 0, [
            "Lead and copper nuggets into a blank gatling round.",
        ], [item("cgs:round_gatling", 32)], xp=25),
        Q("launcher", "Launcher", 0, 0, [
            "Chute, fluid pipe, brass and steel sheets: fires rockets.",
        ], [item("cgs:launcher")], xp=50),
        Q("rocket", "Rocket", 0, 0, [
            "Sequenced assembly: TNT, brass sheet and a fluid pipe.",
        ], [item("cgs:rocket", 4)], xp=20),
        Q("frag_grenade", "Frag Grenade", 0, 0, [
            "Iron and brass sheets, gunpowder, copper nuggets and a cogwheel.",
        ], [item("cgs:frag_grenade", 4)], xp=20),
        Q("blazegun", "Blazegun", 0, 0, [
            "A &ablaze burner&r, fluid tank, pipe and chute: a flamethrower.",
        ], [item("cgs:blazegun")], xp=60),
        Q("nailgun", "Nailgun", 0, 0, [
            "Runs off a &acopper backtank&r: precision mechanism, valve, pipe, brass and iron sheets.",
        ], [item("cgs:nailgun")], xp=50),
        Q("nails", "Nails", 0, 0, [
            "Iron nuggets (crafting or sequenced assembly). Nailgun ammo.",
        ], [item("cgs:nail", 32)], xp=15),
        Q("ballistazooka", "Ballistazooka", 0, 0, [
            "A &aflywheel&r, string, brass and iron sheets: a handheld ballista.",
        ], [item("cgs:ballistazooka")], xp=50),
    ]),
    # ----------------------------------------------------------------------------------------------
    dict(slug="radar", group="warfare", title="Radar and Missiles",
         subtitle="Create: Radars, fire control and guided missiles", icon="create_radar:radar_dish_block",
         unlock=[("brass_and_precision", "next"), ("artillery", "cannon_mount")], quests=[
        Q("binoculars", "Binoculars", 0, 0, [
            "Copper, glass panes and string. Spot targets by eye before you track them by radar.",
        ], [item("create_radar:binoculars")], xp=15),
        Q("radar_bearing", "Radar Bearing", 0, 0, [
            "A mechanical bearing, electron tube and iron sheet. Build a dish on it and spin it to",
            "&ascan the sky&r. Check the Ponder for radar builds.",
        ], [item("create_radar:radar_bearing")], xp=40),
        Q("radar_dish", "Radar Dish", 0, 0, [
            "Iron sheets and bars: the dish surface.",
        ], [item("create_radar:radar_dish_block", 8)], xp=15),
        Q("radar_plate", "Radar Plate", 0, 0, [
            "Iron sheets: flat radar panels.",
        ], [item("create_radar:radar_plate_block", 8)], xp=15),
        Q("radar_receiver", "Radar Receiver", 0, 0, [
            "Industrial iron, an electron tube and a lightning rod.",
        ], [item("create_radar:radar_receiver_block")], xp=20),
        Q("monitor", "Monitor", 0, 0, [
            "Brass casing, electron tube and precision mechanism. Shows radar contacts.",
        ], [item("create_radar:monitor")], xp=40),
        Q("data_link", "Data Link", 0, 0, [
            "Brass casing, redstone torch and transmitter: connects radar to other machines.",
        ], [item("create_radar:data_link")], xp=20),
        Q("detection_filter", "Detection Filter", 0, 0, [
            "Paper, electron tube and redstone: choose what radar sees.",
        ], [item("create_radar:radar_filter_item")], xp=15),
        Q("targeting_filter", "Targeting Filter", 0, 0, [
            "Paper, precision mechanism and redstone: choose what gets shot at.",
        ], [item("create_radar:target_filter_item")], xp=15),
        Q("ident_filter", "Identification Filter", 0, 0, [
            "Paper, an electron tube and redstone. Tells friend from foe, so your guns leave",
            "transponder-marked craft alone.",
        ], [item("create_radar:ident_filter_item")], xp=15),
        Q("auto_aim", "Auto Yaw and Pitch Controllers", 0, 0, [
            "A gearbox and a precision mechanism each. They let radar &aaim a cannon mount&r for you.",
        ], [item("create_radar:auto_yaw_controller"), item("create_radar:auto_pitch_controller")], xp=50),
        Q("fire_controller", "Fire Controller", 0, 0, [
            "Brass casing, comparator, precision mechanism and redstone: fires when on target.",
        ], [item("create_radar:fire_controller")], xp=30),
        Q("guided_fuze", "Guided Fuze", 0, 0, [
            "Electron tube, precision mechanism and redstone: shells that steer.",
        ], [item("create_radar:guided_fuze", 2)], xp=25),
        Q("fire_arc", "Fire Arc Filters", 0, 0, [
            "&6Create Radar: Fire Arc Filter&r. Mark &cno-fire sectors&r so turrets don't hit your own",
            "base or ships.",
        ], [item("create_radar_firearc:yaw_fire_arc_filter"), item("create_radar_firearc:pitch_fire_arc_filter")], xp=25),
        Q("plane_radar", "Plane Radar", 0, 0, [
            "Brass casing, a radar dish and a receiver: compact radar for aircraft.",
        ], [item("create_radar:plane_radar")], xp=40),
        Q("transponder", "Identification Transponder", 0, 0, [
            "Brass casing, electron tube and redstone link: marks you as friendly.",
        ], [item("create_radar:identification_transponder")], xp=25),
        Q("network_controller", "Network Controller", 0, 0, [
            "Brass casing, a precision mechanism and all three filters (detection, targeting,",
            "identification). Applies them to a whole radar network at once.",
        ], [item("create_radar:network_filterer")], xp=30),
        Q("safe_zone", "Radar Safe Zone Designator", 0, 0, [
            "Paper, a compass and redstone. Marks an area your radar weapons won't fire into, such as",
            "your own base.",
        ], [item("create_radar:radar_safe_zone_designator")], xp=20),
        Q("missile_mount", "Missile Mount", 0, 0, [
            "&6CBC Aeronautics Missiles&r: brass casing, steel, iron sheet and precision mechanism.",
            "Launches guided missiles.",
        ], [item("cbcaeronauticsmissiles:missile_mount")], xp=50),
        Q("actuator_fins", "Actuator Fins", 0, 0, [
            "Iron sheet, precision mechanism and shaft: steering for a missile.",
        ], [item("cbcaeronauticsmissiles:actuator_fins", 2)], xp=20),
        Q("rocket_motor", "Rocket Motor", 0, 0, [
            "Actuator fins, brass casing, steel and a powder charge.",
        ], [item("cbcaeronauticsmissiles:rocket_motor")], xp=30),
        Q("payload_casing", "Payload Casing", 0, 0, [
            "Zinc: the missile body that carries the warhead.",
        ], [item("cbcaeronauticsmissiles:octagonal_copycat", 4)], xp=15),
        Q("guidance", "Guidance Computer", 0, 0, [
            "Brass sheet, compass, electron tube, steel and precision mechanism: steers the missile",
            "onto a radar track.",
        ], [item("cbcaeronauticsmissiles:guidance_computer")], xp=60),
        Q("targeting_interface", "Targeting Interface", 0, 0, [
            "Uses a &aMechanical Arm&r: pick targets for your missiles.",
        ], [item("cbcaeronauticsmissiles:targeting_interface")], xp=40),
        Q("air_prox_fuze", "Aircraft Proximity Fuze", 0, 0, [
            "Built from a proximity fuze: bursts near aircraft.",
        ], [item("cbcaeronauticsmissiles:aircraft_proximity_fuze")], xp=30),
    ]),
    # ----------------------------------------------------------------------------------------------
    dict(slug="aeronautics", group="warfare", title="Aeronautics",
         subtitle="Create Aeronautics + Sable: airships, planes and air weapons", icon="aeronautics:propeller_bearing",
         unlock=[("brass_and_precision", "next")], quests=[
        Q("physics_assembler", "Physics Assembler", 0, 0, [
            "Everything that flies (or drives, or sails) starts here. A &aPhysics Assembler&r turns a",
            "built contraption into a real &6Sable&r physics object. Check its Ponder.",
        ], [item("simulated:physics_assembler")], xp=25),
        Q("levitite", "Levitite", 0, 0, [
            "&aLevitite&r provides lift: build it into a hull to make it float.",
        ], [item("aeronautics:levitite", 8)], xp=30),
        Q("end_stone_powder", "End Stone Powder", 0, 0, [
            "Crushed end stone: part of the levitite process (see JEI).",
        ], [item("aeronautics:end_stone_powder", 8)], xp=15),
        Q("levitite_blend", "Levitite Blend", 0, 0, [
            "Liquid levitite blend. JEI shows how it sets into solid levitite.",
        ], [item("aeronautics:levitite_blend_bucket")], xp=20),
        Q("pearlescent_levitite", "Pearlescent Levitite", 0, 0, [
            "A stronger levitite, made from levitite (see JEI for the step). More lift for",
            "the same space.",
        ], [item("aeronautics:pearlescent_levitite", 4)], xp=25),
        Q("hot_air", "Hot Air Burner", 0, 0, [
            "Hot air balloons: a &aHot Air Burner&r under an envelope gives adjustable lift.",
        ], [item("aeronautics:adjustable_burner")], xp=30),
        Q("steam_vent", "Steam Vent", 0, 0, [
            "A copper block and gold sheets. Fills an envelope with steam from a boiler, instead",
            "of hot air from a burner.",
        ], [item("aeronautics:steam_vent")], xp=15),
        Q("aviators_goggles", "Aviator's Goggles", 0, 0, [
            "Engineer's Goggles and leather. Goggles for pilots.",
        ], [item("aeronautics:aviators_goggles")], xp=15),
        Q("propeller", "Propeller Bearing", 0, 0, [
            "Mount blades on a &aPropeller Bearing&r and spin it for thrust.",
        ], [item("aeronautics:propeller_bearing")], xp=35),
        Q("wooden_propeller", "Wooden Propeller", 0, 0, [
            "Convert an Andesite Propeller in a crafting grid. Light, cheap blades.",
        ], [item("aeronautics:wooden_propeller")], xp=15),
        Q("andesite_propeller", "Andesite Propeller", 0, 0, [
            "Wooden slabs, a Create propeller and a shaft. Sturdier blades for a Propeller",
            "Bearing.",
        ], [item("aeronautics:andesite_propeller")], xp=15),
        Q("smart_propeller", "Smart Propeller", 0, 0, [
            "Brass casing, a gyroscopic mechanism and a propeller. A propeller you can steer",
            "and throttle with redstone.",
        ], [item("aeronautics:smart_propeller")], xp=20),
        Q("gyro_propeller", "Gyroscopic Propeller Bearing", 0, 0, [
            "Brass casing, wooden slabs and a gyroscopic mechanism. A propeller bearing that",
            "keeps itself level.",
        ], [item("aeronautics:gyroscopic_propeller_bearing")], xp=25),
        Q("controls", "Steering Wheel", 0, 0, [
            "Fly it yourself: a &aSteering Wheel&r on your craft lets you steer from the seat.",
        ], [item("simulated:steering_wheel")], xp=35),
        Q("throttle", "Throttle Lever", 0, 0, [
            "Brass casing and a stick. Sets engine and propeller power from the seat.",
        ], [item("simulated:throttle_lever")], xp=15),
        Q("altitude_sensor", "Altitude Sensor", 0, 0, [
            "Outputs redstone by height: the basis of altitude hold.",
        ], [item("simulated:altitude_sensor")], xp=15),
        Q("navigation_table", "Navigation Table", 0, 0, [
            "Brass casing, a brass sheet and a precision mechanism. Plots a course and can",
            "steer the craft toward it.",
        ], [item("simulated:navigation_table")], xp=15),
        Q("gimbal_sensor", "Gimbal Sensor", 0, 0, [
            "Brass casing, a compass and a gyroscopic mechanism. Outputs redstone by tilt: the",
            "sensor behind auto-leveling.",
        ], [item("simulated:gimbal_sensor")], xp=15),
        Q("gyroscope", "Gyroscope", 0, 0, [
            "&6Aeroworks&r: a flywheel and a Gimbal Sensor. Powered by rotation, it holds your craft",
            "level and steady.",
        ], [item("aeroworks:gyroscope")], xp=25),
        Q("cockpit", "Control Stand", 0, 0, [
            "&6Aeroworks&r: a real cockpit. A &aControl Stand&r (copper casing, redstone link, electron",
            "tube, transmitter, precision mechanism) has &asockets&r for control modules. Sneak-right-click",
            "it to bind each module to &aRedstone Link&r frequencies, then wire those to your craft.",
        ], [item("aeroworks:control_stand")], xp=40),
        Q("control_desk", "Control Desk", 0, 0, [
            "The same console in brass casing: a desk-style cockpit for bigger craft.",
        ], [item("aeroworks:control_desk")], xp=25),
        Q("lever_module", "Lever Module", 0, 0, [
            "An analog lever on brass casing with a transmitter: one tilt lever. The base for the yoke",
            "and throttle quadrant.",
        ], [item("aeroworks:lever_module")], xp=15),
        Q("yoke_module", "Yoke Module", 0, 0, [
            "A lever module, brass and brass casing: pitch and roll in one control.",
        ], [item("aeroworks:yoke_module")], xp=20),
        Q("throttle_quadrant_module", "Throttle Quadrant", 0, 0, [
            "Crafted from a lever module: four throttle levers, one per engine.",
        ], [item("aeroworks:throttle_quadrant_module")], xp=20),
        Q("joystick_module", "Joystick Module", 0, 0, [
            "An analog lever, brass casing and a transmitter: two tilt axes on one stick.",
        ], [item("aeroworks:joystick_module")], xp=20),
        Q("pedal_module", "Pedal Module", 0, 0, [
            "A pressure plate on brass casing: foot pedals for the rudder.",
        ], [item("aeroworks:pedal_module")], xp=15),
        Q("button_panel_module", "Button Panel", 0, 0, [
            "Brass, brass casing and a transmitter: a 2x2 grid of buttons for weapons and gear.",
        ], [item("aeroworks:button_panel_module")], xp=15),
        Q("button_keypad_module", "Button Keypad", 0, 0, [
            "Crafted from a button panel: a 3x3 grid.",
        ], [item("aeroworks:button_keypad_module")], xp=15),
        Q("wheel_module", "Wheel Module", 0, 0, [
            "A valve handle on brass casing: a steering wheel. Dye it any color.",
        ], [item("aeroworks:wheel_module")], xp=15),
        Q("mechanical_servo", "Mechanical Servo", 0, 0, [
            "Precision mechanism, sequenced gearshift, electron tube and brass. Turns to the angle a",
            "redstone signal asks for: drives flaps, rudders and turrets from your controls.",
        ], [item("aeroworks:mechanical_servo")], xp=30),
        Q("stepper_servo", "Stepper Servo", 0, 0, [
            "Same parts as the Mechanical Servo, but it keeps turning step by step while a signal is",
            "held.",
        ], [item("aeroworks:stepper_servo")], xp=25),
        Q("air_weapons", "Aircraft Machine Gun", 0, 0, [
            "&6Create: The Air War&r. Arm your aircraft. (Its launchers and their ammo are removed in this",
            "pack; guns, bombs and missile blocks remain.)",
        ], [item("create_the_air_wars:machinegun")], xp=40),
        Q("minigun", "Minigun", 0, 0, [
            "Spins up, then fires very fast. Power it with redstone.",
        ], [item("create_the_air_wars:minigun")], xp=25),
        Q("air_camera", "Camera", 0, 0, [
            "A camera that feeds a monitor, for remote aiming.",
        ], [item("create_the_air_wars:camera")], xp=20),
        Q("air_monitor", "Monitor (Air War)", 0, 0, [
            "Shows a linked camera's view and controls linked weapons.",
        ], [item("create_the_air_wars:monitor")], xp=20),
        Q("rocket_engine", "Rocket Engine", 0, 0, [
            "Thrust from lava fuel; redstone sets the throttle.",
        ], [item("create_the_air_wars:rocket_engine")], xp=25),
        Q("sc_250", "SC250 Bomb", 0, 0, [
            "&6The Air War&r: titanium sheets, an activator and a big explosive (mechanical",
            "crafting). A free-fall bomb.",
        ], [item("create_the_air_wars:sc_250")], xp=20),
        Q("aim9x", "AIM-9X", 0, 0, [
            "&6The Air War&r: titanium, a chip, wires, an explosive, an activator and a rocket",
            "engine (mechanical crafting). A short-range infrared missile.",
        ], [item("create_the_air_wars:aim9x")], xp=25),
        Q("tomahawk", "Tomahawk", 0, 0, [
            "A long-range guided missile: set its target with the Target Gunner Gadget.",
        ], [item("create_the_air_wars:tomahawk")], xp=30),
        Q("aerial_ordnance", "HE Bomb", 0, 0, [
            "&6CBC Military Supplement&r: aerial bombs for Big Cannons-style payloads.",
        ], [item("cbcmoreshells:he_bomb")], xp=30),
        Q("aphe_bomb", "APHE Bomb", 0, 0, [
            "Mechanical crafting: an AP Shell, iron plates and a propeller. Armor-piercing high",
            "explosive for armored targets.",
        ], [item("cbcmoreshells:aphe_bomb")], xp=20),
        Q("bouncing_bomb", "HE Bouncing Bomb", 0, 0, [
            "Iron sheets, packed guncotton and an &aImpact Fuze&r (pack recipe). Drop it low over water:",
            "it skips along the surface into its target.",
        ], [item("cbcmoreshells:he_bouncing_bomb")], xp=20),
        Q("aerial_torpedo", "Aerial Torpedo", 0, 0, [
            "A &aBasic Torpedo&r fixed to a &aRocket Bracket&r with two iron sheets (pack recipe).",
            "Dropped from aircraft into water, it runs to the target like a ship's torpedo.",
        ], [item("cbcmoreshells:racked_torpedo")], xp=25),
        Q("rocket_bracket", "Rocket Bracket", 0, 0, [
            "Iron bars and iron sheets, makes 2 (pack recipe). Holds rockets and torpedoes under",
            "aircraft; the Dual HE and APHE rockets are built on one.",
        ], [item("cbcmoreshells:rocket_bracket")], xp=20),
        Q("synaxis", "Control Chair", 0, 0, [
            "&6Synaxis&r: precision controls for Sable craft (circuits, Lua, motors and actuators).",
        ], [item("synaxis:control_chair")], xp=40),
        Q("jet", "Jet", 0, 0, [
            "&aMechanical Crafting&r: steel plates, TFMG &aTurbine Blades&r, a blaze burner and a fluid",
            "pipe (pack recipe). Jet thrust for fast aircraft.",
        ], [item("synaxis:jet")], xp=25),
        Q("circuit", "Circuit", 0, 0, [
            "Deploy a precision control circuit blank onto brass casing. Program flight logic",
            "with Cimulink circuits.",
        ], [item("synaxis:circuit")], xp=20),
        Q("hydraulic_actuator", "Hydraulic Linear Actuator", 0, 0, [
            "A mechanical piston, piston pole, shaft, brass casing and a sequenced",
            "gearshift. Pushes and pulls parts of your craft precisely.",
        ], [item("synaxis:hydraulic_linear_actuator")], xp=20),
    ]),
    # ----------------------------------------------------------------------------------------------
    dict(slug="naval", group="warfare", title="Naval",
         subtitle="Create Deep Seas: boats, submarines and torpedoes", icon="create_submarine:ballast_tank",
         unlock=[("brass_and_precision", "next")], quests=[
        Q("rudder", "Rudder", 0, 0, [
            "&6Create: High Seas&r. Boats are Sable physics objects too (see the Physics Assembler in",
            "Aeronautics). A rudder steers.",
        ], [item("create_high_seas:rudder")], xp=20),
        Q("boat_engine", "Boat Engine", 0, 0, [
            "&6Create: High Seas&r: a blast furnace, a propeller and a lever. Burns fuel to drive",
            "your boat.",
        ], [item("create_high_seas:boat_engine")], xp=30),
        Q("anchor", "Anchor", 0, 0, [
            "An iron block, chain, iron sheet and ingot. Drop it to hold your ship in place.",
        ], [item("create_high_seas:anchor")], xp=15),
        Q("buoy", "Buoy", 0, 0, [
            "Red and white wool. Marks a spot on the water: channels, mines, rally points.",
        ], [item("create_high_seas:buoy")], xp=10),
        Q("wind_vane", "Wind Vane", 0, 0, [
            "An arrow and copper. Shows which way the wind blows, for sailing.",
        ], [item("create_high_seas:wind_vane")], xp=10),
        Q("oar", "Oar of Boat", 0, 0, [
            "Sticks and planks. Row a small boat by hand.",
        ], [item("create_high_seas:oar_of_boat")], xp=10),
        Q("ballast", "Ballast Tank", 0, 0, [
            "&6Create Deep Seas&r. Flood and empty &aBallast Tanks&r to dive and surface.",
        ], [item("create_submarine:ballast_tank")], xp=40),
        Q("ballast_vent", "Ballast Vent", 0, 0, [
            "A copper block and copper nuggets. Lets water in and out of the ballast tanks.",
        ], [item("create_submarine:ballast_vent")], xp=15),
        Q("floater", "Floater", 0, 0, [
            "Wool and a phycological membrane. Adds buoyancy so the hull floats higher.",
        ], [item("create_submarine:floater")], xp=15),
        Q("sub_propeller", "Submarine Propeller", 0, 0, [
            "A propeller, industrial iron and a shaft. Thrust under water.",
        ], [item("create_submarine:submarine_propeller")], xp=20),
        Q("water_thruster", "Water Thruster", 0, 0, [
            "A mechanical pump, a copper block and a propeller. A water jet for fine maneuvering.",
        ], [item("create_submarine:water_thruster")], xp=20),
        Q("oxygen", "Electrolyzer", 0, 0, [
            "Makes &aoxygen&r for your crew. Submarines need air.",
        ], [item("create_submarine:electrolyzer")], xp=40),
        Q("diffuser", "Oxygen Diffuser", 0, 0, [
            "A propeller, nozzle, item drain, redstone link and electron tube. Spreads the",
            "electrolyzer's oxygen through the hull.",
        ], [item("create_submarine:oxygene_diffuser")], xp=20),
        Q("decompression", "Decompression Chamber", 0, 0, [
            "Copper sheets, glass and a mechanical pump. Come up from depth without getting the",
            "bends.",
        ], [item("create_submarine:decompression_chamber")], xp=20),
        Q("diving_gear", "Diving Gear", 0, 0, [
            "Copper and andesite alloy. Chestplate and leggings for swimming outside the hull. Wear",
            "them with a Copper Backtank and Diving Helmet.",
        ], [item("create_submarine:diving_chestplate"), item("create_submarine:diving_leggings")], xp=25),
        Q("pressure_goggles", "Pressure Goggles", 0, 0, [
            "Engineer's Goggles, an electron tube and red glass. Shows water pressure at a",
            "glance.",
        ], [item("create_submarine:pressure_goggles")], xp=15),
        Q("command", "Onboard Computer", 0, 0, [
            "A crafter slot cover, planks and a transmitter. The submarine's command console: drive and",
            "dive from here.",
        ], [item("create_submarine:command_sub")], xp=40),
        Q("sub_sonar", "Sonar (Deep Seas)", 0, 0, [
            "See under water. (A different block from the Air War sonar.)",
        ], [item("create_submarine:sonar")], xp=25),
        Q("barometer", "Pressure Barometer", 0, 0, [
            "An iron pressurizer, industrial iron and a water bucket. Measures depth by pressure.",
        ], [item("create_submarine:barometer")], xp=15),
        Q("alarm", "Industrial Alarm", 0, 0, [
            "A redstone lamp, note block, electron tube, iron sheet and red glass. Sounds when it gets",
            "a redstone signal.",
        ], [item("create_submarine:industrial_alarm")], xp=10),
        Q("pump_controller", "Pump Controller", 0, 0, [
            "A copper block, a mechanical pump and a transmitter. Runs the ballast pumps from one",
            "place.",
        ], [item("create_submarine:pump_controller")], xp=20),
        Q("torpedo", "Basic Torpedo", 0, 0, [
            "&6CBC Military Supplement&r: torpedoes are assembled in stages (see JEI) and fired from a",
            "torpedo tube.",
        ], [item("cbcmoreshells:primary_torpedo")], xp=40),
        Q("torpedo_head", "Torpedo Warhead", 0, 0, [
            "Sequenced assembly: iron sheets, packed gunpowder, redstone and a brass nugget. The",
            "explosive end of a torpedo.",
        ], [item("cbcmoreshells:torpedo_head")], xp=20),
        Q("torpedo_tube", "Torpedo Tube", 0, 0, [
            "Iron plates (mechanical crafting) make the chamber; convert it to get the barrel. The",
            "launcher for torpedoes.",
        ], [item("cbcmoreshells:steel_torpedo_tube_chamber"), item("cbcmoreshells:steel_torpedo_tube_barrel")], xp=30),
        Q("depth_charge", "Depth Charge", 0, 0, [
            "Iron sheets, packed guncotton and a &aTimed Fuze&r (pack recipe). Roll it off the stern",
            "over a submarine.",
        ], [item("cbcmoreshells:depth_charge")], xp=20),
        Q("mine", "Underwater Mine", 0, 0, [
            "Industrial iron and TNT. Deny an area of sea to enemy submarines.",
        ], [item("create_submarine:underwater_mine")], xp=20),
        Q("torpedo_detector", "Torpedo Detection Device", 0, 0, [
            "A hydrophone: copper sheets, an electron tube, a note block and brass casing (pack recipe).",
            "Warns you of incoming torpedoes.",
        ], [item("cbcmoreshells:torpedo_detection_device")], xp=25),
    ]),
    # ----------------------------------------------------------------------------------------------
    dict(slug="rail", group="warfare", title="Rail Warfare",
         subtitle="Create trains, Steam 'n' Rails and armored trains", icon="create:controls",
         unlock=[("brass_and_precision", "next")], quests=[
        Q("track", "Train Track", 0, 0, [
            "Sequenced assembly: sleepers, iron nuggets and zinc nuggets (makes 32 at a time). Create",
            "trains run on Train Track.",
        ], [item("create:track", 32)], xp=20),
        Q("station", "Train Station", 0, 0, [
            "Assemble and stop trains at a &aStation&r. Check the Ponder.",
        ], [item("create:track_station")], xp=35),
        Q("signal", "Train Signal", 0, 0, [
            "Train Casing and an electron tube (makes 2). Splits track into blocks so trains don't",
            "collide.",
        ], [item("create:track_signal", 2)], xp=15),
        Q("observer", "Train Observer", 0, 0, [
            "Train Casing and a pressure plate. Outputs redstone when a train passes.",
        ], [item("create:track_observer")], xp=15),
        Q("schedule", "Train Schedule", 0, 0, [
            "Paper and an obsidian sheet. Give it to a train's conductor to run a route on its own.",
        ], [item("create:schedule")], xp=20),
        Q("train_controls", "Train Controls", 0, 0, [
            "Train Casing, a lever and a precision mechanism. Drive the train yourself.",
        ], [item("create:controls")], xp=35),
        Q("railway_casing", "Train Casing", 0, 0, [
            "Brass casing material for train parts (and Quantum Casing).",
        ], [item("create:railway_casing", 4)], xp=15),
        Q("train_door", "Train Door", 0, 0, [
            "Train Casing and a wooden door (makes 2). Doors that work on a moving train.",
        ], [item("create:train_door", 2)], xp=10),
        Q("snr", "Handcar", 0, 0, [
            "&6Steam 'n' Rails&r adds more to trains: a handcar for quick trips.",
        ], [item("railways:handcar")], xp=30),
        Q("semaphore", "Semaphore", 0, 0, [
            "&6Steam 'n' Rails&r: andesite casing, a fence, iron plate and an electron tube. A signal",
            "arm that shows a Train Signal's state.",
        ], [item("railways:semaphore")], xp=15),
        Q("whistle", "Conductor Whistle", 0, 0, [
            "Copper and a brass nugget. Call your train to you.",
        ], [item("railways:conductor_whistle")], xp=15),
        Q("fuel_tank", "Fuel Tank", 0, 0, [
            "A fluid tank and a sturdy sheet. Lets a train run on liquid fuel.",
        ], [item("railways:fuel_tank")], xp=15),
        Q("fuel_interface", "Portable Fuel Interface", 0, 0, [
            "Train Casing and a chute. Refuel a train while it waits at a station.",
        ], [item("railways:portable_fuel_interface")], xp=15),
        Q("armored_train", "Train Lock", 0, 0, [
            "&6Create: Who Touched My Train&r: lock your train against other teams. In this pack, train",
            "blocks also resist cannon fire (&6CBC: Locometal Armor&r, server-side).",
        ], [item("who_touched_my_train:train_lock")], xp=40),
        Q("iron_key", "Iron Key", 0, 0, [
            "&6Who Touched My Train&r: iron. Lock your train so only key holders can drive it.",
        ], [item("who_touched_my_train:iron_key")], xp=10),
        Q("gold_key", "Gold Key", 0, 0, [
            "Gold, gold nuggets and a golden sheet. A key that opens more of your trains.",
        ], [item("who_touched_my_train:gold_key")], xp=15),
        Q("locometal", "Riveted Locometal", 0, 0, [
            "Stonecut an iron block. Steam 'n' Rails' armored train plating. With &6CBC Locometal",
            "Armor&r it resists cannon fire.",
        ], [item("railways:riveted_locometal", 8)], xp=15),
        Q("psi", "Portable Storage Interface", 0, 0, [
            "Moves items between a moving train (or ship, or vehicle) and storage at a station.",
            "Place one on the train and one facing it on the platform. Supply runs to the front.",
        ], [item("create:portable_storage_interface", 2)], xp=25),
    ]),
    # ----------------------------------------------------------------------------------------------
    dict(slug="armored", group="warfare", title="Armored Vehicles",
         subtitle="Wheels, tank treads, armor plate and vehicle cannons", icon="bits_n_tracks:tank_tread",
         unlock=[("brass_and_precision", "next")], quests=[
        Q("wheel_mount", "Wheel Mount", 0, 0, [
            "&6Offroad&r: ground vehicles are Sable physics objects (see the Physics Assembler in",
            "Aeronautics). Mount wheels on a &aWheel Mount&r.",
        ], [item("offroad:wheel_mount", 4)], xp=25),
        Q("tires", "Tire", 0, 0, [
            "&6Offroad&r: dried kelp and a shaft (makes 4). Standard wheels for a ground vehicle.",
        ], [item("offroad:tire", 4)], xp=30),
        Q("small_tire", "Small Tire", 0, 0, [
            "A shaft and dried kelp (makes 4). Light vehicles.",
        ], [item("offroad:small_tire", 4)], xp=10),
        Q("large_tire", "Large Tire", 0, 0, [
            "A belt and a shaft (makes 4). Heavier vehicles.",
        ], [item("offroad:large_tire", 4)], xp=15),
        Q("monstrous_tire", "Monstrous Tire", 0, 0, [
            "A dried kelp block and a shaft (makes 4). For the biggest builds.",
        ], [item("offroad:monstrous_tire", 4)], xp=20),
        Q("rockcutting_wheel", "Rock Cutting Wheel", 0, 0, [
            "A Crushing Wheel, industrial iron and iron plates. A wheel that cuts through",
            "terrain as it drives.",
        ], [item("offroad:rockcutting_wheel")], xp=20),
        Q("tracks", "Tank Tread", 0, 0, [
            "&6Create: Bits 'n' Tracks&r: Sable-driven &atank treads&r. Check the Ponder for a track setup.",
        ], [item("bits_n_tracks:tank_tread", 16)], xp=40),
        Q("grouser", "Grouser", 0, 0, [
            "Industrial iron and iron nuggets (makes 8). The cleats that give tank treads grip.",
        ], [item("bits_n_tracks:grouser", 8)], xp=15),
        Q("suspension", "Suspension Piece", 0, 0, [
            "A sturdy sheet, a spring, a shaft and zinc nuggets (makes 4). Smooths the ride over",
            "rough ground.",
        ], [item("bits_n_tracks:suspension_piece", 4)], xp=15),
        Q("industrial_belt", "Industrial Belt", 0, 0, [
            "A belt and iron nuggets (makes 4). The heavy drive belt tank treads are built",
            "around.",
        ], [item("bits_n_tracks:industrial_belt", 4)], xp=15),
        Q("flanged_cog", "Flanged Cogwheel", 0, 0, [
            "Two cogwheels and an industrial belt (makes 4). The sprocket that drives the treads.",
        ], [item("bits_n_tracks:flanged_cogwheel", 4)], xp=15),
        Q("armor", "Hardened Steel Armor", 0, 0, [
            "&6Rolled Homogeneous Armor&r: armor plating in many camo colors. Protects against cannon",
            "fire. Cut an &airon block&r in a &astonecutter&r (any color, also layered, riveted and",
            "slashed styles).",
        ], [item("rha:hardsteelolive", 16)], xp=40),
        # owner-facing fix 2026-11-21: RHA hatches have no recipe and rha:hatcholive is not registered
        # (game saved it as ftbquests:missing_item), so sandbags replace the old Armored Hatch quest.
        Q("sandbags", "Sandbags", 0, 0, [
            "Also from the stonecutter (iron block). Cheap cover for gun nests and trenches.",
        ], [item("rha:sandbaggreen", 8)], xp=15),
        Q("arcon", "Arcon Cannon Barrel", 0, 0, [
            "&6Create: Armored Constructs&r: a tank gun. Assemble Breech, Barrel sections, an",
            "Intermediate Muzzle and a Muzzle in a line. Pack recipes (the mod ships without any):",
            "&aMechanical Crafting&r from heavy plates and steel. Barrels come 2 at a time.",
        ], [item("arcon:arcon_cannon_barrel")], xp=50),
        Q("arcon_muzzle", "Arcon Cannon Muzzle", 0, 0, [
            "Steel plates, steel and a heavy plate (mechanical crafting).",
        ], [item("arcon:arcon_cannon_muzzle")], xp=20),
        Q("arcon_breech", "Arcon Barrel Section (Breech)", 0, 0, [
            "Where the round goes in: heavy plates, steel plates, steel blocks and a &aSteel",
            "Mechanism&r (mechanical crafting).",
        ], [item("arcon:arcon_barrel_section")], xp=20),
        Q("hull_rolled", "Rolled Hull Armor", 0, 0, [
            "&6Armored Constructs&r hull armor stops shells by its &atoughness&r and weighs the",
            "vehicle down by its &amass&r. Rolled steel is the baseline: steel, steel plates and a",
            "heavy plate, makes 8. A &astonecutter&r recolors any hull (15 camouflage patterns).",
        ], [item("arcon:hull_rolled_green", 16)], xp=40),
        Q("hull_nickel", "Nickel Hull Armor", 0, 0, [
            "Tougher and heavier than rolled steel: TFMG nickel, heavy plates and a steel block.",
        ], [item("arcon:hull_nickel_green", 8)], xp=30),
        Q("hull_ceramic", "Ceramic Hull Armor", 0, 0, [
            "Much tougher, and lighter than steel: fireclay, heavy plates and a diamond.",
        ], [item("arcon:hull_ceramic_green", 8)], xp=40),
        Q("hull_boron", "Boron Hull Armor", 0, 0, [
            "The toughest armor: coal coke, heavy plates and netherite scrap (mechanical crafting).",
        ], [item("arcon:hull_boron_green", 8)], xp=60),
        Q("hull_aluminum", "Aluminum Hull Armor", 0, 0, [
            "For aircraft: barely any mass, light protection. Aluminum sheets around a steel plate.",
        ], [item("arcon:hull_aluminum_neutral_gray", 16)], xp=30),
        Q("hull_titanium", "Titanium Hull Armor", 0, 0, [
            "Aircraft armor that takes more hits: Air War titanium sheets around an aluminum sheet.",
        ], [item("arcon:hull_titanium_neutral_gray", 8)], xp=40),
        Q("bops", "BOPS Armor-Piercing Shell", 0, 0, [
            "An AP shot in a brass case: AP Shot, two brass sheets and packed guncotton. Firing leaves a",
            "&aSpent Cartridge Casing&r; reload it with an AP Shot and guncotton.",
        ], [item("arcon:bops", 8)], xp=25),
    ]),
    # ----------------------------------------------------------------------------------------------
    dict(slug="drones", group="warfare", title="Drones",
         subtitle="Create: Droneworks and FPV drones", icon="droneworks:drone_core",
         unlock=[("brass_and_precision", "next")], quests=[
        Q("drone_core", "Drone Core", 0, 0, [
            "&6Create: Droneworks Simulated&r: the heart of a drone. Check the Ponder for a basic build.",
        ], [item("droneworks:drone_core")], xp=40),
        Q("drone_blade", "Drone Blade", 0, 0, [
            "A sail frame, black dye and iron (makes 4). Rotor blades.",
        ], [item("droneworks:drone_blade", 4)], xp=15),
        Q("drone_propeller", "Drone Propeller", 0, 0, [
            "An Andesite Propeller and a Gimbal Sensor (makes 4). Drone lift and thrust.",
        ], [item("droneworks:drone_propeller", 4)], xp=15),
        Q("tilting_bearing", "Tilting Propeller Bearing", 0, 0, [
            "A Propeller Bearing and a Gimbal Sensor. Tilts its rotor to steer the drone.",
        ], [item("droneworks:tilting_propeller_bearing")], xp=20),
        Q("flap_bearing", "Flap Bearing", 0, 0, [
            "A mechanical bearing, torsion spring, clutch and gearshift. Moves control surfaces.",
        ], [item("droneworks:flap_bearing")], xp=15),
        Q("drone_camera", "Drone Camera", 0, 0, [
            "Iron, a spyglass and a transmitter. Sends what the drone sees to your remote.",
        ], [item("droneworks:drone_camera")], xp=35),
        Q("drone_hub", "Drone Hub", 0, 0, [
            "An iron block and black dye. A base where drones land and recharge.",
        ], [item("droneworks:drone_hub")], xp=20),
        Q("remote", "Drone Remote Controller", 0, 0, [
            "A transmitter, precision mechanism and compass. Fly drones wirelessly.",
        ], [item("droneworks:drone_remote_control")], xp=40),
        Q("drone_controls", "Drone Controls", 0, 0, [
            "Six transmitters, a gyroscopic mechanism and brass casing. The drone's on-board flight",
            "controller.",
        ], [item("droneworks:drone_controls")], xp=15),
        Q("commander_seat", "Commander Seat", 0, 0, [
            "A seat, a transmitter and a precision mechanism. Command your drones from a vehicle.",
        ], [item("droneworks:commander_seat")], xp=20),
        Q("fpv", "FPV Drone", 0, 0, [
            "&6Create: The Air War&r: a first-person attack drone. Four Andesite Propellers, a gyro",
            "stabilizer, antenna, camera and packed guncotton (pack recipe). Place it, link it with the",
            "Drone Joystick, and fly it into the target.",
        ], [item("create_the_air_wars:fpv_drone")], xp=50),
        Q("drone_joystick", "Drone Joystick", 0, 0, [
            "Brass sheets, an antenna, a monitor and an electron tube (pack recipe). Links to and flies",
            "FPV drones.",
        ], [item("create_the_air_wars:drone_controller")], xp=20),
    ]),
    # ----------------------------------------------------------------------------------------------
    # Create: Warnautics (mod ID cbc_more_content), owner 2026-11-21. Recipes read from the jar.
    dict(slug="demolitions", group="warfare", title="Demolitions",
         subtitle="Create: Warnautics bombs, mines, C4 and missiles", icon="cbc_more_content:moab",
         unlock=[("artillery", "shells")], quests=[
        Q("guncotton", "Packed Guncotton", 0, 0, [
            "Every Warnautics explosive uses &aPacked Guncotton&r, Big Cannons' high explosive",
            "(check JEI for how it's made).",
        ], [item("createbigcannons:packed_guncotton", 4)], xp=30),
        Q("tripwire_coil", "Tripwire Coil", 0, 0, [
            "String, guncotton and iron nuggets (makes 2). Booby-trap a doorway.",
        ], [item("cbc_more_content:tripwire_coil", 2)], xp=15),
        Q("wire_cutters", "Wire Cutters", 0, 0, [
            "Iron plate, nuggets and red wool. Safely cut enemy tripwires.",
        ], [item("cbc_more_content:wire_cutters")], xp=15),
        Q("small_bomb", "Small Bomb", 0, 0, [
            "&6Create: Warnautics&r: bombs fall with &aBig Cannons ballistics&r. Cast iron, iron plate,",
            "guncotton and a powder charge. Combine two for a bigger rack.",
        ], [item("cbc_more_content:small_bomb", 4)], xp=30),
        Q("bombsight", "Bombsight", 0, 0, [
            "Iron plates, glass, a compass and redstone. Aim your drops from the air.",
        ], [item("cbc_more_content:bombsight")], xp=20),
        Q("small_mine", "Small Mine", 0, 0, [
            "Gunpowder, iron plate, shot balls and a pressure plate.",
        ], [item("cbc_more_content:small_mine", 4)], xp=15),
        Q("bounding_mine", "Bounding Mine", 0, 0, [
            "Jumps up before it goes off. Tripwire hook trigger.",
        ], [item("cbc_more_content:bounding_mine", 2)], xp=15),
        Q("claymore", "M18A1 Claymore", 0, 0, [
            "A directional mine: the blast goes one way.",
        ], [item("cbc_more_content:claymore", 2)], xp=15),
        Q("medium_bomb", "Medium Bomb", 0, 0, [
            "&aMechanical Crafting&r: adds wooden slabs and an &aImpact Fuze&r to the small bomb's",
            "ingredients.",
        ], [item("cbc_more_content:medium_bomb", 2)], xp=40),
        Q("rocket_pod", "Rocket Pod Section", 0, 0, [
            "Iron plates, a dispenser and redstone. Mount it on an aircraft.",
        ], [item("cbc_more_content:rocket_pod")], xp=20),
        Q("s8_rocket", "S-8 Rocket", 0, 0, [
            "Iron plate, gunpowder and blaze powder (makes 2). Ammunition for rocket pods.",
        ], [item("cbc_more_content:s8_rocket", 8)], xp=15),
        Q("sea_mine", "Sea Mine", 0, 0, [
            "Copper, iron nuggets and guncotton. Guards a harbor.",
        ], [item("cbc_more_content:sea_mine", 2)], xp=20),
        Q("sea_torpedo", "Sea Torpedo", 0, 0, [
            "Mechanical crafting with a propeller and an impact fuze. Sinks ships.",
        ], [item("cbc_more_content:sea_bomb")], xp=25),
        Q("large_bomb", "Large Bomb", 0, 0, [
            "The medium bomb's recipe plus &aSturdy Sheets&r.",
        ], [item("cbc_more_content:large_bomb")], xp=50),
        Q("large_mine", "Large Mine", 0, 0, [
            "Cast iron, iron plate, guncotton and a heavy pressure plate. Stops vehicles.",
        ], [item("cbc_more_content:large_mine", 2)], xp=20),
        Q("siren", "Air-Raid Siren", 0, 0, [
            "Iron plates, copper, a note block and a shaft. Warn your base when bombers come.",
        ], [item("cbc_more_content:siren")], xp=15),
        Q("c4", "C4 Charge", 0, 0, [
            "Mechanical crafting: brass plates, an electron tube, a &aWired Fuze&r, a powder charge,",
            "redstone, string and guncotton. Stick it to a wall and set it off remotely.",
        ], [item("cbc_more_content:c4", 2)], xp=50),
        Q("detonator", "Detonator", 0, 0, [
            "Redstone torch, lever, copper and iron plate. Sets off your C4.",
        ], [item("cbc_more_content:detonator")], xp=20),
        Q("bomb_vest", "Bomb Vest", 0, 0, [
            "Mechanical crafting with C4 and a leather chestplate.",
        ], [item("cbc_more_content:bomb_vest")], xp=20),
        Q("cruise_missile", "Cruise Missile", 0, 0, [
            "Mechanical crafting: precision mechanism, electron tube, brass and sturdy sheets, a",
            "propeller, a powder charge, guncotton and an impact fuze.",
        ], [item("cbc_more_content:cruise_missile")], xp=60),
        Q("target_designator", "Target Designator", 0, 0, [
            "Electron tube, iron plates, brass nuggets and redstone. Marks targets.",
        ], [item("cbc_more_content:target_designator")], xp=25),
        Q("aim9", "AIM-9 Sidewinder", 0, 0, [
            "An air-to-air missile. Mechanical crafting with a &aProximity Fuze&r and a precision",
            "mechanism.",
        ], [item("cbc_more_content:aim9")], xp=40),
        Q("moab", "MOAB", 0, 0, [
            "The biggest bomb. Mechanical crafting around a Large Bomb, with a precision mechanism and",
            "sturdy sheets. &cBe careful where you drop it.&r",
        ], [item("cbc_more_content:moab")], xp=100),
    ]),
    # ----------------------------------------------------------------------------------------------
    # Nuclear (owner 2026-11-22: "a good nuclear mod to add to the chaos"). Create Nuclear reactors and
    # radiation; nuke shells from CBC Enhanced Shells, re-gated on uranium rods by
    # pack/kubejs/server_scripts/nuclear_weapons.js. Recipe chain read from createnuclear-2.0.1's jar.
    dict(slug="nuclear", group="ages", title="Nuclear Age",
         subtitle="Reactors, radiation, and the shells that end wars", icon="cbc_enhanced_shells:nuke_shell",
         unlock=[("industrial", "steel")], quests=[
        Q("raw_uranium", "Uranium", 0, 0, [
            "&6Create Nuclear&r: uranium and thorium ores generate underground.",
            "&cUranium is radioactive.&r Carry too much for too long and you get &cRadiation&r. Store it,",
            "don't hoard it in your pockets.",
        ], [item("createnuclear:raw_uranium", 8)], xp=40),
        Q("raw_thorium", "Thorium", 0, 0, [
            "The second reactor fuel: weaker than uranium, but it runs cooler.",
        ], [item("createnuclear:raw_thorium", 4)], xp=20),
        Q("thorium_ingot", "Thorium Ingot", 0, 0, [
            "Crush raw thorium into dust, turn it into &aliquid thorium&r, and compact it in a basin",
            "(check JEI for every step).",
        ], [item("createnuclear:thorium_ingot", 4)], xp=25),
        Q("thorium_rod", "Thorium Rod", 0, 0, [
            "&aMechanical Crafting&r from thorium ingots.",
        ], [item("createnuclear:thorium_rod", 2)], xp=30),
        Q("uranium_powder", "Uranium Powder", 0, 0, [
            "Crush raw uranium (Crushing Wheels), then crush the crushed uranium again. Crushing",
            "&agranite&r also gives a little.",
        ], [item("createnuclear:uranium_powder", 16)], xp=30),
        Q("enriched_soul_soil", "Enriched Soul Soil", 0, 0, [
            "Soul soil, obsidian and a &5Nether Star&r.",
        ], [item("createnuclear:enriched_soul_soil")], xp=30),
        Q("enriching_campfire", "Enriching Campfire", 0, 0, [
            "Logs and sticks around Enriched Soul Soil. Its green fire &aenriches&r anything an",
            "encased fan blows through it, the same way soul fire haunts.",
        ], [item("createnuclear:enriching_campfire")], xp=30),
        Q("yellowcake", "Yellowcake", 0, 0, [
            "Turn uranium powder into &aliquid uranium&r (check JEI), then compact it in a basin.",
        ], [item("createnuclear:yellowcake", 8)], xp=40),
        Q("enriched_yellowcake", "Enriched Yellowcake", 0, 0, [
            "Blow yellowcake through the &aEnriching Campfire&r with an encased fan.",
        ], [item("createnuclear:enriched_yellowcake", 8)], xp=50),
        Q("hazmat", "Anti-Radiation Suit", 0, 0, [
            "Brass, lead and graphite rods. Wear the full set around reactors and fuel.",
            "Any lead works.",
        ], [item("createnuclear:default_anti_radiation_helmet"), item("createnuclear:default_anti_radiation_chestplate"),
            item("createnuclear:default_anti_radiation_leggings"), item("createnuclear:default_anti_radiation_boots")],
          xp=60),
        Q("graphene", "Graphene", 0, 0, [
            "Press coal dust.",
        ], [item("createnuclear:graphene", 4)], xp=20),
        Q("graphite_rod", "Graphite Rod", 0, 0, [
            "&aMechanical Crafting&r: steel and graphene. Graphite rods &bcool&r a reactor.",
        ], [item("createnuclear:graphite_rod", 4)], xp=30),
        Q("uranium_rod", "Uranium Rod", 0, 0, [
            "&aMechanical Crafting&r from enriched yellowcake. Reactor fuel, and the core of every",
            "nuclear shell.",
        ], [item("createnuclear:uranium_rod", 4)], xp=60),
        Q("reactor_blueprint", "Reactor Blueprint", 0, 0, [
            "Steel, a display board, an empty schematic and a precision mechanism. It shows where",
            "every reactor part goes.",
        ], [item("createnuclear:reactor_blueprint_item")], xp=30),
        Q("reactor_casing", "Reactor Casing", 0, 0, [
            "Apply steel to a brass casing.",
        ], [item("createnuclear:reactor_casing", 16)], xp=30),
        Q("reactor_frame", "Reactor Frame", 0, 0, [
            "&aMechanical Crafting&r: casing, steel, reinforced glass (glass and lead) and a bucket.",
        ], [item("createnuclear:reactor_frame", 4)], xp=30),
        Q("reactor_core", "Reactor Core", 0, 0, [
            "&aMechanical Crafting&r: casing, steel, a precision mechanism and a bucket of liquid",
            "uranium.",
        ], [item("createnuclear:reactor_core")], xp=40),
        Q("nitrogen", "Coolant", 0, 0, [
            "Smelt nitrate ore into &bnitrogen concentrate&r, then fan it through &bpowder snow&r.",
            "Nitrogen coolant keeps bigger reactors from melting down.",
        ], [item("createnuclear:cooled_nitrogen_concentrate", 4)], xp=30),
        Q("reactor_controller", "Reactor Controller", 0, 0, [
            "&aMechanical Crafting&r: a &5Nether Star&r, netherite, an item vault and casings.",
            "Build the reactor the blueprint shows, load rods, and it makes &6millions of SU&r.",
            "&cIf it overheats, it melts down:&r a nuclear explosion that leaves a &cWasteland&r",
            "biome behind. Everyone within 256 blocks gets a warning first. A reactor is a target.",
        ], [item("createnuclear:reactor_controller")], xp=150),
        Q("nuke_shell", "Nuclear Shell", 0, 0, [
            "&aMechanical Crafting&r: a Big Cannons &cHE Shell&r wrapped in 8 uranium rods and lead,",
            "with a &5Nether Star&r core. A mushroom cloud, and a blast that levels whole bases.",
            "&cClaims &omaybe&r&c won't save anyone.&r Fire it from very far away, and never at home.",
        ], [item("cbc_enhanced_shells:nuke_shell")], xp=250),
        Q("h_bomb_mini", "Mini H-Bomb", 0, 0, [
            "Four nuclear shells, end crystals and nether stars: a smaller thermonuclear shell.",
        ], [item("cbc_enhanced_shells:h_bomb_mini_shell")], xp=300),
        Q("nuke_shell_mk2", "Nuclear Shell Mk.II", 0, 0, [
            "&aMechanical Crafting&r: a nuclear shell with more uranium, thorium rods and enriched",
            "yellowcake. Bigger.",
        ], [item("cbc_enhanced_shells:nuke_shell_mk2")], xp=400),
        Q("h_bomb", "H-Bomb", 0, 0, [
            "&cThe end of the war.&r Three Mk.II nuclear shells, end crystals and nether stars. A",
            "thermonuclear dome and a shockwave in rings. There is nothing bigger.",
        ], [item("cbc_enhanced_shells:h_bomb_shell")], xp=750, levels=30, rolls=[("war_trophy", 2)],
          shape="hexagon"),
    ]),
    # ----------------------------------------------------------------------------------------------
    # Know Your Enemy (owner 2026-11-21: "mobs quests"). Improved Mobs, Enhanced AI, Trigger Mobs, AMBUSH.
    # None of these add new mob types; they upgrade vanilla ones, so these are kill tasks on vanilla mobs.
    dict(slug="enemy", group="warfare", title="Know Your Enemy",
         subtitle="Smarter, tougher, armed mobs and enemy fleets", icon="minecraft:zombie_head",
         unlock=[("welcome", "next")], quests=[
        Q("first_blood", "First Blood", 0, 0, [
            "&6Improved Mobs&r: mobs get stronger the longer you play. The &dDifficulty&r number",
            "(bottom right) goes up over time. Higher difficulty means better gear, more health, and",
            "mobs that break blocks to reach you.",
        ], [kill("minecraft:zombie", 10)], xp=20, items=[("minecraft:shield", 1)]),
        Q("spider", "Spiders", 0, 0, ["They climb walls. Walls alone will not stop them."], [kill("minecraft:spider", 5)], xp=10),
        Q("husk", "Husks", 0, 0, ["Desert zombies. They make you hungry."], [kill("minecraft:husk", 5)], xp=10),
        Q("zombie_villager", "Zombie Villagers", 0, 0, ["Cure one with a golden apple and weakness."], [kill("minecraft:zombie_villager", 3)], xp=10),
        Q("skeleton", "Snipers", 0, 0, [
            "&6Enhanced AI&r: skeletons aim better and keep their distance. Fight from cover.",
        ], [kill("minecraft:skeleton", 10)], xp=25),
        Q("stray", "Strays", 0, 0, ["Slowness arrows in cold biomes."], [kill("minecraft:stray", 5)], xp=10),
        Q("bogged", "Bogged", 0, 0, ["Poison arrows from swamps and trial chambers."], [kill("minecraft:bogged", 3)], xp=10),
        Q("creeper", "Breachers", 0, 0, [
            "&6Enhanced AI&r: creepers &cbreach walls&r on purpose, and zombies dig to reach you. Build",
            "thick walls, or something they cannot dig through.",
        ], [kill("minecraft:creeper", 5)], xp=25),
        Q("enderman", "Endermen", 0, 0, ["Do not look them in the eye."], [kill("minecraft:enderman", 3)], xp=15),
        Q("witch", "Witches", 0, 0, ["Kill them before they drink a potion."], [kill("minecraft:witch", 2)], xp=15),
        Q("armed", "Armed and Dangerous", 0, 0, [
            "&6Trigger Mobs&r: some mobs spawn &ccarrying guns&r and fire them at you. Armor up and",
            "keep moving.",
        ], [kill("minecraft:zombie", 25)], xp=40),
        Q("raiders", "Raiders", 0, 0, [
            "Pillagers patrol and raid villages with crossbows. &6CTOV&r outposts are styled to each",
            "biome, and &6Create: Pillager Arise&r adds mechanized pillager bases: towers, camps, a",
            "fortress gate, a cathedral, even a pillager village and a blimp.",
        ], [kill("minecraft:pillager", 10)], xp=30),
        Q("vindicator", "Vindicators", 0, 0, ["Axes. Shield up."], [kill("minecraft:vindicator", 5)], xp=15),
        Q("evoker", "Evoker", 0, 0, ["Fangs and vexes. Drops a Totem of Undying."], [kill("minecraft:evoker")], xp=25),
        Q("ravager", "Ravager", 0, 0, ["A raid's heavy armor."], [kill("minecraft:ravager")], xp=25),
        # Illager Invasion (owner 2026-11-22: "more pillager things"). Entity IDs from the live registry.
        Q("invasion", "Illager Invasion", 0, 0, [
            "&6Illager Invasion&r: a whole new illager army. They join raids, and guard new structures:",
            "&cIllager Forts&r, &cLabyrinths&r, &cIllusioner Towers&r, and Firecaller and Sorcerer huts.",
            "Start with the &aProvoker&r.",
        ], [kill("illagerinvasion:provoker", 3)], xp=40),
        Q("basher", "Basher", 0, 0, ["A shield-bearing brute. Get around the shield."],
          [kill("illagerinvasion:basher", 3)], xp=15),
        Q("marauder", "Marauder", 0, 0, ["Throws hatchets from range."], [kill("illagerinvasion:marauder", 3)], xp=15),
        Q("inquisitor", "Inquisitor", 0, 0, ["The heavy infantry of the invasion."],
          [kill("illagerinvasion:inquisitor", 2)], xp=25),
        Q("alchemist", "Alchemist", 0, 0, ["Throws potions. Kill it before it supports the rest."],
          [kill("illagerinvasion:alchemist", 2)], xp=20),
        Q("firecaller", "Firecaller", 0, 0, ["A fire caster. Found at Firecaller huts."],
          [kill("illagerinvasion:firecaller", 2)], xp=20),
        Q("sorcerer", "Sorcerer", 0, 0, ["A magic caster. Found at Sorcerer huts."],
          [kill("illagerinvasion:sorcerer", 2)], xp=20),
        Q("archivist", "Archivist", 0, 0, ["A spellcaster scholar of the illagers."],
          [kill("illagerinvasion:archivist", 2)], xp=20),
        Q("necromancer", "Necromancer", 0, 0, ["Raises the dead as Surrendered. Kill the caster first."],
          [kill("illagerinvasion:necromancer", 2)], xp=25),
        Q("surrendered", "Surrendered", 0, 0, ["The Necromancer's undead illagers."],
          [kill("illagerinvasion:surrendered", 5)], xp=15),
        Q("invoker", "The Invoker", 0, 0, [
            "&cBoss:&r the Invoker leads the invasion, with a boss bar and fangs. Bring a team.",
        ], [kill("illagerinvasion:invoker")], xp=150, levels=10, rolls=[("war_trophy", 1)], shape="hexagon"),
        Q("ambush", "Ambush!", 0, 0, [
            "&6Create Aeronautics: AMBUSH&r: enemies attack in planned &cambushes&r and &cinvasions&r,",
            "including &cairships, armored cars and anti-air&r built with the same Create tech you",
            "use. Enemy airships can appear on their own.",
            "&aPrepare:&r radar to see them coming (Radar chapter), anti-air guns, and an air-raid",
            "siren.",
        ], [CHECK], xp=50),
        Q("nether", "Into the Nether", 0, 0, [
            "Thin air down here too (see Pollution and Air): bring a backtank.",
        ], [kill("minecraft:blaze", 10)], xp=30),
        Q("wither_skeleton", "Wither Skeletons", 0, 0, ["Their skulls summon the Wither."], [kill("minecraft:wither_skeleton", 5)], xp=20),
        Q("ghast", "Ghasts", 0, 0, ["Hit their fireballs back."], [kill("minecraft:ghast", 3)], xp=15),
        Q("piglin_brute", "Piglin Brute", 0, 0, ["Bastion guards. They never calm down."], [kill("minecraft:piglin_brute")], xp=25),
        Q("elder_guardian", "Elder Guardian", 0, 0, ["Ocean monument boss. Mining Fatigue."], [kill("minecraft:elder_guardian")], xp=40),
        Q("wither", "The Wither", 0, 0, [
            "A boss that destroys blocks. Fight it far from your base.",
        ], [kill("minecraft:wither")], xp=100),
        Q("ender_dragon", "The Ender Dragon", 0, 0, [
            "&6Stellarity&r: the dragon is &cnot there when you arrive&r. You summon it: place &a4 End",
            "Crystals&r on the 4 sparkling spots around the exit portal at the center of the main island.",
            "It's a real boss: 300 health, armor, and invulnerable while any crystal stands.",
            "&cNo air in the End&r: bring backtanks and air bladders.",
        ], [kill("minecraft:ender_dragon")], xp=100),
        Q("warden", "The Warden", 0, 0, ["Deep dark. Probably best avoided."], [kill("minecraft:warden")], xp=100),
    ]),
    # ----------------------------------------------------------------------------------------------
    # Defend Your Home (owner 2026-11-21): a ladder of AMBUSH waves the player calls in, getting harder.
    # Each quest: checkmark (starting the quest fires the ambush via its tag) + kill goal. Waves 1-4 are
    # custom definitions in pack/kubejs/data/createwars/ambushes/; 5-8 are AMBUSH's own vehicles/ships.
    dict(slug="defense", group="warfare", title="Defend Your Home",
         subtitle="Call in enemy waves: each one harder, each one richer", icon="minecraft:bell",
         unlock=[("enemy", "ambush")], quests=[
        Q("wave_scouts", "Wave 1: Scouting Party", 0, 0, [
            "Zombies and skeletons probe your walls.",
            "&aClick the checkmark when you're ready&r (quest edit mode OFF): the attack starts on the spot. Fight near your base.",
        ], [CHECK, kill("minecraft:zombie", 4)], xp=150, levels=3, rolls=[("war_spoils_1", 2)], bonus=False,
          tags=["ambush:trigger:createwars:quest_scouting_party"]),
        Q("wave_raiders", "Wave 2: Raiding Party", 0, 0, [
            "Pillagers and vindicators, led by a &cRaid Captain&r.",
            "&aClick the checkmark when you're ready&r (quest edit mode OFF): the attack starts on the spot. Fight near your base.",
        ], [CHECK, kill("minecraft:pillager", 6)], xp=250, levels=5, rolls=[("war_spoils_1", 3)], bonus=False,
          tags=["ambush:trigger:createwars:quest_raiding_party"]),
        Q("wave_warband", "Wave 3: Warband", 0, 0, [
            "A bigger illager band with an &5Evoker&r leader. Watch for fangs and vexes.",
            "&aClick the checkmark when you're ready&r (quest edit mode OFF): the attack starts on the spot. Fight near your base.",
        ], [CHECK, kill("minecraft:vindicator", 4), kill("minecraft:evoker", 1)], xp=400, levels=7,
          rolls=[("war_spoils_2", 3)], bonus=False, tags=["ambush:trigger:createwars:quest_warband"]),
        Q("wave_siege", "Wave 4: Siege", 0, 0, [
            "A &cRavager&r leads the assault, with illagers and witches behind it. It breaks crops and",
            "walls. Bring friends.",
            "&aClick the checkmark when you're ready&r (quest edit mode OFF): the attack starts on the spot. Fight near your base.",
        ], [CHECK, kill("minecraft:ravager", 1)], xp=600, levels=10, rolls=[("war_spoils_2", 4)], bonus=False,
          tags=["ambush:trigger:createwars:quest_siege"]),
        Q("wave_drill_car", "Wave 5: Armored Drill Car", 0, 0, [
            "An illager &6armored car&r with a drill, built from real Create parts, rolls in. Stop the",
            "crew. Cannons help.",
            "&aClick the checkmark when you're ready&r (quest edit mode OFF): the attack starts on the spot. Fight near your base.",
        ], [CHECK, kill("minecraft:pillager", 3)], xp=800, levels=12, rolls=[("war_spoils_3", 3)], bonus=False,
          tags=["ambush:trigger:ambush:_illager_drill_car"]),
        Q("wave_patrol_ship", "Wave 6: Patrol Airship", 0, 0, [
            "An illager &6airship&r on patrol finds your base. Shoot it down: autocannons and",
            "anti-air.",
            "&aClick the checkmark when you're ready&r (quest edit mode OFF): the attack starts on the spot. Fight near your base.",
        ], [CHECK, kill("minecraft:pillager", 4)], xp=1000, levels=15, rolls=[("war_spoils_3", 4)], bonus=False,
          tags=["ambush:trigger:ambush:_illager_patrol_ship"]),
        Q("wave_antiair", "Wave 7: Anti-Air Battery", 0, 0, [
            "A cast-iron &6anti-air car&r with a heavy crew. Your aircraft are its targets.",
            "&aClick the checkmark when you're ready&r (quest edit mode OFF): the attack starts on the spot. Fight near your base.",
        ], [CHECK, kill("minecraft:pillager", 6)], xp=1200, levels=18, rolls=[("war_spoils_3", 5)], bonus=False,
          tags=["ambush:trigger:ambush:_castiron_antiair_car"]),
        Q("wave_storm_breaker", "Wave 8: The Storm Breaker", 0, 0, [
            "&cBoss:&r the &6Storm Breaker&r, a high-altitude battle airship with escorts. Radar to find",
            "it, guns to bring it down, oxygen to chase it up high.",
            "&aClick the checkmark when you're ready&r (quest edit mode OFF): the attack starts on the spot. Fight near your base.",
        ], [CHECK, kill("minecraft:pillager", 8)], xp=2000, levels=30,
          rolls=[("war_spoils_3", 5), ("war_trophy", 1)], bonus=False, shape="hexagon",
          tags=["ambush:trigger:ambush:_storm_breaker_boss_high_altitude_ship"]),
    ]),
    # ----------------------------------------------------------------------------------------------
    # Infrastructure (owner 2026-11-21): food and storage. Recipes read from the jars.
    dict(slug="food", group="infrastructure", title="Food",
         subtitle="Farmer's Delight cooking, then Create: Slice and Dice automation",
         icon="farmersdelight:cooking_pot", unlock=[("welcome", "next")], quests=[
        Q("knife", "Flint Knife", 0, 0, [
            "&6Farmer's Delight&r: a &aknife&r cuts food, harvests straw from grass, and gets more",
            "drops from animals. Flint and a stick.",
        ], [item("farmersdelight:flint_knife")], xp=10),
        Q("cutting_board", "Cutting Board", 0, 0, [
            "Place it, put food on it, and right-click with a &aknife&r (or axe, pickaxe, shovel).",
            "Planks and sticks.",
        ], [item("farmersdelight:cutting_board")], xp=20),
        Q("straw", "Straw", 0, 0, [
            "Break tall grass or wheat with a knife.",
        ], [item("farmersdelight:straw", 8)], xp=10),
        Q("canvas", "Canvas", 0, 0, ["4 straw."], [item("farmersdelight:canvas", 2)], xp=10),
        Q("basket", "Basket", 0, 0, [
            "Canvas and sticks. Picks up items in front of it, like a hopper.",
        ], [item("farmersdelight:wooden_basket")], xp=10),
        Q("cuts", "Raw Bacon", 0, 0, [
            "Cut a porkchop on the board. Meat cuts cook faster and stack into meals.",
        ], [item("farmersdelight:bacon", 4)], xp=10),
        Q("crops", "Wild Crops", 0, 0, [
            "Find wild crops in the world and break them for seeds and produce. Plant them.",
            "&aTip:&r Create's Millstone turns wild crops into seeds too.",
        ], [item("farmersdelight:cabbage")], xp=20),
        Q("tomato", "Tomato", 0, 0, [
            "Find wild tomatoes in warm biomes, cut them with a knife for seeds, and plant them.",
        ], [item("farmersdelight:tomato", 8)], xp=10),
        Q("cabbage_more", "Cabbage", 0, 0, [
            "Wild cabbages grow near beaches. Cut them with a knife for seeds.",
        ], [item("farmersdelight:cabbage", 8)], xp=10),
        Q("onion", "Onion", 0, 0, [
            "Wild onions grow in temperate biomes. Plant the onions themselves.",
        ], [item("farmersdelight:onion", 8)], xp=10),
        Q("rice", "Rice", 0, 0, [
            "Wild rice grows in shallow water. Plant it in water one block deep.",
        ], [item("farmersdelight:rice", 8)], xp=10),
        Q("stove", "Stove", 0, 0, [
            "Iron, bricks and a campfire. The heat source for pots and skillets.",
        ], [item("farmersdelight:stove")], xp=25),
        Q("skillet", "Skillet", 0, 0, [
            "Iron and a brick. Cook on the stove, or swing it as a weapon.",
        ], [item("farmersdelight:skillet")], xp=15),
        Q("fried_egg", "Fried Egg", 0, 0, ["Cook an egg in the skillet."], [item("farmersdelight:fried_egg", 4)], xp=10),
        Q("cooking_pot", "Cooking Pot", 0, 0, [
            "Bricks, iron, a water bucket and a wooden shovel. Put it on a stove and cook meals that",
            "give &aNourishment&r and &aComfort&r.",
        ], [item("farmersdelight:cooking_pot")], xp=40),
        Q("tomato_sauce", "Tomato Sauce", 0, 0, [
            "Two tomatoes and a bowl in the Cooking Pot (or a Create mixer).",
        ], [item("farmersdelight:tomato_sauce", 2)], xp=10),
        Q("cooked_rice", "Cooked Rice", 0, 0, [
            "Rice and a bowl in the Cooking Pot. The base for many meals.",
        ], [item("farmersdelight:cooked_rice", 4)], xp=10),
        Q("vegetable_soup", "Vegetable Soup", 0, 0, [
            "Carrot, potato, beetroot and a leafy green in the Cooking Pot.",
        ], [item("farmersdelight:vegetable_soup", 2)], xp=15),
        Q("beef_stew", "Beef Stew", 0, 0, [
            "Raw beef, carrot and potato in the Cooking Pot. Real food for a long fight.",
        ], [item("farmersdelight:beef_stew", 2)], xp=15),
        Q("compost", "Organic Compost", 0, 0, [
            "Dirt, straw, bone meal and &atree bark&r (strip logs on the cutting board). Place it and",
            "it slowly turns into &aRich Soil&r.",
        ], [item("farmersdelight:organic_compost", 4)], xp=30),
        Q("rich_soil", "Rich Soil", 0, 0, [
            "Crops grow faster on it, and mushrooms grow into colonies.",
        ], [item("farmersdelight:rich_soil", 8)], xp=15),
        Q("slicer", "Slicer", 0, 0, [
            "&6Create: Slice and Dice&r: a cogwheel, andesite casing and turntable. Put a knife in it",
            "and it runs &acutting board recipes&r on items below it, like a press on a depot or belt.",
            "Check the Ponder.",
        ], [item("sliceanddice:slicer")], xp=50),
        Q("sprinkler", "Sprinkler", 0, 0, [
            "Copper sheets, a fluid pipe and iron bars (makes 3). Pipe water into it to hydrate farmland.",
        ], [item("sliceanddice:sprinkler", 3)], xp=20),
        Q("fertilizer", "Liquid Fertilizer", 0, 0, [
            "Mix organic compost with water in a basin. Sprinklers spray it to speed up crops.",
        ], [item("sliceanddice:fertilizer_bucket")], xp=25),
        Q("feast", "Roast Chicken Feast", 0, 0, [
            "Feasts are placed blocks that serve several plates. One feeds a whole squad before a raid.",
        ], [item("farmersdelight:roast_chicken_block")], xp=60),
        Q("hamburger", "Hamburger", 0, 0, [
            "Bread, a beef patty, a leafy green, tomato and onion.",
        ], [item("farmersdelight:hamburger", 4)], xp=20),
        Q("cabbage_rolls", "Cabbage Rolls", 0, 0, [
            "Cabbage with meat, fish, vegetables or mushrooms in the Cooking Pot.",
        ], [item("farmersdelight:cabbage_rolls", 4)], xp=15),
        Q("dumplings", "Dumplings", 0, 0, [
            "Dough, cabbage, onion, meat and a brown mushroom in the Cooking Pot.",
        ], [item("farmersdelight:dumplings", 4)], xp=15),
    ]),
    # ----------------------------------------------------------------------------------------------
    dict(slug="storage", group="infrastructure", title="Storage",
         subtitle="Backpacks, upgradeable chests, vaults and a Tom's storage network",
         icon="toms_storage:storage_terminal", unlock=[("welcome", "next")], quests=[
        # owner 2026-11-21: Tom's Simple Storage is THE storage network (quests only, recipes untouched);
        # Sophisticated chests + tier upgrades are the chest-upgrade mod; no Create storage besides vaults.
        Q("backpack", "Backpack", 0, 0, [
            "&6Sophisticated Backpacks&r: leather, string and a chest. Wear it or place it.",
        ], [item("sophisticatedbackpacks:backpack")], xp=20),
        Q("bp_upgrade_base", "Backpack Upgrade Base", 0, 0, [
            "Iron, leather and string. The base for every backpack upgrade.",
        ], [item("sophisticatedbackpacks:upgrade_base")], xp=10),
        Q("pickup_upgrade", "Pickup Upgrade", 0, 0, [
            "Items you walk over go straight into the backpack.",
        ], [item("sophisticatedbackpacks:pickup_upgrade")], xp=15),
        Q("magnet_upgrade", "Magnet Upgrade", 0, 0, [
            "Pulls nearby items in. Great for clearing loot after a fight.",
        ], [item("sophisticatedbackpacks:magnet_upgrade")], xp=20),
        Q("iron_backpack", "Iron Backpack", 0, 0, [
            "Surround a backpack with iron for more slots. It keeps its contents.",
        ], [item("sophisticatedbackpacks:iron_backpack")], xp=20),
        Q("chest", "Sophisticated Chest", 0, 0, [
            "&6Sophisticated Storage&r: chests that take upgrades and can be tiered up. Planks and a",
            "lever (any wood works).",
        ], [item("sophisticatedstorage:chest")], xp=20),
        Q("barrel", "Sophisticated Barrel", 0, 0, [
            "Planks, slabs and a lever. A Sophisticated chest in barrel form: same tiers and upgrades.",
        ], [item("sophisticatedstorage:barrel")], xp=10),
        Q("packing_tape", "Packing Tape", 0, 0, [
            "Slime and paper. Tape a full chest to pick it up with everything inside.",
        ], [item("sophisticatedstorage:packing_tape")], xp=10),
        Q("ss_upgrade_base", "Storage Upgrade Base", 0, 0, [
            "Planks and iron. The base for storage upgrades.",
        ], [item("sophisticatedstorage:upgrade_base")], xp=10),
        Q("stack_upgrade", "Stack Upgrade Tier 1", 0, 0, [
            "An upgrade base and logs. Each slot holds more items; higher tiers hold far more.",
        ], [item("sophisticatedstorage:stack_upgrade_tier_1")], xp=15),
        Q("compacting_upgrade", "Compacting Upgrade", 0, 0, [
            "Turns nuggets into ingots and ingots into blocks as they come in.",
        ], [item("sophisticatedstorage:compacting_upgrade")], xp=15),
        Q("hopper_upgrade", "Hopper Upgrade", 0, 0, [
            "Pulls items in and pushes them out, with filters.",
        ], [item("sophisticatedstorage:hopper_upgrade")], xp=15),
        Q("copper_tier", "Chest Tier Upgrades", 0, 0, [
            "Right-click a placed chest or barrel with a tier upgrade to make it bigger &awithout",
            "emptying it&r. Copper first (copper ingots and a lever), then up the tiers.",
        ], [item("sophisticatedstorage:basic_to_copper_tier_upgrade")], xp=25),
        Q("iron_tier", "Iron Tier", 0, 0, [
            "Iron and a lever. Use it on a copper chest to upgrade it in place: contents stay.",
        ], [item("sophisticatedstorage:copper_to_iron_tier_upgrade")], xp=15),
        Q("gold_tier", "Gold Tier", 0, 0, [
            "Gold and a lever. Iron to gold.",
        ], [item("sophisticatedstorage:iron_to_gold_tier_upgrade")], xp=20),
        Q("diamond_tier", "Diamond Tier", 0, 0, [
            "Diamonds and a lever. Gold to diamond.",
        ], [item("sophisticatedstorage:gold_to_diamond_tier_upgrade")], xp=30),
        Q("netherite_tier", "Netherite Tier", 0, 0, [
            "A netherite ingot and a lever. Diamond to netherite: the biggest chest.",
        ], [item("sophisticatedstorage:diamond_to_netherite_tier_upgrade")], xp=40),
        Q("item_vault", "Item Vault", 0, 0, [
            "&6Create&r: a multiblock that holds a huge amount of items. Place several side by side to",
            "make it bigger. Hook it to your Tom's network like any chest.",
        ], [item("create:item_vault", 4)], xp=40),
        Q("connector", "Inventory Connector", 0, 0, [
            "&6Tom's Simple Storage&r is this pack's storage network. The &aInventory Connector&r",
            "joins every touching chest, barrel and vault into one network. Needs a diamond and an",
            "ender pearl.",
        ], [item("toms_storage:inventory_connector")], xp=40),
        Q("inventory_cable", "Inventory Cable", 0, 0, [
            "Planks, sticks, a chest and a trapdoor (makes 6). Reach storage that isn't next to the",
            "connector.",
        ], [item("toms_storage:inventory_cable", 6)], xp=10),
        Q("inventory_interface", "Inventory Interface", 0, 0, [
            "Lets hoppers, funnels and pipes insert into and extract from the whole network.",
        ], [item("toms_storage:inventory_interface")], xp=20),
        Q("terminal", "Storage Terminal", 0, 0, [
            "See and search everything on the network from one screen.",
        ], [item("toms_storage:storage_terminal")], xp=40),
        Q("wireless_terminal", "Wireless Terminal", 0, 0, [
            "A spyglass, comparator, ender pearl, glowstone, glass and planks. Opens your network",
            "from anywhere nearby.",
        ], [item("toms_storage:wireless_terminal")], xp=25),
        Q("crafting_terminal", "Crafting Terminal", 0, 0, [
            "A storage terminal with a crafting grid that pulls straight from the network.",
        ], [item("toms_storage:crafting_terminal")], xp=60),
        Q("adv_wireless_terminal", "Advanced Wireless Terminal", 0, 0, [
            "Netherite upgrade of the wireless terminal: much longer range.",
        ], [item("toms_storage:adv_wireless_terminal")], xp=30),
    ]),
    # ----------------------------------------------------------------------------------------------
    # Pollution and Air (owner 2026-11-21). Create: Smog is the ONLY way to handle pollution (PoTR's own
    # tools are removed by kubejs potr_tools_removed.js). Thick Air: no air below Y=0 / above Y=192 (pack config).
    dict(slug="pollution", group="infrastructure", title="Pollution and Air",
         subtitle="Create: Smog cleans up your factory; bring oxygen up high and deep down",
         icon="smog:air_scrubber", unlock=[("welcome", "next")], quests=[
        Q("backtank", "Copper Backtank", 0, 0, [
            "&6Thick Air&r: you slowly run out of air &cbelow Y=0&r, &cabove Y=192&r, and in the Nether.",
            "The End has no air at all. A &aBacktank&r with a &aDiving Helmet&r is your air supply.",
            "&cPilots:&r flying above Y=192 needs this too.",
        ], [item("create:copper_backtank")], xp=40),
        Q("diving_helmet", "Copper Diving Helmet", 0, 0, [
            "Wear it with the backtank to breathe from it.",
        ], [item("create:copper_diving_helmet")], xp=15),
        Q("air_bladder", "Air Bladder", 0, 0, [
            "Leather and string. A portable refill of air.",
        ], [item("thick_air:air_bladder")], xp=10),
        Q("reinforced_bladder", "Reinforced Air Bladder", 0, 0, [
            "Netherite upgrade: holds far more air.",
        ], [item("thick_air:reinforced_air_bladder")], xp=25),
        Q("safety_lantern", "Safety Lantern", 0, 0, [
            "Copper and a redstone torch. Its color shows the air quality around you.",
        ], [item("thick_air:safety_lantern")], xp=10),
        Q("air_respirator", "Air Respirator", 0, 0, [
            "&6Thick Air&r's respirator (paper, string, charcoal): helps in thin air. Not the same as",
            "Smog's respirator.",
        ], [item("thick_air:respirator")], xp=10),
        Q("soulfire_bottle", "Bottle of Soulfire", 0, 0, [
            "Emergency air. Soul fire, soul torches and soul campfires also make small pockets of",
            "breathable air.",
        ], [item("thick_air:soulfire_bottle", 2)], xp=10),
        Q("flue", "Smokestack", 0, 0, [
            "&6Create: Smog&r: anything that burns pollutes its chunk. Pollution here is handled &aonly",
            "with Create machines&r. Stack smokestacks on a source: &a12 tall&r sends most of the smoke",
            "into the high air, where it spreads thin.",
        ], [item("smog:flue", 12)], xp=30),
        Q("exhaust_duct", "Exhaust Duct", 0, 0, [
            "Iron sheet and andesite alloy. Pipe exhaust from a machine to a smokestack elsewhere.",
            "A broken duct leaks and smokes.",
        ], [item("smog:exhaust_duct", 8)], xp=15),
        Q("soot", "Soot", 0, 0, [
            "Collected from filters. Compact 4 into coal, or 6 into graphite.",
        ], [item("smog:soot", 8)], xp=10),
        Q("graphite", "Graphite", 0, 0, ["Compact 6 soot."], [item("smog:graphite", 2)], xp=10),
        Q("filter_cartridge", "Filter Cartridge", 0, 0, [
            "Iron bars, white wool and andesite alloy. Goes in an Air Scrubber. Clogged cartridges",
            "come back clean with &abulk washing&r (fan through water).",
        ], [item("smog:filter_cartridge", 2)], xp=25),
        Q("smog_respirator", "Smog Respirator", 0, 0, [
            "Leather, glass, string and a filter cartridge. Pulls pollution out of you.",
        ], [item("smog:respirator")], xp=15),
        Q("filter_medium", "Filter Medium", 0, 0, [
            "4 soot and string. A cheaper way to make cartridges.",
        ], [item("smog:filter_medium", 2)], xp=10),
        Q("air_scrubber", "Air Scrubber", 0, 0, [
            "Iron sheets, iron bars, andesite casing and a shaft. Spin it and give it a cartridge to",
            "clean the chunk around it. Pipe in water for a faster, sulfur-catching wet filter.",
        ], [item("smog:air_scrubber")], xp=40),
        Q("scrubber_panel", "Scrubber Panel", 0, 0, [
            "Scrubbers side by side join into one panel. A full &a5x5&r reaches up and clears the high",
            "air and the smog clouds.",
        ], [item("smog:air_scrubber", 25)], xp=40),
        Q("wastewater", "Industrial Wastewater", 0, 0, [
            "Wet scrubbers drain it. &cDo not dump it&r: it contaminates ground and kills plants.",
        ], [item("smog:industrial_wastewater_bucket")], xp=15),
        Q("clarified_water", "Clarified Water", 0, 0, [
            "Settle wastewater in a basin with a mixer.",
        ], [item("smog:clarified_water_bucket")], xp=15),
        Q("sludge_cake", "Sludge Cake", 0, 0, [
            "Compact industrial sludge. Crush it for dust and a chance of metals, or smelt it into brick.",
        ], [item("smog:sludge_cake", 4)], xp=15),
        Q("aerometer", "Aerometer", 0, 0, [
            "Glass, brass sheet and an electron tube. Hold it for a live pollution reading.",
            "Engineer's Goggles show the state of every Smog machine.",
        ], [item("smog:aerometer")], xp=30),
        Q("smog_sensor", "Smog Sensor", 0, 0, [
            "Outputs 0-15 redstone for the pollution around it. Turn on scrubbers automatically.",
        ], [item("smog:smog_sensor")], xp=20),
        Q("oil_burner", "Oil Burner", 0, 0, [
            "Heats basins and boilers with liquid fuel. Very dirty on waste oil, clean on refined oil.",
        ], [item("smog:oil_burner")], xp=20),
        Q("refined_oil", "Refined Oil", 0, 0, [
            "Engine smokestacks collect &aWaste Oil&r. Refine it with clay in a heated basin.",
        ], [item("smog:refined_oil_bucket")], xp=20),
        Q("precipitator", "Electrostatic Precipitator", 0, 0, [
            "Brass casing, brass sheets, an electron tube and iron bars. Put it in an exhaust line:",
            "it catches soot, more the faster it spins. Pipe water in to wash out sulfur.",
        ], [item("smog:electrostatic_precipitator")], xp=40),
        Q("brass_cartridge", "Brass Filter Cartridge", 0, 0, [
            "A brass sheet on a filter cartridge. Lasts 4x longer. Wash a clogged one with a",
            "fan through water to clean it and get the soot back.",
        ], [item("smog:brass_filter_cartridge")], xp=20),
        Q("acidic_runoff", "Acidic Runoff", 0, 0, [
            "Washed-out sulfur. Neutralize it in a basin (limestone works) back to clarified water.",
        ], [item("smog:acidic_runoff_bucket")], xp=15),
        Q("precision_cartridge", "Precision Filter Cartridge", 0, 0, [
            "Graphite, an electron tube and a brass cartridge. Lasts 16x longer. A clean factory.",
        ], [item("smog:precision_filter_cartridge")], xp=60),
    ]),
    # ----------------------------------------------------------------------------------------------
    dict(slug="automation", group="automation", title="Automation",
         subtitle="Put your machines to work: production goals for every tier",
         icon="create:mechanical_arm", unlock=[("kinetics", "casing")], quests=[
        Q("andesite_auto", "Andesite Automation", 0, 0, [
            "Production goals for Andesite-tier machines. Make these with &amachines&r, not by hand.",
        ], [CHECK], xp=20),
        Q("auto_cobble", "Automate: Cobblestone", 0, 0, [
            "A cobblestone generator with a &aMechanical Drill&r mining it nonstop. Make a &astack&r.",
        ], [item("minecraft:cobblestone", STACK)], xp=30),
        Q("auto_gravel", "Automate: Gravel", 0, 0, [
            "Feed cobblestone into a &aMillstone&r. Make a &astack&r of gravel.",
        ], [item("minecraft:gravel", STACK)], xp=30),
        Q("auto_alloy", "Automate: Andesite Alloy", 0, 0, [
            "Feed andesite and iron (or zinc) nuggets into a &aMixer&r over a Basin, no heat needed.",
            "Make a &astack&r.",
        ], [item("create:andesite_alloy", STACK)], xp=30),
        # owner: one iron quest with all three steps (nuggets -> ingots -> blocks)
        Q("auto_iron", "Automate: Iron", 0, 0, [
            "Blow &agravel&r through water with an &aEncased Fan&r (washing) for iron nuggets, then",
            "have a &aMechanical Press&r over a &aBasin&r compact them: &a9 nuggets&r into an ingot,",
            "&a9 ingots&r into a block.",
            "",
            "Make a &astack&r of nuggets, a &astack&r of ingots and &a7 Blocks of Iron&r.",
        ], [item("minecraft:iron_nugget", STACK), item("minecraft:iron_ingot", STACK),
            item("minecraft:iron_block", 7)], xp=80),
        Q("auto_sheets", "Automate: Iron Sheets", 0, 0, [
            "A Press over a belt of iron ingots. Make a &astack&r of Iron Sheets.",
        ], [item("create:iron_sheet", STACK)], xp=40),
        Q("auto_kelp", "Automate: Dried Kelp", 0, 0, [
            "Blow kelp through &afire&r with an Encased Fan (smoking). Make a &astack&r of Dried Kelp.",
        ], [item("minecraft:dried_kelp", STACK)], xp=30),
        Q("brass_auto", "Brass Automation", 0, 0, [
            "Production goals for the Brass Age.",
        ], [CHECK], xp=25),
        Q("auto_brass", "Automate: Brass", 0, 0, [
            "Feed copper and zinc into a heated Mixer automatically. Make a &astack&r of Brass Ingots.",
        ], [item("create:brass_ingot", STACK)], xp=40),
        Q("crushing", "Crushing Wheels", 0, 0, [
            "Andesite alloy, planks and stone (mechanical crafting). Two &aCrushing Wheels&r spinning",
            "toward each other crush ores into &acrushed ore&r: far more metal per ore than smelting.",
        ], [item("create:crushing_wheel", 2)], xp=20),
        Q("auto_zinc", "Automate: Ore Processing", 0, 0, [
            "Crush &azinc ore&r, wash the crushed ore with a fan, and smelt it. Make a &astack&r of Zinc",
            "Ingots.",
        ], [item("create:zinc_ingot", STACK)], xp=40),
        Q("auto_tubes", "Automate: Electron Tubes", 0, 0, [
            "Make &a5 Electron Tubes&r without crafting them by hand (Deployers on a belt work).",
        ], [item("create:electron_tube", 5)], xp=40),  # owner: 5, not a stack
        Q("auto_precision", "Automate: Precision Mechanisms", 0, 0, [
            "Loop the sequenced assembly line so it runs unattended. Make &a5 Precision Mechanisms&r.",
        ], [item("create:precision_mechanism", 5)], xp=60),  # owner: 5, not a stack
        Q("heat_auto", "Heat Automation", 0, 0, [
            "Keep the heat on without lifting a finger.",
        ], [CHECK], xp=25),
        Q("auto_cakes", "Automate: Blaze Cakes", 0, 0, [
            "Compact the base, fill it with lava and feed the cakes to your burners, all without",
            "touching it. Make a &astack&r of Blaze Cakes.",
        ], [item("create:blaze_cake", STACK)], xp=50),
        Q("auto_diamond", "Automate: Diamonds", 0, 0, [
            "&eThis pack's own recipe:&r compact &a9 Blocks of Coal&r in a Basin over a &6Superheated&r",
            "burner to make &b1 Diamond&r. Automate it and make a &astack&r (576 coal blocks).",
        ], [item("minecraft:diamond", STACK)], xp=100),
        Q("auto_netherite", "Automate: Netherite", 0, 0, [
            "&eThis pack's own recipe:&r &aCrushing Wheels&r crushing &aNether Bricks&r (the block) have a",
            "&a5% chance&r to drop &aNetherite Scrap&r. Netherrack is endless, so this is renewable.",
            "(Ancient Debris blown through lava with a fan works too.)",
            "",
            "Then let &aMechanical Crafters&r run the normal recipe: &a4 Netherite Scrap + 4 Gold Ingots&r",
            "= 1 Netherite Ingot. Make &a4 Netherite Ingots&r.",
        ], [item("minecraft:netherite_ingot", 4)], xp=100),  # 4, not a stack: ~80 brick blocks per ingot at 5%
        Q("auto_biofuel", "Automate: Biofuel", 0, 0, [
            "A biofuel plant that keeps its own mixer superheated. Fill a &astack&r of Biofuel buckets",
            "(16).",
        ], [item("createaddition:bioethanol_bucket", STACK16)], xp=75),
        Q("industrial_auto", "Industrial Automation", 0, 0, [
            "Heavy industry on autopilot.",
        ], [CHECK], xp=30),
        Q("auto_coke", "Automate: Coal Coke", 0, 0, [
            "Keep the coke oven fed. Make a &astack&r of Coal Coke.",
        ], [item("tfmg:coal_coke", STACK)], xp=50),
        Q("auto_steel", "Automate: Steel", 0, 0, [
            "Run the blast furnace continuously. Make a &astack&r of Steel Ingots.",
        ], [item("tfmg:steel_ingot", STACK)], xp=100),
        Q("auto_gasoline", "Automate: Gasoline", 0, 0, [
            "Pumpjack to distillation tower, no hands. Fill a &astack&r of Gasoline buckets (16).",
        ], [item("tfmg:gasoline_bucket", STACK16)], xp=100),
        Q("quantum_auto", "Quantum Automation", 0, 0, [
            "Mass-produce the quantum supply chain.",
        ], [CHECK], xp=30),
        Q("auto_telejuice", "Automate: Telejuice", 0, 0, [
            "A chorus fruit farm feeding a heated mixer. Fill a &astack&r of Telejuice buckets (16).",
        ], [item("createteleporters:quantum_fluid_bucket", STACK16)], xp=75),
        Q("enchanting_auto", "Enchanting Automation", 0, 0, [
            "Experience on tap.",
        ], [CHECK], xp=30),
        Q("auto_xp", "Automate: Liquid Experience", 0, 0, [
            "Fill a &astack&r of Bucket o' Enchanting (16) from an automated setup.",
        ], [item("create_enchantment_industry:experience_bucket", STACK16)], xp=75),
        # Food hub (owner 2026-11-21: "Yes, a Food hub")
        Q("food_auto", "Food Automation", 0, 0, [
            "Feed an army without lifting a knife. Make these with &amachines&r, not by hand.",
        ], [CHECK], xp=20),
        Q("auto_bread", "Automate: Bread", 0, 0, [
            "Mill wheat into flour, mix flour and water into dough, then bake it with an encased fan",
            "blowing through fire. Make a &astack&r.",
        ], [item("minecraft:bread", STACK)], xp=40),
        Q("auto_cabbage_leaf", "Automate: Cabbage Leaves", 0, 0, [
            "Feed cabbages under a &aSlicer&r holding a knife (it runs cutting board recipes). Make a",
            "&astack&r.",
        ], [item("farmersdelight:cabbage_leaf", STACK)], xp=40),
        Q("auto_soup", "Automate: Vegetable Soup", 0, 0, [
            "Keep a cooking pot on a stove fed with funnels and pull the soup out. Make a &astack&r",
            "(16).",
        ], [item("farmersdelight:vegetable_soup", STACK16)], xp=50),
    ]),
]


# --------------------------------------------------------------------------------------------------
# Layout: hub-and-spoke (owner's reference screenshot, 2026-11-21)
# --------------------------------------------------------------------------------------------------
# For each chapter: a main line of hubs (left -> right, each depends on the previous), satellites fanned
# around a hub on arcs above and below (each depends on its hub), and an optional gate quest whose
# dependencies are a hand-picked list drawn with hidden lines (so they don't cross the fan).
# x/y/deps written inside Q(...) are IGNORED for chapters listed here; this table is the truth.
#   main: [(slug, x, size[, y])]   y defaults to 0
#   connected: False  -> main hubs are separate bubbles (no line / dependency between them)
#   hubs: {hub_slug: [satellite slugs]}
#   chains: {satellite: [quests]}  (optional) extend a satellite straight outward along its spoke,
#           each depending on the one before (e.g. shaft -> water wheel -> large water wheel)
#   fans: {quest: [quests]}  (optional) spread around a spoke quest, pointing outward (sub-branch);
#         {quest: ([quests], offset_deg)} rotates the fan off the spoke (e.g. to sit beside a chain)
#   hubs values may be a list (spread over both arcs) or dict(top=[...], bottom=[...])
#   extra_deps: {quest: ["chapter/quest", ...]}  (optional) cross-chapter dependencies (not drawn)
#   gate: (slug, [required slugs]) or None
LAYOUTS = {
    "welcome": dict(
        main=[("welcome", 0, 2.0), ("next", 6, 1.5)],
        hubs={"welcome": ["team", "claims", "no_elytra", "waystones", "ultimine", "lootr"]},
        gate=None),
    "kinetics": dict(
        main=[("find_andesite", -5, 1.25), ("andesite_alloy", 0, 2.0), ("casing", 7, 2.0), ("next", 13, 2.0)],
        hubs={"andesite_alloy": dict(top=["shafts_cogs"]),
              "casing": dict(top=["millstone", "press", "basin_mixer"], bottom=["kelp", "gearbox"])},
        chains={"shafts_cogs": ["water_wheel", "large_water_wheel"],  # owner: shaft -> water wheel -> large
                # 2026-11-22 audit: gearboxes need andesite casing, so they moved to the casing hub
                "gearbox": ["vertical_gearbox"],
                "press": ["iron_sheets"],                              # owner: press & depot -> iron sheets
                "kelp": ["dried_kelp", "belts"]},                      # owner: kelp -> dried kelp -> belts
        fans={"iron_sheets": ["saw_drill", "harvester", "drill", "fan"],    # owner: iron sheets unlock these
              "press": (["gold_sheets"], -60),                              # owner: press -> gold sheet tree
              "gold_sheets": (["wrench_goggles", "goggles"], 0, 90),        # owner: gold sheets -> tools
              "dried_kelp": (["tunnel"], 90),                               # owner: dried kelp -> tunnels
              "shafts_cogs": (["cogwheels"], 70)},                          # owner 2026-11-22: cogs branch off shafts
        # owner 2026-11-22: no lines from shafts/cogwheels to the casing hub (the audit flags casing machines that
        # use shafts/cogs; accepted, they are basic parts taught right next to it)
        gate=("next", ["casing", "press", "basin_mixer", "belts", "iron_sheets"])),
    "brass_and_precision": dict(
        main=[("empty_burner", -9, 1.25), ("blaze", -5, 1.5), ("brass", 0, 2.0), ("brass_casing", 8, 2.0),
              ("next", 14, 2.0)],
        hubs={"brass": dict(top=["rose_quartz_raw"], bottom=["brass_sheets"]),
              "brass_casing": dict(top=["deployer"], bottom=["crafter"])},
        chains={"rose_quartz_raw": ["rose_quartz", "electron_tube"],   # recipe order
                "brass_sheets": ["brass_hand"],
                "deployer": ["precision"]},                           # deployers assemble precision mechs
        fans={"electron_tube": ["brass_funnel", "brass_tunnel"],
              "precision": ["mech_arm", "speed_controller"]},
        # owner 2026-11-22: no lines from Brass Hand / Electron Tube to the Brass Casing hub
        gate=("next", ["brass_casing", "electron_tube", "deployer", "precision", "crafter"])),
    "industrial": dict(
        main=[("cast_iron", -6, 1.25), ("coke_oven", -1, 2.0), ("blast_furnace", 6, 2.0), ("steel", 13, 2.0),
              ("heavy_casing", 20, 2.0), ("pumpjack", 27, 2.0), ("distillation", 34, 2.0), ("napalm", 40, 1.75)],
        hubs={"coke_oven": dict(top=["coal_coke"]),
              "blast_furnace": dict(top=["blast_stove"], bottom=["blast_hatch"]),
              "steel": dict(top=["steel_casing"], bottom=["steel_mechanism"]),
              "heavy_casing": dict(top=["surface_scanner"], bottom=["engine"]),
              "pumpjack": dict(top=["crude_oil"]),
              "distillation": dict(top=["gasoline", "diesel", "kerosene"], bottom=["aluminum"])},
        extra_deps={"napalm": ["heat/biofuel"],   # napalm needs biofuel (Heat Expansion)
                    "heavy_casing": ["steel_casing", "steel_mechanism"]},   # 2026-11-22 audit
        gate=None),
    "copper": dict(
        main=[("copper_sheet", -6, 1.25), ("copper_casing", -1, 2.0), ("fluid_pipe", 6, 2.0), ("fluid_tank", 13, 2.0),
              ("steam_engine", 20, 2.0), ("rolling_mill", 27, 2.0), ("electric_motor", 34, 2.0),
              ("tesla_coil", 41, 2.25)],
        hubs={"copper_casing": dict(top=["item_drain", "hose_pulley"], bottom=["portable_fluid_interface"]),
              "fluid_pipe": dict(top=["mechanical_pump", "fluid_valve"], bottom=["smart_fluid_pipe"]),
              "fluid_tank": dict(top=["fluid_vessel"], bottom=["fragile_fluid_tank"]),
              "steam_engine": dict(top=["steam_whistle"]),
              "rolling_mill": dict(top=["copper_rod", "capacitor"], bottom=["spool", "copper_wire"]),
              "electric_motor": dict(top=["alternator", "electric_pump"], bottom=["portable_energy_interface"]),
              "tesla_coil": dict(top=["electrum"])},
        chains={"item_drain": ["fluid_hatch"], "copper_rod": ["connector"], "copper_wire": ["copper_spool"],
                "fluid_valve": ["copper_valve_handle"],
                "electrum": ["modular_accumulator"]},   # the accumulator needs electrum wire
        # a boiler needs lit blaze burners; the engine needs gold sheets; brass parts stay visible but locked
        extra_deps={"steam_engine": ["brass_and_precision/blaze", "kinetics/gold_sheets"],
                    "smart_fluid_pipe": ["brass_and_precision/electron_tube"],
                    "electric_motor": ["brass_and_precision/brass_casing"],   # owner: no capacitor/spool lines to the motor
                    "copper_spool": ["spool"]},   # owner: copper spool requires copper wire and spool (both drawn)
        hidden_deps={
                     "electric_pump": ["mechanical_pump"]},
        gate=None),
    "heat": dict(
        main=[("tiers", -5, 1.5), ("blaze_cake", 1, 2.0), ("biofuel", 8, 2.0)],
        hubs={"tiers": dict(top=["cinder_flour"], bottom=["spout"]),
              "blaze_cake": dict(bottom=["biomass"]),
              "biofuel": dict(top=["straw"])},
        chains={"cinder_flour": ["cake_base"]},
        extra_deps={"blaze_cake": ["cake_base"]},   # 2026-11-22 audit
        gate=None),
    "quantum": dict(
        main=[("chorus", -6, 1.25), ("telejuice", -1, 2.0), ("quantum_pearl", 6, 2.0), ("waystone", 13, 2.0),
              ("advanced_part", 20, 1.75), ("quantum_mechanism", 26, 2.0), ("teleporter", 33, 2.0),
              ("item_transmitter", 40, 2.0)],
        hubs={"telejuice": dict(top=["quantum_casing"], bottom=["quantum_paper"]),
              "quantum_pearl": dict(top=["warp_dust"], bottom=["redstone_pearl"]),
              "waystone": dict(top=["blank_scroll"], bottom=["sharestone", "portstone", "warp_plate"]),
              "quantum_mechanism": dict(top=["tp_link"], bottom=["item_tp"]),
              "teleporter": dict(top=["adv_tplink", "custom_portal"]),
              "item_transmitter": dict(top=["fluid_transmitter", "energy_transmitter"], bottom=["chunk_loader"])},
        chains={"warp_dust": ["warp_stone"], "item_tp": ["block_teleporter"]},
        fans={"blank_scroll": ["warp_scroll", "return_scroll"]},
        # 2026-11-22 audit: recipe order
        extra_deps={"quantum_casing": ["rail/railway_casing"]},
        main_deps={"advanced_part": ["quantum_pearl"]},
        hidden_deps={"waystone": ["quantum_casing", "warp_stone", "quantum_paper"], "advanced_part": ["redstone_pearl"],
                     "quantum_mechanism": ["quantum_casing"]},
        gate=None),
    "enchanting": dict(
        main=[("grindstone", -6, 1.25), ("liquid_xp", -1, 2.0), ("xp_block", 6, 2.0), ("blaze_enchanter", 13, 2.0)],
        hubs={"liquid_xp": dict(top=["xp_cake_base"]),
              "xp_block": dict(top=["enchanting_template"], bottom=["xp_hatch", "xp_lantern"]),
              "blaze_enchanter": dict(top=["blaze_forger"], bottom=["printer"])},
        chains={"xp_cake_base": ["xp_cake"]},
        extra_deps={"printer": ["heat/spout"]},   # 2026-11-22 audit
        gate=None),
    "artillery": dict(
        main=[("log_cannon", -6, 1.25), ("cannon_mount", -1, 2.0), ("powder", 6, 2.0), ("shells", 13, 2.0),
              ("casting", 20, 2.0), ("built_up", 27, 2.0), ("autocannon", 34, 2.0), ("firepower", 41, 2.0),
              ("nethersteel", 47, 1.75)],
        hubs={"cannon_mount": dict(top=["wrought_iron", "cannon_carriage"], bottom=["cannon_loader"]),
              "powder": dict(top=["solid_shot"], bottom=["congealed_nitro"]),
              "shells": dict(top=["ap_shell", "shrapnel_shell", "smoke_shell"], bottom=["impact_fuze"]),
              "casting": dict(top=["casting_sand", "foundry_lid", "cast_mould"], bottom=["bronze"]),
              "built_up": dict(top=["cannon_builder", "cannon_drill"], bottom=["cannon_welder"]),
              "autocannon": dict(top=["autocannon_cartridge"], bottom=["ammo_container"]),
              "firepower": dict(top=["compact_autocannon_mount", "auto_cannon_controller"],
                                bottom=["magazine_loader", "ballistic_computer"])},
        chains={"congealed_nitro": ["hardened_nitro", "nitropowder"],
                "impact_fuze": ["timed_fuze", "proximity_fuze"],
                "autocannon_cartridge": ["ap_autocannon_round"]},
        # owner 2026-11-22: brass parts stay in view as a pull toward brass automation
        extra_deps={"firepower": ["brass_and_precision/brass_casing"],
                    "ballistic_computer": ["brass_and_precision/precision"],
                    "cannon_welder": ["brass_and_precision/blaze"]},
        hidden_deps={"magazine_loader": ["cannon_loader"]},
        gate=None),
    "infantry": dict(
        main=[("lead", -6, 1.25), ("flintlock", -1, 2.0), ("steel", 6, 2.0), ("revolver", 13, 2.0),
              ("shotgun", 20, 2.0), ("gatling", 27, 2.0), ("launcher", 34, 2.0), ("blazegun", 41, 2.0)],
        hubs={"flintlock": dict(top=["paper_cartridge", "musket_barrel"], bottom=["stock", "bayonet"]),
              "steel": dict(top=["charcoal_dust"], bottom=["steel_sheet"]),
              "revolver": dict(top=["press_form_revolver"], bottom=["scope", "long_barrel"]),
              "shotgun": dict(top=["press_form_shotgun"]),
              "gatling": dict(top=["round_gatling"]),
              "launcher": dict(top=["rocket"], bottom=["frag_grenade"]),
              "blazegun": dict(top=["nailgun"], bottom=["ballistazooka"])},
        chains={"press_form_revolver": ["shell_revolver", "round_revolver"],
                "press_form_shotgun": ["shell_shotgun", "round_shotgun"],
                "nailgun": ["nails"]},
        extra_deps={"gatling": ["brass_and_precision/precision"], "blazegun": ["brass_and_precision/blaze"],
                    "nailgun": ["pollution/backtank"]},   # 2026-11-22 audit
        gate=None),
    "radar": dict(
        main=[("binoculars", -6, 1.25), ("radar_bearing", -1, 2.0), ("monitor", 6, 2.0), ("auto_aim", 13, 2.0),
              ("plane_radar", 20, 2.0), ("missile_mount", 27, 2.0), ("guidance", 34, 2.0)],
        hubs={"radar_bearing": dict(top=["radar_dish"], bottom=["radar_plate", "radar_receiver"]),
              "monitor": dict(top=["data_link"], bottom=["detection_filter", "targeting_filter", "ident_filter"]),
              "auto_aim": dict(top=["fire_controller"], bottom=["guided_fuze"]),
              "plane_radar": dict(top=["transponder"], bottom=["network_controller", "safe_zone"]),
              "missile_mount": dict(top=["actuator_fins"], bottom=["payload_casing"]),
              "guidance": dict(top=["targeting_interface"], bottom=["air_prox_fuze"])},
        chains={"fire_controller": ["fire_arc"], "actuator_fins": ["rocket_motor"]},
        extra_deps={"monitor": ["radar_dish", "radar_receiver"]},   # 2026-11-22 audit
        hidden_deps={"auto_aim": ["detection_filter", "targeting_filter", "ident_filter"]},
        gate=None),
    "aeronautics": dict(
        main=[("physics_assembler", -6, 1.25), ("levitite", -1, 2.0), ("hot_air", 6, 2.0), ("propeller", 13, 2.0),
              ("controls", 20, 2.0), ("cockpit", 27, 2.0), ("air_weapons", 34, 2.0), ("aerial_ordnance", 41, 2.0),
              ("synaxis", 48, 2.0)],
        hubs={"levitite": dict(top=["end_stone_powder"], bottom=["pearlescent_levitite"]),
              "hot_air": dict(top=["steam_vent"], bottom=["aviators_goggles"]),
              "propeller": dict(top=["andesite_propeller"], bottom=["smart_propeller", "gyro_propeller"]),
              "controls": dict(top=["throttle", "altitude_sensor"], bottom=["navigation_table", "gimbal_sensor"]),
              "cockpit": dict(top=["control_desk", "lever_module", "joystick_module"],
                              bottom=["pedal_module", "button_panel_module", "wheel_module"]),
              "air_weapons": dict(top=["minigun", "air_camera", "rocket_engine"], bottom=["sc_250", "aim9x", "tomahawk"]),
              "aerial_ordnance": dict(top=["aphe_bomb", "bouncing_bomb"], bottom=["rocket_bracket"]),
              "synaxis": dict(top=["jet", "mechanical_servo"], bottom=["circuit", "hydraulic_actuator"])},
        chains={"end_stone_powder": ["levitite_blend"], "air_camera": ["air_monitor"],
                "andesite_propeller": ["wooden_propeller"], "gimbal_sensor": ["gyroscope"], "rocket_bracket": ["aerial_torpedo"],
                "button_panel_module": ["button_keypad_module"], "mechanical_servo": ["stepper_servo"]},
        fans={"lever_module": ["yoke_module", "throttle_quadrant_module"]},
        extra_deps={"aerial_ordnance": ["artillery/shells"], "aphe_bomb": ["artillery/ap_shell"],
                    "bouncing_bomb": ["demolitions/guncotton"], "aerial_torpedo": ["naval/torpedo"]},
        gate=None),
    "naval": dict(
        main=[("rudder", -6, 1.25), ("boat_engine", -1, 2.0), ("ballast", 6, 2.0), ("oxygen", 13, 2.0),
              ("command", 20, 2.0), ("torpedo", 27, 2.0)],
        hubs={"boat_engine": dict(top=["anchor", "buoy"], bottom=["wind_vane", "oar"]),
              "ballast": dict(top=["ballast_vent", "floater"], bottom=["sub_propeller", "water_thruster"]),
              "oxygen": dict(top=["diffuser", "decompression"], bottom=["diving_gear", "pressure_goggles"]),
              "command": dict(top=["sub_sonar", "barometer"], bottom=["alarm", "pump_controller"]),
              "torpedo": dict(top=["torpedo_head", "torpedo_tube"], bottom=["depth_charge", "mine", "torpedo_detector"])},
        extra_deps={"depth_charge": ["demolitions/guncotton", "artillery/timed_fuze"]},   # 2026-11-22 audit
        gate=None),
    "rail": dict(
        main=[("track", -6, 1.25), ("station", -1, 2.0), ("train_controls", 6, 2.0), ("snr", 13, 2.0),
              ("armored_train", 20, 2.0)],
        hubs={"track": dict(top=["railway_casing"]),
              "station": dict(top=["signal", "observer"], bottom=["schedule"]),
              "train_controls": dict(bottom=["train_door", "psi"]),
              "snr": dict(top=["semaphore", "whistle"], bottom=["fuel_tank", "fuel_interface"]),
              "armored_train": dict(top=["iron_key", "gold_key"], bottom=["locometal"])},
        extra_deps={"station": ["railway_casing"]},   # 2026-11-22 audit
        gate=None),
    "armored": dict(
        main=[("wheel_mount", -6, 1.25), ("tires", -1, 2.0), ("tracks", 6, 2.0), ("armor", 13, 2.0), ("arcon", 20, 2.0)],
        hubs={"tires": dict(top=["small_tire", "large_tire"], bottom=["monstrous_tire", "rockcutting_wheel", "industrial_belt"]),
              "tracks": dict(top=["grouser", "suspension"], bottom=["flanged_cog"]),
              "armor": dict(top=["sandbags", "hull_aluminum"], bottom=["hull_rolled"]),
              "arcon": dict(top=["arcon_muzzle", "arcon_breech"], bottom=["bops"])},
        chains={"hull_rolled": ["hull_nickel", "hull_ceramic", "hull_boron"], "hull_aluminum": ["hull_titanium"]},
        # 2026-11-22 audit; Arcon armor and guns use TFMG heavy plates and steel
        extra_deps={"tracks": ["industrial_belt"], "rockcutting_wheel": ["automation/crushing"],
                    "hull_rolled": ["industrial/steel"], "arcon": ["industrial/steel_mechanism"],
                    "bops": ["demolitions/guncotton"]},
        gate=None),
    "drones": dict(
        main=[("drone_core", -1, 2.0), ("drone_camera", 6, 2.0), ("remote", 13, 2.0), ("fpv", 20, 2.0)],
        hubs={"drone_core": dict(top=["drone_blade", "drone_propeller"], bottom=["tilting_bearing", "flap_bearing"]),
              "drone_camera": dict(top=["drone_hub"]),
              "remote": dict(top=["drone_controls"], bottom=["commander_seat"]),
              "fpv": dict(top=["drone_joystick"])},
        extra_deps={"drone_core": ["aeronautics/andesite_propeller", "aeronautics/propeller",
                                   "aeronautics/gimbal_sensor"],   # 2026-11-22 audit
                    "fpv": ["demolitions/guncotton"]},
        gate=None),
    "demolitions": dict(
        main=[("guncotton", -6, 1.25), ("small_bomb", -1, 2.0), ("medium_bomb", 6, 2.0), ("large_bomb", 13, 2.0),
              ("c4", 20, 2.0), ("cruise_missile", 27, 2.0), ("moab", 34, 2.0)],
        hubs={"guncotton": dict(top=["tripwire_coil"], bottom=["wire_cutters"]),
              "small_bomb": dict(top=["bombsight"], bottom=["small_mine", "bounding_mine", "claymore"]),
              "medium_bomb": dict(top=["rocket_pod"], bottom=["sea_mine", "sea_torpedo"]),
              "large_bomb": dict(top=["large_mine"], bottom=["siren"]),
              "c4": dict(top=["detonator"], bottom=["bomb_vest"]),          # bomb vest is crafted from C4
              "cruise_missile": dict(top=["target_designator"], bottom=["aim9"])},
        chains={"rocket_pod": ["s8_rocket"]},
        # mechanical crafting needs the Brass Age crafter; fuzes come from Artillery
        extra_deps={"medium_bomb": ["artillery/impact_fuze", "brass_and_precision/crafter"],
                    "aim9": ["artillery/proximity_fuze"]},
        gate=None),
    "nuclear": dict(
        main=[("raw_uranium", -7, 1.5), ("uranium_powder", 0, 2.0), ("yellowcake", 7, 2.0),
              ("enriched_yellowcake", 14, 2.0), ("uranium_rod", 21, 2.0), ("reactor_controller", 28, 2.25),
              ("nuke_shell", 35, 2.25), ("nuke_shell_mk2", 42, 2.25), ("h_bomb", 49, 2.75)],
        hubs={"raw_uranium": dict(top=["raw_thorium"]),
              "uranium_powder": dict(top=["enriched_soul_soil"]),
              "uranium_rod": dict(top=["reactor_casing"], bottom=["graphene"]),
              "reactor_controller": dict(top=["reactor_blueprint"], bottom=["nitrogen"]),
              "nuke_shell": dict(bottom=["h_bomb_mini"])},
        chains={"raw_thorium": ["thorium_ingot", "thorium_rod"], "enriched_soul_soil": ["enriching_campfire"],
                "graphene": ["graphite_rod", "hazmat"]},   # 2026-11-22 audit: the suit needs graphite rods
        fans={"reactor_casing": ["reactor_frame", "reactor_core"]},
        hidden_deps={"nuke_shell_mk2": ["thorium_rod"]},
        # rods and the controller are mechanical crafting; the nuke is built around a Big Cannons HE shell
        extra_deps={"uranium_rod": ["brass_and_precision/crafter"], "enriched_yellowcake": ["enriching_campfire"],
                    "nuke_shell": ["artillery/shells"],
                    "reactor_controller": ["reactor_casing", "storage/item_vault"]},
        gate=None),
    "pollution": dict(
        main=[("backtank", -7, 1.5), ("flue", 0, 2.0), ("filter_cartridge", 7, 2.0), ("air_scrubber", 14, 2.0),
              ("aerometer", 21, 2.0), ("precipitator", 28, 2.0), ("precision_cartridge", 35, 2.0)],
        hubs={"backtank": dict(top=["diving_helmet", "safety_lantern"], bottom=["air_bladder", "air_respirator", "soulfire_bottle"]),
              "flue": dict(top=["exhaust_duct"], bottom=["soot"]),
              "filter_cartridge": dict(top=["smog_respirator"], bottom=["filter_medium"]),
              "air_scrubber": dict(top=["scrubber_panel"], bottom=["wastewater"]),
              "aerometer": dict(top=["smog_sensor"], bottom=["oil_burner"]),
              "precipitator": dict(top=["brass_cartridge"], bottom=["acidic_runoff"])},
        chains={"air_bladder": ["reinforced_bladder"], "soot": ["graphite"],
                "wastewater": ["clarified_water", "sludge_cake"], "oil_burner": ["refined_oil"]},
        extra_deps={"backtank": ["kinetics/shafts_cogs"], "filter_medium": ["soot"],   # 2026-11-22 audit
                    "flue": ["kinetics/andesite_alloy"], "air_scrubber": ["kinetics/casing"],
                    "aerometer": ["brass_and_precision/brass"], "precipitator": ["brass_and_precision/brass_casing"],
                    "precision_cartridge": ["brass_and_precision/precision"]},
        gate=None),
    "enemy": dict(
        main=[("first_blood", -6, 1.5), ("skeleton", 1, 2.0), ("creeper", 8, 2.0), ("armed", 15, 2.0),
              ("raiders", 22, 2.0), ("ambush", 29, 2.0), ("nether", 36, 2.0), ("wither", 43, 2.0),
              ("invasion", 36, 2.0, 11), ("invoker", 45, 2.25, 11)],
        hubs={"first_blood": dict(top=["spider", "husk"], bottom=["zombie_villager"]),
              "skeleton": dict(top=["stray"], bottom=["bogged"]),
              "creeper": dict(top=["enderman"], bottom=["witch"]),
              "raiders": dict(top=["vindicator", "evoker"], bottom=["ravager"]),
              "nether": dict(top=["wither_skeleton", "ghast"], bottom=["piglin_brute"]),
              "wither": dict(top=["ender_dragon"], bottom=["elder_guardian", "warden"]),
              "invasion": dict(top=["basher", "marauder"], bottom=["firecaller", "necromancer"])},
        chains={"basher": ["inquisitor"], "marauder": ["alchemist"], "firecaller": ["sorcerer", "archivist"],
                "necromancer": ["surrendered"]},
        # Illager Invasion sits on a second row under Raiders, so Ambush (Defend Your Home's unlock) doesn't move
        main_deps={"invasion": ["raiders"]},
        gate=None),
    "defense": dict(
        main=[("wave_scouts", -6, 1.5), ("wave_raiders", 0, 1.5), ("wave_warband", 6, 1.75),
              ("wave_siege", 12, 1.75), ("wave_drill_car", 18, 2.0), ("wave_patrol_ship", 24, 2.0),
              ("wave_antiair", 30, 2.0), ("wave_storm_breaker", 37, 2.5)],
        hubs={},
        # vehicle/airship waves need the matching weapons first
        extra_deps={"wave_drill_car": ["artillery/cannon_mount"], "wave_patrol_ship": ["artillery/autocannon"],
                    "wave_storm_breaker": ["radar/monitor"]},
        gate=None),
    "food": dict(
        main=[("knife", -6, 1.25), ("cutting_board", -1, 2.0), ("crops", 6, 2.0), ("stove", 13, 2.0),
              ("cooking_pot", 20, 2.0), ("compost", 27, 2.0), ("slicer", 34, 2.0), ("feast", 41, 2.0)],
        hubs={"cutting_board": dict(top=["straw"], bottom=["cuts"]),
              "crops": dict(top=["tomato", "cabbage_more"], bottom=["onion", "rice"]),
              "stove": dict(top=["skillet"]),
              "cooking_pot": dict(top=["tomato_sauce", "cooked_rice"], bottom=["vegetable_soup", "beef_stew"]),
              "compost": dict(top=["rich_soil"]),
              "slicer": dict(top=["sprinkler"], bottom=["fertilizer"]),
              "feast": dict(top=["hamburger", "cabbage_rolls"], bottom=["dumplings"])},
        chains={"straw": ["canvas", "basket"],    # recipe order: straw -> canvas -> basket
                "skillet": ["fried_egg"]},
        extra_deps={"slicer": ["kinetics/casing"]},   # andesite casing + turntable
        hidden_deps={"compost": ["straw"]},   # 2026-11-22 audit: organic compost uses straw
        gate=None),
    "storage": dict(
        main=[("backpack", -6, 1.25), ("chest", -1, 2.0), ("copper_tier", 6, 2.0), ("item_vault", 13, 2.0),
              ("connector", 20, 2.0), ("terminal", 27, 2.0), ("crafting_terminal", 34, 2.0)],
        hubs={"backpack": dict(top=["bp_upgrade_base"], bottom=["iron_backpack"]),
              "chest": dict(top=["ss_upgrade_base"], bottom=["barrel", "packing_tape"]),
              "copper_tier": dict(top=["iron_tier"]),
              "connector": dict(top=["inventory_cable"], bottom=["inventory_interface"]),
              "terminal": dict(top=["wireless_terminal"]),
              "crafting_terminal": dict(top=["adv_wireless_terminal"])},
        chains={"bp_upgrade_base": ["pickup_upgrade", "magnet_upgrade"],   # magnet is crafted from pickup
                "iron_tier": ["gold_tier", "diamond_tier", "netherite_tier"]},   # tier upgrade order
        fans={"ss_upgrade_base": ["stack_upgrade", "compacting_upgrade", "hopper_upgrade"]},
        extra_deps={"item_vault": ["kinetics/iron_sheets"], "adv_wireless_terminal": ["wireless_terminal"]},
        gate=None),
    "automation": dict(
        # owner: separate bubbles, not a connected line. Top row = Ages tiers, bottom row = Expansions.
        connected=False,
        main=[("andesite_auto", 0, 2.0, 0), ("brass_auto", 10, 2.0, 0), ("industrial_auto", 20, 2.0, 0),
              ("heat_auto", 0, 2.0, 11), ("quantum_auto", 10, 2.0, 11), ("enchanting_auto", 20, 2.0, 11),
              ("food_auto", 30, 2.0, 0)],
        hubs={"andesite_auto": dict(top=["auto_cobble", "auto_gravel", "auto_alloy"],
                                    bottom=["auto_iron", "auto_sheets", "auto_kelp"]),
              "brass_auto": dict(top=["auto_brass", "auto_tubes", "auto_precision"], bottom=["crushing"]),
              "heat_auto": dict(top=["auto_cakes", "auto_diamond", "auto_netherite"], bottom=["auto_biofuel"]),
              "industrial_auto": dict(top=["auto_coke", "auto_steel"], bottom=["auto_gasoline"]),
              "quantum_auto": dict(top=["auto_telejuice"]),   # owner 2026-11-21: no quantum pearl automate
              "enchanting_auto": dict(top=["auto_xp"]),
              "food_auto": dict(top=["auto_bread", "auto_cabbage_leaf"], bottom=["auto_soup"])},
        chains={"crushing": ["auto_zinc"]},
        # each tier hub also needs progress in its own chapter (not drawn: other chapter)
        extra_deps={"andesite_auto": ["kinetics/casing"],
                    "brass_auto": ["brass_and_precision/brass_casing"],
                    "heat_auto": ["heat/blaze_cake"],
                    "industrial_auto": ["industrial/steel"],
                    "quantum_auto": ["quantum/telejuice"],
                    "enchanting_auto": ["enchanting/liquid_xp"],
                    "food_auto": ["food/slicer"]},
        gate=None),
}
# Copper Expansion parts used by other chapters (2026-11-22 audit, after the Copper chapter was added):
# each quest also needs the Copper quest that teaches its fluid/copper part. Other chapter, so not drawn.
COPPER_DEPS = {
    "aeronautics": {"cockpit": ["copper/copper_casing"], "jet": ["copper/fluid_pipe"],
                    "rocket_engine": ["copper/fluid_tank"]},
    "artillery": {"cannon_drill": ["copper/fluid_pipe"]},
    "enchanting": {"xp_hatch": ["copper/fluid_hatch"], "xp_lantern": ["copper/copper_casing"]},
    "heat": {"spout": ["copper/copper_casing"]},
    "infantry": {"blazegun": ["copper/fluid_tank"], "launcher": ["copper/fluid_pipe"],
                 "nailgun": ["copper/fluid_valve"], "rocket": ["copper/fluid_pipe"]},
    "naval": {"ballast": ["copper/fluid_tank"], "decompression": ["copper/mechanical_pump"],
              "diffuser": ["copper/item_drain"], "pump_controller": ["copper/mechanical_pump"],
              "sub_sonar": ["copper/copper_sheet"], "torpedo_detector": ["copper/copper_sheet"],
              "water_thruster": ["copper/mechanical_pump"]},
    "pollution": {"oil_burner": ["copper/copper_casing", "copper/fluid_pipe"]},
    "quantum": {"custom_portal": ["copper/fluid_tank"], "fluid_transmitter": ["copper/mechanical_pump"]},
    "radar": {"fire_arc": ["copper/copper_sheet"]},
    "rail": {"fuel_tank": ["copper/fluid_tank"]},
}
ARCS = [(35, 145), (215, 325)]  # degrees; keeps satellites clear of the horizontal main line
SAT_SPACING = 1.8               # arc distance between neighbouring satellites
FAN_RADIUS = 2.6                # sub-fan: distance from its center quest
FAN_SPREAD = 160                # sub-fan: total angle (degrees), centered on the spoke direction
CHAIN_STEP = 1.8                # distance between links of a chain along a spoke
MIN_GAP = 0.6                   # minimum empty space between quest edges (room for labels)
_unused = 0                # sub-fan: total angle (degrees), centered on the spoke direction


def apply_layout(ch):
    lay = LAYOUTS.get(ch["slug"])
    if not lay:
        return
    by = {q["slug"]: q for q in ch["quests"]}
    placed = set()
    prev = None
    connected = lay.get("connected", True)
    for entry in lay["main"]:
        slug, x, size = entry[:3]
        y = entry[3] if len(entry) > 3 else 0
        q = by[slug]
        q.update(x=x, y=y, size=size, deps=[prev] if (prev and connected) else [])
        if q["shape"] != "hexagon":
            q["shape"] = None
        placed.add(slug)
        prev = slug
    def put(slug, x, y, deps, ang):
        by[slug].update(x=round(x, 2), y=round(y, 2), deps=deps)
        by[slug]["_ang"] = ang  # outward direction, used by fans
        placed.add(slug)

    def angles_for(sats):
        """list -> spread evenly over both ARCS; dict(top=[...], bottom=[...]) -> each over its own arc."""
        if isinstance(sats, dict):
            out = []
            for key, (a, b) in (("top", ARCS[0]), ("bottom", ARCS[1])):
                lst = sats.get(key, [])
                out += [(s, math.radians(a + (b - a) * (i + 0.5) / len(lst))) for i, s in enumerate(lst)]
            return out
        total = sum(math.radians(b - a) for a, b in ARCS)
        out = []
        for i, slug in enumerate(sats):
            t = (i + 0.5) / len(sats) * total
            for a, b in ARCS:
                span = math.radians(b - a)
                if t <= span:
                    out.append((slug, math.radians(a) + t))
                    break
                t -= span
        return out

    for hub, sats in lay["hubs"].items():
        hx, hy = by[hub]["x"], by[hub]["y"]
        placed_angles = angles_for(sats)
        r = max(2.6, len(placed_angles) * SAT_SPACING / sum(math.radians(b - a) for a, b in ARCS))
        for slug, ang in placed_angles:
            put(slug, hx + r * math.cos(ang), hy - r * math.sin(ang), [hub], ang)
            prev_c = slug
            for k, cslug in enumerate(lay.get("chains", {}).get(slug, []), start=1):
                rc = r + k * CHAIN_STEP
                put(cslug, hx + rc * math.cos(ang), hy - rc * math.sin(ang), [prev_c], ang)
                prev_c = cslug
    # fans: side quests spread around a quest that is itself on a spoke, pointing outward
    for center, sats in lay.get("fans", {}).items():
        offset, spread_deg = 0, FAN_SPREAD
        if isinstance(sats, tuple):  # (quests, offset_deg[, spread_deg]): rotate / narrow the fan
            sats, offset, *rest = sats
            spread_deg = rest[0] if rest else FAN_SPREAD
        cx, cy, base = by[center]["x"], by[center]["y"], by[center]["_ang"] + math.radians(offset)
        spread = math.radians(spread_deg)
        fr = max(FAN_RADIUS, len(sats) * SAT_SPACING / spread)  # grow with count, like hubs
        for i, slug in enumerate(sats):
            ang = base - spread / 2 + spread * (i + 0.5) / len(sats)
            put(slug, cx + fr * math.cos(ang), cy - fr * math.sin(ang), [center], ang)
    for slug, extra in lay.get("extra_deps", {}).items():
        by[slug]["deps"] = by[slug]["deps"] + list(extra)
    for slug, extra in COPPER_DEPS.get(ch["slug"], {}).items():
        by[slug]["deps"] = by[slug]["deps"] + list(extra)
    # main_deps: replace a main-line quest's dependency on the previous hub (owner 2026-11-22: Advanced Component
    # doesn't need the Waystone; its recipe has no waystone parts).
    for slug, deps in lay.get("main_deps", {}).items():
        by[slug]["deps"] = list(deps)
    # hidden_deps: same-chapter prerequisites whose line would cross the chapter. The quest's lines are hidden
    # (FTB only has a per-quest switch), so use sparingly. 2026-11-22 quest audit.
    for slug, extra in lay.get("hidden_deps", {}).items():
        by[slug]["deps"] = by[slug]["deps"] + list(extra)
        by[slug]["hide_lines"] = True
    if lay["gate"]:
        slug, req = lay["gate"]
        by[slug].update(deps=list(req), hide_lines=True)
    missing = set(by) - placed
    assert not missing, f"{ch['slug']}: quests with no layout position: {missing}"


def check_layout(ch):
    """No overlapping quests; no visible dependency line passing through another quest."""
    qs = ch["quests"]
    rad = {q["slug"]: (q["size"] or 1.0) / 2 for q in qs}
    pos = {q["slug"]: (q["x"], q["y"]) for q in qs}
    errors = []
    for i, a in enumerate(qs):
        for b in qs[i + 1:]:
            d = math.dist(pos[a["slug"]], pos[b["slug"]])
            if d < rad[a["slug"]] + rad[b["slug"]] + MIN_GAP:
                errors.append(f"overlap {a['slug']} / {b['slug']}")
    for q in qs:
        if q.get("hide_lines"):
            continue
        for dep in q["deps"]:
            if "/" in dep:
                continue  # other chapter: FTB doesn't draw it
            (x1, y1), (x2, y2) = pos[dep], pos[q["slug"]]
            for o, (ox, oy) in pos.items():
                if o in (dep, q["slug"]):
                    continue
                L2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
                t = max(0, min(1, ((ox - x1) * (x2 - x1) + (oy - y1) * (y2 - y1)) / L2))
                if math.dist((ox, oy), (x1 + t * (x2 - x1), y1 + t * (y2 - y1))) < rad[o] + 0.05:
                    errors.append(f"line {dep}->{q['slug']} passes through {o}")
    assert not errors, f"{ch['slug']} layout: " + "; ".join(errors)


# --------------------------------------------------------------------------------------------------
# SNBT writer
# --------------------------------------------------------------------------------------------------
def s(v):
    return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'


def write_snbt(value, indent=0):
    tab = "\t" * indent
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Raw):
        return value.text
    if isinstance(value, float):
        return f"{value}d"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return s(value)
    if isinstance(value, list):
        if not value:
            return "[ ]"
        inner = "\n".join(tab + "\t" + write_snbt(v, indent + 1) for v in value)
        return "[\n" + inner + "\n" + tab + "]"
    if isinstance(value, dict):
        if not value:
            return "{ }"
        lines = []
        for k, v in sorted(value.items()):  # FTB Quests sorts keys on write; match it to avoid rewrites
            key = k if k.replace("_", "").isalnum() else s(k)
            lines.append(f"{tab}\t{key}: {write_snbt(v, indent + 1)}")
        return "{\n" + "\n".join(lines) + "\n" + tab + "}"
    raise TypeError(value)


class Raw:
    def __init__(self, text):
        self.text = text


def stack(i, count=1):
    return {"id": i, "count": count}


def levels_for(ch, q):
    """Whole-level bonus by role (see XP constants). A quest's own `levels` wins."""
    if q.get("levels") is not None:
        return q["levels"]
    lay = LAYOUTS.get(ch["slug"], {})
    main = [e[0] for e in lay.get("main", [])]
    gate = lay.get("gate")
    if gate and q["slug"] == gate[0]:
        return LEVELS_GATE
    if main and q["slug"] == main[-1] and lay.get("connected", True):
        return LEVELS_FINALE
    if q["slug"].startswith("auto_"):
        return LEVELS_AUTOMATE
    if q["slug"] in main:
        return LEVELS_HUB
    return 0


def build():
    lang = {}
    chapter_files = {}
    group_ids = {}
    for slug, title in GROUPS:
        group_ids[slug] = qid("group", slug)
        lang[f"chapter_group.{group_ids[slug]}.title"] = title
    for order, ch in enumerate(CHAPTERS):
        cid = qid(ch["slug"])
        lang[f"chapter.{cid}.title"] = ch["title"]
        if ch.get("subtitle"):
            lang[f"chapter.{cid}.chapter_subtitle"] = [ch["subtitle"]]
        apply_layout(ch)
        check_layout(ch)
        slugs = {q["slug"] for q in ch["quests"]}
        quests = []
        for q in ch["quests"]:
            for d in q["deps"]:
                if "/" in d:
                    c2, q2 = d.split("/")
                    assert any(c["slug"] == c2 and any(x["slug"] == q2 for x in c["quests"]) for c in CHAPTERS), \
                        f"{ch['slug']}/{q['slug']}: unknown cross-chapter dependency {d}"
                else:
                    assert d in slugs, f"{ch['slug']}/{q['slug']}: unknown dependency {d}"
            id_ = qid(ch["slug"], q["slug"])
            lang[f"quest.{id_}.title"] = q["title"]
            if q["subtitle"]:
                lang[f"quest.{id_}.quest_subtitle"] = q["subtitle"]
            lang[f"quest.{id_}.quest_desc"] = q["desc"]
            tasks = []
            for n, (kind, iid, count) in enumerate(q["tasks"]):
                t = {"id": qid(ch["slug"], q["slug"], "task", str(n)), "type": kind}
                if kind == "item":
                    t["item"] = stack(iid)
                    if count != 1:  # the game omits the default count of 1
                        t["count"] = Raw(f"{count}L")
                elif kind == "kill":
                    # KillTask.writeData (2101.1.39): "entity" string, "value" long, always written
                    t["entity"] = iid
                    t["value"] = Raw(f"{count}L")
                tasks.append(t)
            rewards = []
            if q["xp"]:
                rewards.append({"id": qid(ch["slug"], q["slug"], "xp"), "type": "xp", "xp": q["xp"] * XP_SCALE})
            levels = levels_for(ch, q)
            if levels:
                rewards.append({"id": qid(ch["slug"], q["slug"], "levels"), "type": "xp_levels",
                                "xp_levels": levels})
            for n, (iid, count) in enumerate(q["items"]):
                # ItemReward keeps the amount in its own "count"; the stack itself is count 1 (game format)
                rewards.append({"id": qid(ch["slug"], q["slug"], "reward", str(n)), "type": "item",
                                "item": stack(iid), "count": count})
            for n, (table, times) in enumerate(q["rolls"]):
                assert table in REWARD_TABLES, f"{ch['slug']}/{q['slug']}: unknown reward table {table}"
                for k in range(times):
                    # RandomReward.writeData: "table_id" is the table's ID as a LONG (not the hex string)
                    rewards.append({"id": qid(ch["slug"], q["slug"], "roll", str(n), str(k)), "type": "random",
                                    "table_id": Raw(f"{int(qid('table', table), 16)}L")})
            if q["bonus"]:
                for n, (kind, iid, count) in enumerate(q["tasks"]):
                    if kind != "item":
                        continue
                    r = {"id": qid(ch["slug"], q["slug"], "bonus", str(n)), "type": "item", "item": stack(iid)}
                    if bonus_count(count) != 1:
                        r["count"] = bonus_count(count)
                    rewards.append(r)
            quest = {"id": id_, "x": float(q["x"]), "y": float(q["y"])}
            if q["tags"]:
                quest["tags"] = list(q["tags"])
            if q["shape"]:
                quest["shape"] = q["shape"]
            if q["size"]:
                quest["size"] = float(q["size"])
            if q["optional"]:
                quest["optional"] = True
            if q.get("hide_lines"):
                quest["hide_dependency_lines"] = True  # FTB Library Tristate -> plain boolean
            if q["icon"]:
                quest["icon"] = {"id": q["icon"]}
            if q["deps"]:
                quest["dependencies"] = [qid(*d.split("/")) if "/" in d else qid(ch["slug"], d) for d in q["deps"]]
            quest["tasks"] = tasks
            quest["rewards"] = rewards
            quests.append(quest)
        chapter_files[ch["slug"]] = {
            "id": cid,
            "group": group_ids[ch["group"]],
            "order_index": order,
            "filename": ch["slug"],
            "icon": {"id": ch["icon"]},  # icons are written without a count
            "images": [],
            "default_quest_shape": "",
            "default_hide_dependency_lines": False,
            "quest_links": [],
            "quests": quests,
        }

    # Chapter unlocks (spec v2): each chapter's first quest depends on the listed quests elsewhere.
    # With progression_mode "linear", the whole chapter stays locked until those are done.
    all_quests = {(c["slug"], q["slug"]) for c in CHAPTERS for q in c["quests"]}
    for ch in CHAPTERS:
        first = chapter_files[ch["slug"]]["quests"][0]
        for ref in ch["unlock"]:
            assert ref in all_quests, f"{ch['slug']}: unknown unlock {ref}"
            deps = first.setdefault("dependencies", [])
            if qid(*ref) not in deps:  # may already be there via extra_deps
                deps.append(qid(*ref))

    # Remove old .snbt files (so deleted chapters don't linger) but keep folders: OneDrive can lock
    # directories mid-sync, which makes rmtree fail.
    for root, _, files in os.walk(OUT):
        for f in files:
            if f.endswith(".snbt"):
                os.remove(os.path.join(root, f))
    os.makedirs(os.path.join(OUT, "chapters"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "lang"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "reward_tables"), exist_ok=True)
    # Full settings as FTB Quests 2101.1.39 writes them (captured from the game's own re-save on
    # 2026-11-21). Changed from defaults: default_quest_shape "circle", drop_loot_crates off.
    # progression_mode "linear" (spec v2): quests lock until dependencies are done, so chapter unlocks
    # are real in the book. Recipes/items are never locked.
    data = {
        "default_autoclaim_rewards": "disabled",
        "default_consume_items": False,
        "default_quest_disable_jei": False,
        "default_quest_shape": "circle",
        "default_reward_team": False,
        "detection_delay": 20,
        "disable_gui": False,
        "drop_book_on_death": False,
        "drop_loot_crates": False,
        "emergency_items_cooldown": 0,
        "fallback_locale": "",
        "grid_scale": 0.5,
        "hide_excluded_quests": False,
        "lock_message": "",
        "loot_crate_no_drop": {"boss": 0, "monster": 600, "passive": 4000},
        "pause_game": False,
        "presets": {
            "goal": {"shape": "hexagon", "size": 2.0},
            "info": {"shape": "gear", "size": 1.0},
            "normal": {"shape": "square", "size": 1.0},
        },
        "progression_mode": "linear",
        "show_lock_icons": True,
        "verify_on_load": False,
        "version": FILE_VERSION,
    }
    files = {"data.snbt": data,
             "chapter_groups.snbt": {"chapter_groups": [{"id": group_ids[g]} for g, _ in GROUPS]}}
    for slug, ch in chapter_files.items():
        files[os.path.join("chapters", f"{slug}.snbt")] = ch
    # Reward tables (format from RewardTable.writeData, 2101.1.39): file reward_tables/<slug>.snbt,
    # hex "id", "order_index", "loot_size", "rewards" list. Each entry: "id", item reward data
    # ("item" stack + separate "count"), "weight" float only when not 1. "type" only for non-items.
    for order, (slug, table) in enumerate(REWARD_TABLES.items()):
        tid = qid("table", slug)
        lang[f"reward_table.{tid}.title"] = table["title"]
        entries = []
        for n, (iid, count, weight) in enumerate(table["entries"]):
            e = {"id": qid("table", slug, str(n)), "item": stack(iid)}
            if count != 1:
                e["count"] = count
            if weight != 1:
                e["weight"] = Raw(f"{float(weight)}f")
            entries.append(e)
        files[os.path.join("reward_tables", f"{slug}.snbt")] = {
            "id": tid, "order_index": order, "loot_size": 1, "rewards": entries}
    files[os.path.join("lang", "en_us.snbt")] = lang
    for rel, content in files.items():
        with open(os.path.join(OUT, rel), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(write_snbt(content) + "\n")
    n_quests = sum(len(c["quests"]) for c in CHAPTERS)
    print(f"wrote {len(chapter_files)} chapters, {n_quests} quests, {len(lang)} lang entries -> {OUT}")


if __name__ == "__main__":
    build()

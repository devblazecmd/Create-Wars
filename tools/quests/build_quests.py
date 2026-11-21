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
      size=None, optional=False, bonus=True):
    return dict(slug=slug, title=title, x=x, y=y, desc=desc, tasks=tasks, deps=list(deps), xp=xp,
                items=list(items), subtitle=subtitle, icon=icon, shape=shape, size=size, optional=optional,
                bonus=bonus)


def bonus_count(task_count):
    """Owner (2026-11-21): every quest also rewards a little of what it asked you to make.
    About 1/8 of the task amount, at least 1, at most 8."""
    return max(1, min(8, task_count // 8))


def item(i, count=1):
    return ("item", i, count)


CHECK = ("checkmark", None, 0)

# Formatting: &d teleport/quantum, &6 heat, &c combat/rules, &a tips, &r reset

# Sections (FTB Quests chapter groups), in sidebar order. Spec: "Book structure v2".
GROUPS = [
    ("getting_started", "Getting Started"),
    ("ages", "Ages"),
    ("expansions", "Expansions"),
    ("automation", "Automation"),
]

# A "stack" for automate quests (spec v2: automate = make one stack). 16-stackers get 16.
STACK = 64
STACK16 = 16

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
        Q("press", "Mechanical Press & Depot", 4, 0, [
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
            "&7Requires: Press & Depot, Basin and Mixer, Belts and Iron Sheets.&r",
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
        Q("diamond", "Diamonds from Coal", 8, -2, [
            "&eThis pack's own recipe:&r compact &a9 Blocks of Coal&r in a Basin over a",
            "&6Superheated&r burner to make &b1 Diamond&r.",
        ], [item("minecraft:diamond")], deps=["blaze_cake"], xp=40, items=[("minecraft:coal_block", 4)]),
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
            "Your first bucket of &acrude oil&r.",
        ], [item("tfmg:crude_oil_bucket")], xp=30),
        Q("distillation", "Distillation Tower", 0, 0, [
            "A &aDistillation Controller&r and outputs on steel tanks refine crude oil into fuels.",
        ], [item("tfmg:steel_distillation_controller"), item("tfmg:steel_distillation_output", 2)], xp=50),
        Q("gasoline", "Gasoline", 0, 0, [
            "Refined from crude oil. Needed for &cnapalm&r.",
        ], [item("tfmg:gasoline_bucket")], xp=25),
        Q("diesel", "Diesel", 0, 0, [
            "Another distillation product: engine fuel.",
        ], [item("tfmg:diesel_bucket")], xp=20),
        Q("kerosene", "Kerosene", 0, 0, [
            "Another distillation product: aviation fuel.",
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
            "A compact one-way teleport point. Uses Quantum Casings too.",
        ], [item("waystones:white_portstone")], xp=25),
        Q("warp_plate", "Warp Plate", 0, 0, [
            "Step on it to warp to a linked plate. Made with Warp Dust.",
        ], [item("waystones:warp_plate", 2)], xp=25),
        Q("blank_scroll", "Blank Scroll", 0, 0, [
            "&eChanged in this pack:&r every scroll is made from &dQuantum Paper&r.",
        ], [item("waystones:blank_scroll", 3)], xp=20),
        Q("warp_scroll", "Warp Scroll", 0, 0, [
            "One-time teleport to a waystone. Uses a &dQuantum Pearl&r in this pack.",
        ], [item("waystones:warp_scroll")], xp=20),
        Q("return_scroll", "Return Scroll", 0, 0, [
            "Teleports you back to your spawn point.",
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
            "Same smithing upgrade, with an &aanvil&r instead of an enchanting table.",
        ], [item("create_enchantment_industry:blaze_forger")], xp=40),
        Q("printer", "Printer", 0, 0, [
            "Brass sheet, a Spout and a block of iron. Copies books and enchanted books.",
        ], [item("create_enchantment_industry:printer")], xp=40),
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
            "Feed Blocks of Coal into a superheated compactor. Make a &astack&r of Diamonds",
            "(that's 576 coal blocks).",
        ], [item("minecraft:diamond", STACK)], xp=100),
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
        Q("auto_qpearl", "Automate: Quantum Pearls", 0, 0, [
            "Ender pearls and Telejuice into a mixer, automatically. Make a &astack&r (16).",
        ], [item("createwars:quantum_pearl", STACK16)], xp=60),
        Q("enchanting_auto", "Enchanting Automation", 0, 0, [
            "Experience on tap.",
        ], [CHECK], xp=30),
        Q("auto_xp", "Automate: Liquid Experience", 0, 0, [
            "Fill a &astack&r of Bucket o' Enchanting (16) from an automated setup.",
        ], [item("create_enchantment_industry:experience_bucket", STACK16)], xp=75),
    ]),
]


# --------------------------------------------------------------------------------------------------
# Layout: hub-and-spoke (owner's reference screenshot, 2026-11-21)
# --------------------------------------------------------------------------------------------------
# For each chapter: a main line of hubs (left -> right, each depends on the previous), satellites fanned
# around a hub on arcs above and below (each depends on its hub), and an optional gate quest whose
# dependencies are a hand-picked list drawn with hidden lines (so they don't cross the fan).
# x/y/deps written inside Q(...) are IGNORED for chapters listed here; this table is the truth.
#   main: [(slug, x, size)]   all on y = 0
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
        hubs={"welcome": ["team", "claims", "no_elytra", "waystones"]},
        gate=None),
    "kinetics": dict(
        main=[("find_andesite", -5, 1.25), ("andesite_alloy", 0, 2.0), ("casing", 7, 2.0), ("next", 13, 2.0)],
        hubs={"andesite_alloy": dict(top=["shafts_cogs"], bottom=["cogwheels"]),
              "casing": dict(top=["millstone", "press", "basin_mixer"], bottom=["kelp"])},
        chains={"shafts_cogs": ["water_wheel", "large_water_wheel"],  # owner: shaft -> water wheel -> large
                "cogwheels": ["gearbox", "vertical_gearbox"],          # owner: cogs -> gearboxes
                "press": ["iron_sheets"],                              # owner: press & depot -> iron sheets
                "kelp": ["dried_kelp", "belts"]},                      # owner: kelp -> dried kelp -> belts
        fans={"iron_sheets": ["saw_drill", "harvester", "drill", "fan"],    # owner: iron sheets unlock these
              "press": (["gold_sheets"], -60),                              # owner: press -> gold sheet tree
              "gold_sheets": (["wrench_goggles", "goggles"], 0, 90),        # owner: gold sheets -> tools
              "dried_kelp": (["tunnel"], 90)},                              # owner: dried kelp -> tunnels
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
        extra_deps={"napalm": ["heat/biofuel"]},   # napalm needs biofuel (Heat Expansion)
        gate=None),
    "heat": dict(
        main=[("tiers", -5, 1.5), ("blaze_cake", 1, 2.0), ("biofuel", 8, 2.0)],
        hubs={"tiers": dict(top=["cinder_flour"], bottom=["spout"]),
              "blaze_cake": dict(top=["diamond"], bottom=["biomass"]),
              "biofuel": dict(top=["straw"])},
        chains={"cinder_flour": ["cake_base"]},
        gate=None),
    "quantum": dict(
        main=[("chorus", -6, 1.25), ("telejuice", -1, 2.0), ("quantum_pearl", 6, 2.0), ("waystone", 13, 2.0),
              ("advanced_part", 20, 1.75), ("quantum_mechanism", 26, 2.0), ("teleporter", 33, 2.0)],
        hubs={"telejuice": dict(top=["quantum_casing"], bottom=["quantum_paper"]),
              "quantum_pearl": dict(top=["warp_dust"], bottom=["redstone_pearl"]),
              "waystone": dict(top=["blank_scroll"], bottom=["sharestone", "portstone", "warp_plate"]),
              "quantum_mechanism": dict(top=["tp_link"], bottom=["item_tp"]),
              "teleporter": dict(top=["adv_tplink", "custom_portal"])},
        chains={"warp_dust": ["warp_stone"], "item_tp": ["block_teleporter"]},
        fans={"blank_scroll": ["warp_scroll", "return_scroll"]},
        gate=None),
    "enchanting": dict(
        main=[("grindstone", -6, 1.25), ("liquid_xp", -1, 2.0), ("xp_block", 6, 2.0), ("blaze_enchanter", 13, 2.0)],
        hubs={"liquid_xp": dict(top=["xp_cake_base"]),
              "xp_block": dict(top=["enchanting_template"], bottom=["xp_hatch", "xp_lantern"]),
              "blaze_enchanter": dict(top=["blaze_forger"], bottom=["printer"])},
        chains={"xp_cake_base": ["xp_cake"]},
        gate=None),
    "automation": dict(
        main=[("andesite_auto", 0, 2.0), ("brass_auto", 8, 2.0), ("heat_auto", 15, 1.75),
              ("industrial_auto", 22, 1.75), ("quantum_auto", 29, 1.75), ("enchanting_auto", 36, 1.75)],
        hubs={"andesite_auto": dict(top=["auto_cobble", "auto_gravel", "auto_alloy"],
                                    bottom=["auto_iron", "auto_sheets", "auto_kelp"]),
              "brass_auto": dict(top=["auto_brass", "auto_tubes", "auto_precision"], bottom=["crushing"]),
              "heat_auto": dict(top=["auto_cakes", "auto_diamond"], bottom=["auto_biofuel"]),
              "industrial_auto": dict(top=["auto_coke", "auto_steel"], bottom=["auto_gasoline"]),
              "quantum_auto": dict(top=["auto_telejuice"], bottom=["auto_qpearl"]),
              "enchanting_auto": dict(top=["auto_xp"])},
        chains={"crushing": ["auto_zinc"]},
        # each tier hub also needs progress in its own chapter (not drawn: other chapter)
        extra_deps={"brass_auto": ["brass_and_precision/brass_casing"],
                    "heat_auto": ["heat/blaze_cake"],
                    "industrial_auto": ["industrial/steel"],
                    "quantum_auto": ["quantum/telejuice"],
                    "enchanting_auto": ["enchanting/liquid_xp"]},
        gate=None),
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
    for slug, x, size in lay["main"]:
        q = by[slug]
        q.update(x=x, y=0, size=size, deps=[prev] if prev else [])
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
                tasks.append(t)
            rewards = []
            if q["xp"]:
                rewards.append({"id": qid(ch["slug"], q["slug"], "xp"), "type": "xp", "xp": q["xp"]})
            for n, (iid, count) in enumerate(q["items"]):
                # ItemReward keeps the amount in its own "count"; the stack itself is count 1 (game format)
                rewards.append({"id": qid(ch["slug"], q["slug"], "reward", str(n)), "type": "item",
                                "item": stack(iid), "count": count})
            if q["bonus"]:
                for n, (kind, iid, count) in enumerate(q["tasks"]):
                    if kind != "item":
                        continue
                    r = {"id": qid(ch["slug"], q["slug"], "bonus", str(n)), "type": "item", "item": stack(iid)}
                    if bonus_count(count) != 1:
                        r["count"] = bonus_count(count)
                    rewards.append(r)
            quest = {"id": id_, "x": float(q["x"]), "y": float(q["y"])}
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
            first.setdefault("dependencies", []).append(qid(*ref))

    # Remove old .snbt files (so deleted chapters don't linger) but keep folders: OneDrive can lock
    # directories mid-sync, which makes rmtree fail.
    for root, _, files in os.walk(OUT):
        for f in files:
            if f.endswith(".snbt"):
                os.remove(os.path.join(root, f))
    os.makedirs(os.path.join(OUT, "chapters"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "lang"), exist_ok=True)
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
    files[os.path.join("lang", "en_us.snbt")] = lang
    for rel, content in files.items():
        with open(os.path.join(OUT, rel), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(write_snbt(content) + "\n")
    n_quests = sum(len(c["quests"]) for c in CHAPTERS)
    print(f"wrote {len(chapter_files)} chapters, {n_quests} quests, {len(lang)} lang entries -> {OUT}")


if __name__ == "__main__":
    build()

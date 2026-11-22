"""Check that every item/block ID referenced by the FTB Quests book exists in the pack.

Usage:
    python -I tools/check_quest_refs.py [quests_dir] [--instance <path>]

Defaults:
    quests_dir  pack/config/ftbquests/quests
    --instance  the Prism "Create Wars" instance (its mods/ folder must be synced from pack/)

Known IDs are collected from:
  * every mod jar in <instance>/minecraft/mods (and jars bundled inside them under META-INF/jarjar)
  * the vanilla 1.21.1 client jar from Prism's libraries
  * createwars:* items registered in pack/kubejs/startup_scripts/*.js
An ID counts as known if it has an item model (assets/<ns>/models/item/<path>.json) or an
item./block. lang key. Exit code 1 if any referenced ID is unknown.

Why: the most common modpack quest bug is a quest pointing at an item that was renamed or removed
(e.g. elytras, Mob Radar, the Air War launchers). See vault/03-Design/Quest Book.md.
"""
import io
import os
import re
import sys
import zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_QUESTS = os.path.join(REPO, "pack", "config", "ftbquests", "quests")
DEFAULT_INSTANCE = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "PrismLauncher",
                                "instances", "Create Wars")
VANILLA_JAR = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "PrismLauncher", "libraries",
                           "com", "mojang", "minecraft", "1.21.1", "minecraft-1.21.1-client.jar")

MODEL_RE = re.compile(r"^assets/([a-z0-9_.-]+)/models/item/([a-z0-9_/.-]+)\.json$")
LANG_RE = re.compile(r"^assets/[a-z0-9_.-]+/lang/en_us\.json$")
# kind (item/block/entity), namespace, path. Entities so kill-task IDs are checked (2026-11-21).
LANG_KEY_RE = re.compile(r'"(item|block|entity)\.([a-z0-9_-]+)\.([a-z0-9_/-]+)"\s*:')
KJS_ITEM_RE = re.compile(r"""event\.create\(\s*['"]([a-z0-9_.-]+:[a-z0-9_/.-]+)['"]""")
# Items that exist in the registry but the pack has taken out of play. Quests must not reference them.
# Keep in sync with pack/kubejs/server_scripts/elytra_removed.js, air_war_launchers_removed.js and
# potr_tools_removed.js.
BANNED = {
    "minecraft:elytra",
    "create_the_air_wars:anti_aircraft_launcher", "create_the_air_wars:c75",
    "create_the_air_wars:vihr", "create_the_air_wars:vihr_rocket",
    "create_the_air_wars:heattrap", "create_the_air_wars:heattrap_charge",
} | {f"adpother:{t}_{k}" for t in ("iron", "gold", "diamond")
     for k in ("filter_frame", "vacuum_bag", "vacuum_tube", "respirator")} | {"adpother:aerometer"}
# metal_unification.js: non-TFMG steel and lead are hidden; quests use TFMG's.
BANNED |= {"createbigcannons:steel_ingot", "createbigcannons:steel_block",
           "cgs:steel_ingot", "cgs:steel_nugget", "cgs:steel_block",
           "createnuclear:steel_ingot", "createnuclear:steel_nugget", "createnuclear:steel_block",
           # lead (2026-11-22): quests use TFMG's
           *{f"{m}:{f}" for m in ("cgs", "createnuclear") for f in ("lead_ingot", "lead_nugget", "lead_block",
             "raw_lead", "raw_lead_block", "lead_ore", "deepslate_lead_ore")}}
# wire_unification.js (2026-11-22): C&A wire + spool are primary
BANNED |= {"tfmg:copper_wire", "create_the_air_wars:wires", "tfmg:empty_spool"}
# nuclear_weapons.js: every CBC Enhanced Shells item is hidden except the four nukes.
CBCES_KEEP = {"cbc_enhanced_shells:nuke_shell", "cbc_enhanced_shells:nuke_shell_mk2",
              "cbc_enhanced_shells:h_bomb_shell", "cbc_enhanced_shells:h_bomb_mini_shell"}
# Any quoted namespaced ID in quest SNBT (quest object IDs are bare hex, so they never match).
REF_RE = re.compile(r'"#?([a-z0-9_.-]+:[a-z0-9_/.-]+)"')


def scan_jar(zf, known):
    """known = {"item": set, "block": set, "entity": set}. An item model counts as an item.
    A block name alone does NOT make an item (2026-11-21: rha:hatcholive is a block with no item form,
    and the game turned that quest task into ftbquests:missing_item)."""
    for name in zf.namelist():
        m = MODEL_RE.match(name)
        if m:
            known["item"].add(f"{m.group(1)}:{m.group(2)}")
        elif LANG_RE.match(name):
            text = zf.read(name).decode("utf-8", "replace")
            for kind, a, b in LANG_KEY_RE.findall(text):
                known[kind].add(f"{a}:{b}")
        elif name.startswith("META-INF/jarjar/") and name.endswith(".jar"):
            try:
                with zipfile.ZipFile(io.BytesIO(zf.read(name))) as inner:
                    scan_jar(inner, known)
            except zipfile.BadZipFile:
                pass


def known_ids(instance):
    known = {"item": set(), "block": set(), "entity": set()}
    mods = os.path.join(instance, "minecraft", "mods")
    jars = [os.path.join(mods, f) for f in os.listdir(mods) if f.endswith(".jar")]
    jars.append(VANILLA_JAR)
    for path in jars:
        with zipfile.ZipFile(path) as zf:
            scan_jar(zf, known)
    startup = os.path.join(REPO, "pack", "kubejs", "startup_scripts")
    if os.path.isdir(startup):
        for f in os.listdir(startup):
            if f.endswith(".js"):
                with open(os.path.join(startup, f), encoding="utf-8") as fh:
                    known["item"].update(KJS_ITEM_RE.findall(fh.read()))
    return known


def referenced_ids(quests_dir):
    refs = {}
    for root, _, files in os.walk(quests_dir):
        if os.path.basename(root) == "lang":
            continue  # display text only
        for f in files:
            if f.endswith(".snbt"):
                path = os.path.join(root, f)
                with open(path, encoding="utf-8") as fh:
                    for i, line in enumerate(fh, 1):
                        for ref in REF_RE.findall(line):
                            refs.setdefault(ref, []).append(f"{os.path.relpath(path, quests_dir)}:{i}")
    return refs


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    instance = DEFAULT_INSTANCE
    if "--instance" in argv:
        instance = argv[argv.index("--instance") + 1]
        args.remove(instance)
    quests_dir = args[0] if args else DEFAULT_QUESTS

    known = known_ids(instance)
    usable = known["item"] | known["entity"]
    # Authoritative when present: the live registry, exported by pack/kubejs/server_scripts/
    # export_registry_ids.js on the last server load. Jar scanning can't see items that ship assets but
    # are never registered.
    export = os.path.join(instance, "minecraft", "kubejs", "exported", "createwars_registry.json")
    source = "jar scan"
    if os.path.isfile(export):
        import json
        with open(export, encoding="utf-8") as fh:
            reg = json.load(fh)
        usable = set(reg["items"]) | set(reg["entities"])
        known["block"] = known["block"] - usable
        source = f"live registry export ({os.path.getmtime(export) and 'kubejs/exported/createwars_registry.json'})"
    print(f"ID source: {source}")
    refs = referenced_ids(quests_dir)
    unknown = {r: locs for r, locs in refs.items() if r not in usable and r not in known["block"]}
    block_only = {r: locs for r, locs in refs.items() if r not in usable and r in known["block"]}
    banned = {r: locs for r, locs in refs.items()
              if r in BANNED or (r.startswith("cbc_enhanced_shells:") and r not in CBCES_KEEP)}

    print(f"known items: {len(known['item'])}  entities: {len(known['entity'])}  referenced: {len(refs)}  "
          f"unknown: {len(unknown)}  block-only: {len(block_only)}  banned: {len(banned)}")
    for ref, locs in sorted(unknown.items()):
        print(f"  UNKNOWN {ref}  at {', '.join(locs)}")
    for ref, locs in sorted(block_only.items()):
        print(f"  BLOCK-ONLY {ref}  at {', '.join(locs)}  (a block with no item form: an item task can't be completed)")
    for ref, locs in sorted(banned.items()):
        print(f"  BANNED  {ref}  at {', '.join(locs)}  (removed from play by a pack script)")
    return 1 if unknown or banned or block_only else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
